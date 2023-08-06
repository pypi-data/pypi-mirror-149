"""MIDAS upgrade module for simbench data simulator."""
import os

import pandas as pd
from midas.util.base_data_module import BaseDataModule

from . import LOG
from .download import download_simbench


class SimbenchDataModule(BaseDataModule):
    """Upgrade module for simbench data.

    Other, similar data modules can derive from this class.

    """

    def __init__(self):
        super().__init__(
            module_name="sbdata",
            default_scope_name="sbrural3",
            default_sim_config_name="SimbenchData",
            default_import_str=(
                "midas.modules.sbdata.simulator:SimbenchDataSimulator"
            ),
            default_cmd_str="TODO",
            log=LOG,
        )

        self.models = {
            "load": ["p_mw", "q_mvar"],
            "sgen": ["p_mw", "q_mvar"],
            "storage": ["p_mw", "q_mvar"],
        }

    def check_module_params(self, module_params):
        """Check the module params and provide default values."""

        super().check_module_params(module_params)
        module_params.setdefault("load_scaling", 1.0)
        module_params.setdefault("sgen_scaling", 1.0)
        module_params.setdefault("storage_scaling", 1.0)

    def check_sim_params(self, module_params):
        """Check the params for a certain simulator instance."""

        super().check_sim_params(module_params)

        self.sim_params.setdefault(
            "load_scaling", module_params["load_scaling"]
        )
        self.sim_params.setdefault(
            "sgen_scaling", module_params["sgen_scaling"]
        )
        self.sim_params.setdefault(
            "storage_scaling", module_params["storage_scaling"]
        )
        self.sim_params.setdefault("load_mapping", "default")
        self.sim_params.setdefault("sgen_mapping", "default")
        self.sim_params.setdefault("storage_mapping", "default")

        gridfile = self.params["powergrid_params"][
            self.sim_params["grid_name"]
        ]["gridfile"]
        self.sim_params.setdefault(
            "filename",
            f"{gridfile}.hdf5",
        )

    def start_models(self):
        """Start models of a certain simulator."""
        for model in self.models:
            mapping_key = f"{model}_mapping"
            if isinstance(self.sim_params[mapping_key], str):
                self.sim_params[mapping_key] = self.create_default_mapping(
                    model
                )

            mapping = self.scenario.create_shared_mapping(
                self, self.sim_params["grid_name"], model
            )

            for bus, entities in self.sim_params[mapping_key].items():
                mapping.setdefault(bus, list())
                for (eidx, scale) in entities:
                    model_key = self.scenario.generate_model_key(
                        self, model, bus, eidx
                    )
                    scaling = scale * float(
                        self.sim_params[f"{model}_scaling"]
                    )

                    params = {"scaling": scaling, "eidx": eidx}
                    full_id = self.start_model(
                        model_key, model.capitalize(), params
                    )

                    info = self.scenario.get_sim(self.sim_key).get_data_info()
                    meid = full_id.split(".")[-1]
                    mapping[bus].append(
                        (model, info[meid]["p_mwh_per_a"] * scaling)
                    )

    def connect(self):
        """Create connections to other entities."""
        for model, attrs in self.models.items():
            mapping_key = f"{model}_mapping"
            for bus, entities in self.sim_params[mapping_key].items():
                for (eidx, _) in entities:
                    model_key = self.scenario.generate_model_key(
                        self, model, bus, eidx
                    )
                    grid_entity_key = self.get_grid_entity(model, bus)
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
        """Create a default mapping.

        Tries to read the default mapping from hdf5 db that stores
        the data.
        """

        info = self.scenario.get_sim(self.sim_key).get_data_info()
        num_models = f"max_{model}s"
        self.sim_params[num_models] = info[num_models]

        self.logger.debug(
            "Try to load %s default mapping from hdf5 db ...", model
        )
        file_path = os.path.join(
            self.sim_params["data_path"], self.sim_params["filename"]
        )

        default_mapping = dict()
        try:
            mapping = pd.read_hdf(file_path, f"{model}_default_mapping")
        except KeyError:
            self.logger.debug("No default mapping for %s in database.", model)
            mapping = None

        for eidx in range(self.sim_params[num_models]):
            try:
                bus = mapping.loc[eidx]["bus"]
            except TypeError:
                bus = eidx
            except KeyError:
                break
            default_mapping.setdefault(bus, list())
            default_mapping[bus].append([eidx, 1.0])

        return default_mapping

    def download(self, data_path, tmp_path, if_necessary, force):
        download_simbench(data_path, tmp_path, if_necessary, force)

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
