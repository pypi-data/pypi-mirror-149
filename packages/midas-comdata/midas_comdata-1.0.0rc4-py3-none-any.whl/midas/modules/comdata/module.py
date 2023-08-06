"""MIDAS upgrade module for the commercial data simulator."""
import logging

import pandas as pd
from midas.util.runtime_config import RuntimeConfig
from midas.util.upgrade_module import UpgradeModule

from .download import download_commercials

LOG = logging.getLogger(__name__)


class CommercialDataModule(UpgradeModule):
    def __init__(self):
        super().__init__(
            module_name="comdata",
            default_scope_name="midasmv",
            default_sim_config_name="CommercialData",
            default_import_str=(
                "midas.modules.comdata.simulator:CommercialDataSimulator"
            ),
            default_cmd_str="TODO",
            log=LOG,
        )
        attrs = ["p_mw", "q_mvar"]
        self.models = {
            "FullServiceRestaurant": attrs,
            "Hospital": attrs,
            "LargeHotel": attrs,
            "LargeOffice": attrs,
            "MediumOffice": attrs,
            "MidriseApartment": attrs,
            "OutPatient": attrs,
            "PrimarySchool": attrs,
            "QuickServiceRestaurant": attrs,
            "SecondarySchool": attrs,
            "SmallHotel": attrs,
            "SmallOffice": attrs,
            "StandaloneRetail": attrs,
            "StripMall": attrs,
            "SuperMarket": attrs,
            "Warehouse": attrs,
        }

    def check_module_params(self, module_params):
        """Check the module params and provide default values."""

        module_params.setdefault("start_date", self.scenario.base.start_date)
        module_params.setdefault("data_path", self.scenario.base.data_path)
        module_params.setdefault("cos_phi", self.scenario.base.cos_phi)
        module_params.setdefault("interpolate", False)
        module_params.setdefault("noise_factor", 0.2)
        module_params.setdefault("load_scaling", 1.0)

        if self.scenario.base.no_rng:
            module_params["randomize_data"] = False
            module_params["randomize_cos_phi"] = False
        else:
            module_params.setdefault("randomize_data", False)
            module_params.setdefault("randomize_cos_phi", False)

    def check_sim_params(self, module_params):
        """Check the params for a certain simulator instance."""

        self.sim_params.setdefault("grid_name", self.scope_name)
        self.sim_params.setdefault("start_date", module_params["start_date"])
        self.sim_params.setdefault("data_path", module_params["data_path"])
        self.sim_params.setdefault("cos_phi", module_params["cos_phi"])
        self.sim_params.setdefault("interpolate", module_params["interpolate"])
        self.sim_params.setdefault(
            "randomize_data", module_params["randomize_data"]
        )
        self.sim_params.setdefault(
            "randomize_cos_phi", module_params["randomize_cos_phi"]
        )
        self.sim_params.setdefault("seed_max", self.scenario.base.seed_max)
        self.sim_params.setdefault("seed", self.scenario.create_seed())
        self.sim_params.setdefault(
            "filename", RuntimeConfig().data["commercials"][0]["name"]
        )

    def start_models(self):
        """Start models of a certain simulator."""
        mapping_key = "mapping"
        self.sim_params.setdefault(mapping_key, self.create_default_mapping())
        if not self.sim_params[mapping_key]:
            # No mappings configured
            return

        mapping = self.scenario.create_shared_mapping(
            self, self.sim_params["grid_name"], "load"
        )

        for model in self.models:
            for bus, entities in self.sim_params[mapping_key].items():
                mapping.setdefault(bus, [])
                for eidx, (name, scale) in enumerate(entities):
                    if model != name:
                        continue

                    model_key = self.scenario.generate_model_key(
                        self, model.lower(), bus, eidx
                    )
                    scaling = scale * float(
                        self.sim_params.get("load_scaling", 1.0)
                    )
                    params = {"scaling": scaling}
                    self.start_model(model_key, model, params)

                    # Prepare some infor for other modules
                    info = self.scenario.get_sim(self.sim_key).get_data_info()
                    meid = self.scenario.get_model(model_key, self.sim_key).eid
                    mapping[bus].append(
                        (model, info[meid]["p_mwh_per_a"] * scaling)
                    )

    def connect(self):
        mapping_key = "mapping"
        for model, attrs in self.models.items():
            for bus, entities in self.sim_params[mapping_key].items():
                for eidx, (name, _) in enumerate(entities):
                    if model != name:
                        continue

                    model_key = self.scenario.generate_model_key(
                        self, model.lower(), bus, eidx
                    )
                    grid_entity_key = self.get_grid_entity("load", bus)
                    self.connect_entities(model_key, grid_entity_key, attrs)

    def connect_to_db(self):
        """Connect the models to db."""
        mapping_key = "mapping"
        db_key = self.scenario.find_first_model("store", "database")[0]

        for model, attrs in self.models.items():
            for bus, entities in self.sim_params[mapping_key].items():
                for eidx, (name, _) in enumerate(entities):
                    if model != name:
                        continue
                    model_key = self.scenario.generate_model_key(
                        self, model.lower(), bus, eidx
                    )
                    self.connect_entities(model_key, db_key, attrs)

    def get_grid_entity(self, mtype, bus):
        models = self.scenario.find_grid_entities(
            self.sim_params["grid_name"], mtype, endswith=f"_{bus}"
        )
        if models:
            for key in models:
                # Return first match
                return key

        self.logger.info(
            "Grid entity for %s, %s at bus %d not found",
            self.sim_params["grid_name"],
            mtype,
            bus,
        )
        raise ValueError(
            f"Grid entity for {self.sim_params['grid_name']}, {mtype} "
            f"at bus {bus} not found!"
        )

    def create_default_mapping(self):
        default_mapping = {}
        if self.sim_params["grid_name"] == "midasmv":
            default_mapping = {
                13: [["SuperMarket", 0.089]],
                14: [["SmallHotel", 0.022]],
            }

        return default_mapping

    def download(self, data_path, tmp_path, if_necessary, force):
        download_commercials(data_path, tmp_path, if_necessary, force)

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
