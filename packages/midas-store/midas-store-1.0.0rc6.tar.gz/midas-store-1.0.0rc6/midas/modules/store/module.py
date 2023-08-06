"""MIDAS scenario upgrade module.

This module adds a mosaikhdf database to the scenario.

"""
import logging
import os

from midas.util.upgrade_module import UpgradeModule

LOG = logging.getLogger(__name__)


class DatabaseModule(UpgradeModule):
    def __init__(self):
        super().__init__(
            module_name="store",
            default_scope_name="database",
            default_sim_config_name="MidasStore",
            default_import_str="midas.modules.store.simulator:MidasHdf5",
            default_cmd_str=(
                "%(python)s -m midas.modules.store.simulator %(addr)s"
            ),
            log=LOG,
        )
        self.default_filename = "midas_store.hdf5"
        self.filename = None

    def check_module_params(self, module_params):
        """Check module params for this upgrade."""

        module_params.setdefault(self.default_scope_name, dict())
        module_params.setdefault("buffer_size", 0)
        module_params.setdefault("keep_old_files", False)
        module_params.setdefault("filename", self.default_filename)
        if module_params["filename"] is not None:
            module_params["filename"] = os.path.abspath(
                os.path.join(
                    self.scenario.base.output_path, module_params["filename"]
                )
            )

    def check_sim_params(self, module_params):

        self.filename = module_params["filename"]

        if "MosaikHdf5" in self.sim_params["import_str"]:
            self.scenario["db_restricted"] = True
            self.sim_params["duration"] = self.scenario["end"]
        else:
            self.sim_params.setdefault(
                "buffer_size", module_params["buffer_size"]
            )
            self.sim_params.setdefault(
                "keep_old_files", module_params["keep_old_files"]
            )

    def start_models(self):
        mod_key = "database"
        params = {"filename": self.filename}

        if "midas" in self.sim_params["import_str"]:
            params["buffer_size"] = self.sim_params["buffer_size"]
            params["keep_old_files"] = self.sim_params["keep_old_files"]

        self.start_model(mod_key, "Database", params)

    def connect(self):
        pass

    def connect_to_db(self):
        pass
