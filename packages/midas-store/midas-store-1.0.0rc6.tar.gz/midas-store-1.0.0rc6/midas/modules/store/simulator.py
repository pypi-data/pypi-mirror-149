import os
import threading

import mosaik_api
import pandas as pd
from midas.util.logging import set_and_init_logger

from . import LOG
from .meta import META

pd.set_option("io.hdf.default_format", "table")


class MidasHdf5(mosaik_api.Simulator):
    """A mosaik data collector using pytables and hdf.

    This mosaik simulator is able to take any number of inputs from
    mosaik and stores them in a HDF database file. This is done using
    pandas and pytables.

    The only requirement is that the input can be put into a cell of a
    pandas dataframe, i.e., basic data types like int, float, and
    string are supported. More complex structures need to be serialized
    beforehand, e.g., if you want to store a dictionary, use json to
    serialize it to a string.

    MidasHdf5 tries to be non-destructive when it comes to the database
    file. If you pass a filename that already exists on the table, a
    new filename will be searched. This is usually just the old
    filename with an increment, e.g., if you pass my_db.hdf5, which
    already exists, the filename will be my_db-2.hdf5. This behavior
    can be disabled by providing the flag *overwrite*. However, even
    then the old database file will not directly overwritten, but moved
    to my_db.hdf5.old instead.

    Another option is *buffer_size*. Running large simulations can lead
    to a really large data set that is stored in-memory. This may be
    undesired for various reasons. Setting *buffer_size* to a value >0,
    the collected data will be saved to disc every buffer_size steps.
    Generally, writing to disc is done with a thread so using the
    buffer size should not affect the overall performance. It is
    recommended, though, to not set the buffer_size too low.

    """

    def __init__(self):
        super().__init__(META)

        self.sid = None
        self.eid = "Database"
        self.database = None
        self.filename = None
        self.step_size = None
        self.current_size = 0
        self.buffer_size = None
        self.saved_rows = 0
        self.finalized = False
        self.keep_old_files = True
        self._worker = None

    def init(self, sid, **sim_params):
        self.sid = sid
        self.step_size = sim_params.get("step_size", 900)

        return self.meta

    def create(self, num, model, **model_params):
        errmsg = (
            "You should realy not try to instantiate more than one "
            "database. If your need another database, create a new "
            "simulator as well."
        )
        assert self.database is None, errmsg
        assert num == 1, errmsg

        self.keep_old_files = model_params.get("keep_old_files", False)
        self.filename = model_params.get("filename", None)
        if self.filename is not None and not self.filename.endswith(".hdf5"):
            self.filename = f"{self.filename}.hdf5"

        if self.keep_old_files:
            LOG.debug(
                "Keep_old_files is set to True. Attempting to find a unique "
                "filename for the database."
            )
            incr = 2
            new_filename = self.filename
            while os.path.exists(new_filename):
                new_filename = f"{self.filename[:-5]}_{incr}.hdf5"
                incr += 1
            self.filename = new_filename
        elif os.path.exists(self.filename):
            os.rename(self.filename, f"{self.filename}.old")

        self.buffer_size = model_params.get("buffer_size", 0)

        if self.buffer_size is None:
            self.buffer_size = 0
            LOG.info(
                "Buffer size is set to 0. Store will be saved as-whole"
                "once the simulation is finished."
            )

        LOG.info("Saving results to database at '%s'.", self.filename)
        self.database = dict()

        return [{"eid": self.eid, "type": model}]

    def step(self, time, inputs, max_advance=0):
        data = inputs.get(self.eid, {})

        if not data:
            LOG.info(
                "Did not receive any inputs. "
                "Did you connect anything to the store?"
            )

        current = dict()
        for attr, src_ids in data.items():
            for src_id, val in src_ids.items():
                sid, eid = src_id.split(".")
                key = f"{eid}___{attr}".replace("-", "__")
                sid = sid.replace("-", "__")

                current.setdefault(sid, dict())
                current[sid].setdefault("cols", list()).append(key)
                current[sid].setdefault("vals", list()).append(val)

        if self._worker is not None:
            LOG.debug("Waiting for the store worker to finish...")
            self._worker.join()
            LOG.debug("Clearing current database.")
            self.database = dict()
            self._worker = None

        for sid, data in current.items():
            self.database.setdefault(sid, pd.DataFrame())

            ndf = pd.DataFrame([data["vals"]], columns=data["cols"])

            self.database[sid] = pd.concat(
                [self.database[sid], ndf], ignore_index=True
            )

        if self.buffer_size > 0:
            self.current_size += 1

            if self.current_size >= self.buffer_size:
                self._clear_buffer()
                self.current_size = 0

        return time + self.step_size

    def get_data(self, outputs):
        return dict()

    def finalize(self):
        if self.finalized:
            return
        else:
            self.finalized = True

        append = self.buffer_size > 0
        self._to_hdf(append)

    def _clear_buffer(self):
        LOG.debug("Starting worker thread to save the current database...")
        self._worker = threading.Thread(target=self._to_hdf)
        self._worker.start()

    def _to_hdf(self, append=True):
        if not self.database:
            LOG.warning("Database is empty. Unable to write anything to disk.")
            return

        errors = list()
        for sid, data in self.database.items():
            try:
                data.index += self.saved_rows
                data.to_hdf(self.filename, sid, format="table", append=append)
            except Exception:
                LOG.info(
                    "Couldn't save data of simulator %s. Trying to load "
                    "existing data and append manually. ",
                    sid,
                )
                try:
                    edata = pd.read_hdf(self.filename, sid)
                    edata = pd.concat([edata, data])
                    edata.to_hdf(
                        self.filename, sid, format="table", append=False
                    )
                    LOG.info(
                        "Successfully appended the data. One reason could be "
                        "that some values have inconsistent types, e.g., are "
                        "int in the one step and float in the other. As long "
                        "as this is not fixed, this message will probably "
                        "re-appear."
                    )
                except Exception as err:
                    LOG.error(
                        "Could not append data for simulator %s. "
                        "Attempting to export the data to csv.",
                        sid,
                    )
                    fname = os.path.abspath(
                        os.path.join(os.getcwd(), f"fail_{sid}.csv")
                    )
                    LOG.debug("Failed at SID '%s'.", sid)
                    LOG.debug("Columns: %s ", data.columns)
                    LOG.debug("Trying to export data to '%s'", fname)
                    LOG.debug("%s", data.info())

                    data.to_csv(fname)

                    errors.append(err)

        current_num_rows = data.shape[0]
        self.saved_rows += current_num_rows
        if len(errors) > 0:
            LOG.warning("Worker finished with errors: %s", errors)
        else:
            LOG.debug("Worker finished.")
        LOG.info("Wrote %d rows into the store.", current_num_rows)


if __name__ == "__main__":
    set_and_init_logger(0, "store-logfile", "midas-store.log", replace=True)

    mosaik_api.start_simulation(MidasHdf5())
