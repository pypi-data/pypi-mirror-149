"""MIDAS upgrade module for the weather data simulator."""
import logging

import pandas as pd
from midas.util.runtime_config import RuntimeConfig
from midas.util.upgrade_module import UpgradeModule

from .download import download_weather

LOG = logging.getLogger(__name__)


class WeatherDataModule(UpgradeModule):
    def __init__(self):
        super().__init__(
            module_name="weather",
            default_scope_name="bremen",
            default_sim_config_name="WeatherData",
            default_import_str=(
                "midas.modules.weather.simulator:WeatherDataSimulator"
            ),
            default_cmd_str="TODO",
            log=LOG,
        )

        attrs = [
            "t_air_deg_celsius",
            "day_avg_t_air_deg_celsius",
            "bh_w_per_m2",
            "dh_w_per_m2",
            # windspeed
            # wind direction
        ]
        self.models = {
            "WeatherCurrent": attrs,
            "WeatherForecast": [f"forecast_{attr}" for attr in attrs],
        }

    def check_module_params(self, module_params):
        """Check the module params and provide default values."""

        module_params.setdefault("start_date", self.scenario.base.start_date)
        module_params.setdefault("data_path", self.scenario.base.data_path)
        module_params.setdefault("interpolate", False)
        module_params.setdefault("noise_factor", 0.05)
        module_params.setdefault(
            "forecast_horizon_hours", self.scenario.base.forecast_horizon_hours
        )
        module_params.setdefault("forecast_error", 0.05)

        if self.scenario.base.no_rng:
            module_params["randomize"] = False
        else:
            module_params.setdefault("randomize", False)

    def check_sim_params(self, module_params):
        """Check the params for a certain simulator instance."""

        self.sim_params.setdefault("start_date", module_params["start_date"])
        self.sim_params.setdefault("data_path", module_params["data_path"])
        self.sim_params.setdefault("interpolate", module_params["interpolate"])
        self.sim_params.setdefault(
            "noise_factor", module_params["noise_factor"]
        )
        self.sim_params.setdefault(
            "forecast_horizon_hours", module_params["forecast_horizon_hours"]
        )
        self.sim_params.setdefault(
            "forecast_error", module_params["forecast_error"]
        )
        self.sim_params.setdefault("randomize", module_params["randomize"])
        self.sim_params.setdefault("seed_max", self.scenario.base.seed_max)
        self.sim_params.setdefault("seed", self.scenario.create_seed())
        self.sim_params.setdefault(
            "filename", RuntimeConfig().data["weather"][0]["name"]
        )

    def start_models(self):
        """Start models of a certain simulator."""
        mapping_key = "weather_mapping"
        if not self.sim_params.setdefault(
            mapping_key, self.create_default_mapping()
        ):
            # No mapping configured
            return

        for model, configs in self.sim_params[mapping_key].items():
            model_low = model.lower()

            for idx, config in enumerate(configs):
                model_key = self.scenario.generate_model_key(
                    self, model_low, idx
                )
                self.start_model(model_key, model, config)

    def connect(self):
        if self.sim_params["with_timesim"]:
            for model in self.models:
                if model not in self.sim_params["weather_mapping"]:
                    continue

                timesim, _ = self.scenario.find_first_model("timesim")
                for idx, _ in enumerate(
                    self.sim_params["weather_mapping"][model]
                ):
                    entity = self.scenario.generate_model_key(
                        self, model.lower(), idx
                    )
                    self.connect_entities(
                        timesim, entity, [("local_time", "now")]
                    )

    def connect_to_db(self):
        """Connect models to db."""
        mapping_key = "weather_mapping"
        db_key = self.scenario.find_first_model("store", "database")[0]

        for model, attrs in self.models.items():
            if model == "WeatherForecast":
                # TODO: add as soon as arrays/lists can be stored
                continue

            for idx, _ in enumerate(self.sim_params[mapping_key][model]):
                model_key = self.scenario.generate_model_key(
                    self, model.lower(), idx
                )
                self.connect_entities(model_key, db_key, attrs)

    def create_default_mapping(self):
        default_mapping = {}
        if not self.sim_params["weather_mapping"]:
            self.sim_params["weather_mapping"]["WeatherCurrent"] = [
                {
                    "interpolate": self.sim_params["interpolate"],
                    "randomize": self.sim_params["randomize"],
                }
            ]
        return default_mapping

    def download(self, data_path, tmp_path, if_necessary, force):
        download_weather(data_path, tmp_path, if_necessary, force)

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
