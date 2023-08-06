"""MIDAS upgrade module for Smart Nord data simulator."""
import logging

import pandas as pd
from midas.util.base_data_module import BaseDataModule
from midas.util.runtime_config import RuntimeConfig

from .download import download_smartnord

LOG = logging.getLogger(__name__)


class SmartNordDataModule(BaseDataModule):
    def __init__(self):
        super().__init__(
            module_name="sndata",
            default_scope_name="midasmv",
            default_sim_config_name="SmartNordData",
            default_import_str=(
                "midas.modules.sndata.simulator:SmartNordDataSimulator"
            ),
            default_cmd_str="TODO",
            log=LOG,
        )
        self.models = {
            "household": ["p_mw", "q_mvar"],
            "land": ["p_mw", "q_mvar"],
        }

    def check_module_params(self, module_params):
        """Check the module params and provide default values."""
        super().check_module_params(module_params)

        module_params.setdefault("load_scaling", 1.0)

    def check_sim_params(self, module_params):
        """Check the params for a certain simulator instance."""

        super().check_sim_params(module_params)

        self.sim_params.setdefault(
            "load_scaling", module_params["load_scaling"]
        )
        self.sim_params.setdefault(
            "filename", RuntimeConfig().data["smart_nord"][0]["name"]
        )

    def start_models(self):
        """Start models of a certain simulator."""
        for model in self.models:
            mapping_key = f"{model}_mapping"

            self.sim_params.setdefault(
                mapping_key, self.create_default_mapping(model)
            )
            if not self.sim_params[mapping_key]:
                # No mappings configured
                continue

            mapping = self.scenario.create_shared_mapping(
                self, self.sim_params["grid_name"], "load"
            )

            for bus, entities in self.sim_params[mapping_key].items():
                mapping.setdefault(bus, [])
                for (eidx, scale) in entities:
                    model_key = self.scenario.generate_model_key(
                        self, model, bus, eidx
                    )
                    scaling = scale * float(
                        self.sim_params.get("load_scaling", 1.0)
                    )

                    params = {"scaling": scaling, "eidx": eidx}
                    self.start_model(model_key, model.capitalize(), params)

                    # Prepare some info for other modules
                    info = self.scenario.get_sim(self.sim_key).get_data_info()
                    meid = self.scenario.get_model(model_key, self.sim_key).eid
                    mapping[bus].append(
                        (model, info[meid]["p_mwh_per_a"] * scaling)
                    )

    def connect(self):
        for model, attrs in self.models.items():
            mapping = self.sim_params[f"{model}_mapping"]
            for bus, entities in mapping.items():
                for (eidx, _) in entities:
                    model_key = self.scenario.generate_model_key(
                        self, model, bus, eidx
                    )
                    grid_entity_key = self.get_grid_entity("load", bus)
                    self.connect_entities(model_key, grid_entity_key, attrs)

    def connect_to_db(self):
        """Connect the models to db."""
        db_key = self.scenario.find_first_model("store", "database")[0]

        for model, attrs in self.models.items():
            map_key = f"{model}_mapping"

            for bus, entities in self.sim_params[map_key].items():
                for (eidx, _) in entities:
                    model_key = self.scenario.generate_model_key(
                        self, model, bus, eidx
                    )
                    self.connect_entities(model_key, db_key, attrs)

    def create_default_mapping(self, model):
        default_mapping = {}

        if self.sim_params["grid_name"] == "midasmv":
            if model == "land":
                default_mapping = {
                    1: [[0, 1.0], [2, 1.0], [3, 3.0], [6, 2.0], [7, 1.0]],
                    3: [[0, 1.0], [2, 1.0], [3, 1.0], [6, 1.0], [7, 1.0]],
                    4: [[0, 3.0], [3, 2.0], [7, 1.0]],
                    5: [[3, 2.0], [7, 1.0]],
                    6: [[0, 1.0], [3, 2.0]],
                    7: [[0, 3.0], [2, 1.0], [3, 2.0], [7, 1.0]],
                    8: [[0, 2.0], [3, 1.0], [6, 1.0]],
                    9: [[2, 1.0], [3, 2.0], [6, 2.0], [7, 1.0]],
                    10: [[0, 2.0], [2, 1.0], [3, 2.0], [6, 2.0], [7, 1.0]],
                    11: [[0, 2.0], [2, 1.0], [3, 2.0], [6, 2.0], [7, 1.0]],
                }

        return default_mapping

    def download(self, data_path, tmp_path, if_necessary, force):
        return download_smartnord(data_path, tmp_path, if_necessary, force)

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
