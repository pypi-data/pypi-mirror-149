"""MIDAS upgrade module for PV and Wind timeseries data simulator."""
import logging

import pandas as pd
from midas.util.runtime_config import RuntimeConfig
from midas.util.upgrade_module import UpgradeModule

from .download import download_gen

LOG = logging.getLogger(__name__)


class PVWindDataModule(UpgradeModule):
    def __init__(self):
        super().__init__(
            module_name="pwdata",
            default_scope_name="midasmv",
            default_sim_config_name="PVWindData",
            default_import_str=(
                "midas.modules.pwdata.simulator:PVWindDataSimulator"
            ),
            default_cmd_str="TODO",
            log=LOG,
        )

        self.models = {
            "PV": ["p_mw", "q_mvar"],
            "Wind": ["p_mw", "q_mvar"],
            "WindOffshore": ["p_mw", "q_mvar"],
        }

    def check_module_params(self, module_params):
        """Check the module params and provide default values."""

        module_params.setdefault("start_date", self.scenario.base.start_date)
        module_params.setdefault("data_path", self.scenario.base.data_path)
        module_params.setdefault("cos_phi", self.scenario.base.cos_phi)
        module_params.setdefault("interpolate", False)
        module_params.setdefault("noise_factor", 0.2)
        module_params.setdefault(
            "sgen_scaling", module_params.get("scaling", 1.0)
        )

        if self.scenario.base.no_rng:
            module_params["randomize_data"] = False
            module_params["randomize_cos_phi"] = False
        else:
            module_params.setdefault("randomize_data", False)
            module_params.setdefault("randomize_cos_phi", False)

    def check_sim_params(self, module_params):

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
        self.sim_params.setdefault(
            "noise_factor", module_params["noise_factor"]
        )
        self.sim_params.setdefault(
            "sgen_scaling",
            self.sim_params.get("scaling", module_params["sgen_scaling"]),
        )
        self.sim_params.setdefault("peak_mapping", dict())
        self.sim_params.setdefault("scale_mapping", dict())
        self.sim_params.setdefault("seed_max", self.scenario.base.seed_max)
        self.sim_params.setdefault("seed", self.scenario.create_seed())

        self.sim_params.setdefault(
            "filename", RuntimeConfig().data["generator_timeseries"][0]["name"]
        )

    def start_models(self):
        peak_key = "peak_mapping"
        scale_key = "scale_mapping"
        self.sim_params.setdefault(peak_key, self.create_default_mapping())
        self.sim_params.setdefault(scale_key, {})

        mapping = self.scenario.create_shared_mapping(
            self, self.sim_params["grid_name"], "sgen"
        )
        for map_key in [peak_key, scale_key]:
            for bus, entities in self.sim_params[map_key].items():
                mapping.setdefault(bus, list())
                for eidx, (model, scale) in enumerate(entities):
                    model_key = self.scenario.generate_model_key(
                        self, model, bus, eidx
                    )
                    scaling = scale * float(self.sim_params["sgen_scaling"])
                    if "peak" in map_key:
                        params = {"p_peak_mw": scaling}
                    else:
                        params = {"scaling": scaling}

                    full_id = self.start_model(model_key, model, params)
                    info = self.scenario.get_sim(self.sim_key).get_data_info()
                    mapping[bus].append(
                        (
                            model,
                            info[full_id.split(".")[-1]]["p_mwh_per_a"]
                            * scaling,
                        )
                    )

    def connect(self):
        peak_key = "peak_mapping"
        scale_key = "scale_mapping"
        attrs = ["p_mw", "q_mvar"]
        for mapping_key in [peak_key, scale_key]:

            for bus, entities in self.sim_params[mapping_key].items():
                for eidx, (model, _) in enumerate(entities):
                    model_key = self.scenario.generate_model_key(
                        self, model, bus, eidx
                    )
                    grid_entity_key = self.get_grid_entity("sgen", bus)
                    self.connect_entities(model_key, grid_entity_key, attrs)

    def connect_to_db(self):
        """Connect the models to db."""
        peak_key = "peak_mapping"
        scale_key = "scale_mapping"
        attrs = ["p_mw", "q_mvar"]
        db_key = self.scenario.find_first_model("store", "database")[0]

        for mapping_key in [peak_key, scale_key]:

            for bus, entities in self.sim_params[mapping_key].items():
                for eidx, (model, _) in enumerate(entities):
                    model_key = self.scenario.generate_model_key(
                        self, model, bus, eidx
                    )
                    self.connect_entities(model_key, db_key, attrs)

    def create_default_mapping(self):
        default_mapping = dict()
        # if self.sim_name == self.default_grid:
        #     default_mapping = {13: [["Wind", 1.0]]}

        return default_mapping

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

    def download(self, data_path, tmp_path, if_necessary, force):
        download_gen(data_path, tmp_path, if_necessary, force)

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
