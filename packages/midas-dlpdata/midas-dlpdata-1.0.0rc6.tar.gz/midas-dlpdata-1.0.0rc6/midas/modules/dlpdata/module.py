"""MIDAS upgrade module for Smart Nord data simulator."""
import logging

import pandas as pd
from midas.util.base_data_module import BaseDataModule
from midas.util.runtime_config import RuntimeConfig

from .download import download_dlp

LOG = logging.getLogger(__name__)


class DLPDataModule(BaseDataModule):
    def __init__(self):
        super().__init__(
            module_name="dlpdata",
            default_scope_name="midasmv",
            default_sim_config_name="DefaultLoadProfiles",
            default_import_str="midas.modules.dlpdata.simulator:DLPSimulator",
            default_cmd_str=(
                "%(python)s -m midas.modules.dlpdata.simulator %(addr)s"
            ),
            log=LOG,
        )

        self.attrs = ["p_mw", "q_mvar"]
        self.models = {
            "H0": self.attrs,
            "G0": self.attrs,
            "G1": self.attrs,
            "G2": self.attrs,
            "G3": self.attrs,
            "G4": self.attrs,
            "G5": self.attrs,
            "G6": self.attrs,
            "L0": self.attrs,
            "L1": self.attrs,
            "L2": self.attrs,
        }
        self._scaling_key = "p_mwh_per_a"

    def check_module_params(self, module_params):
        """Check the module params and provide default values."""
        super().check_module_params(module_params)

        module_params.setdefault(
            "load_scaling", module_params.get("scaling", 1.0)
        )

    def check_sim_params(self, module_params):
        """Check the params for a certain simulator instance."""
        super().check_sim_params(module_params)

        self.sim_params.setdefault(
            "load_scaling", module_params["load_scaling"]
        )
        self.sim_params.setdefault(
            "filename",
            RuntimeConfig().data["default_load_profiles"][0]["name"],
        )

    def start_models(self):
        """Start models of a certain simulator."""
        mapping_key = "mapping"

        self.start_models_from_mapping(mapping_key, None, "load")

    def connect(self):
        mapping_key = "mapping"

        self.connect_to_grid(mapping_key, None, "load", self.attrs)

    def connect_to_db(self):
        """Connect the models to db."""
        mapping_key = "mapping"
        attrs = ["p_mw", "q_mvar"]
        self._connect_to_db(mapping_key, None, attrs)

    def download(self, data_path, tmp_path, if_necessary, force):
        download_dlp(data_path, tmp_path, if_necessary, force)

    def analyze(
        self,
        name: str,
        data: pd.HDFStore,
        output_folder: str,
        start: int,
        end: int,
        step_size: int,
        full: bool,
    ):
        # No analysis, yet
        pass
