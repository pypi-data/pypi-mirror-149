""" This module contains the Weather simulator."""
import logging
import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict

import mosaik_api
import numpy as np
import pandas as pd
from midas.util.dateformat import GER
from midas.util.logging import set_and_init_logger
from midas.util.print_format import mformat
from midas.util.runtime_config import RuntimeConfig

from .meta import META
from .model.current import WeatherCurrent
from .model.forecast import WeatherForecast
from .model.provider import WeatherData

LOG = logging.getLogger("midas.modules.weather.simulator")


class WeatherDataSimulator(mosaik_api.Simulator):
    """The Weather simulator."""

    def __init__(self):
        super().__init__(META)
        self.sid: str
        self.models: Dict[str, Any] = dict()
        self.step_size: int
        self.now_dt: datetime
        self.rng: np.random.RandomState
        self.randomize: bool
        self.interpolate: bool
        self.forecast_horizon_hours: float
        self.forecast_error: float
        self.seed_max: int
        self._time_synced: bool = False
        self._sim_time: int = 0

    def init(self, sid: str, **sim_params):
        """Called exactly ones after the simulator has been started.

        Parameters
        ----------
        sid : str
            Simulator ID for this simulator.
        start_date : str
            Start date as UTC ISO 8601 timestring such as
            '2019-01-01 00:00:00+0100'.
        step_size : int, optional
            Step size for this simulator. Defaults to 900.
        data_path : str, optional
            Path to the data folder. Defaults to the data folder in the
            midas root folder.
        filename : str, optional
            Name of the weather database. Defaults to
            *weather_bre2009-2019.hdf5*, the file that is created by
            the *midas.tools.weather_data.build_weather_data* function.
        interpolate : bool, optional
            If set to *True*, interpolation is enabled. Can be
            overwritten by model specific configuration.
        seed : int, optional
            A seed for the random number generator.
        randomize : bool, optional
            If set to *True*, randomization of data will be enabled.
            Otherwise, the data from the database is return unchanged.
            Can be overwritten by model specific configuration.

        Returns
        -------
        dict
            The meta dict (set by *mosaik_api.Simulator*).
        """

        self.sid = sid
        if "step_size" not in sim_params:
            LOG.debug(
                "Param *step_size* not provided. "
                "Using default step size of 900."
            )
        self.step_size = sim_params.get("step_size", 900)
        self.now_dt = datetime.strptime(
            sim_params["start_date"], GER
        ).astimezone(timezone.utc)
        self.rng = np.random.RandomState(sim_params.get("seed", None))
        self.seed_max = sim_params.get("seed_max", 1_000_000)
        self.interpolate = sim_params.get("interpolate", False)
        self.randomize = sim_params.get("randomize", False)
        self.forecast_horizon_hours = sim_params.get(
            "forecast_horizon_hours", self.step_size * 2 / 3_600
        )
        self.forecast_error = sim_params.get("forecast_error", 0.05)

        data_path = sim_params.get(
            "data_path",
            os.path.abspath(
                os.path.join(__file__, "..", "..", "..", "..", "..", "data")
            ),
        )
        filename = sim_params.get(
            "filename", RuntimeConfig().data["weather"][0]["name"]
        )
        filepath = os.path.join(data_path, filename)
        if not os.path.isfile(filepath):
            LOG.error(
                "File at '%s' does not exist. Will try to fix this...",
                filepath,
            )
            filepath = os.path.join(
                RuntimeConfig().paths["data_path"],
                RuntimeConfig().data["weather"][0]["name"],
            )
            if not os.path.isfile(filepath):
                LOG.critical(
                    "Unable to find data set at '%s'. Will die now!", filepath
                )
        self.wdata = WeatherData(filepath, self.rng.randint(1_000_000))

        return self.meta

    def create(self, num, model, **model_params):
        """Initialize the simulation model instance (entity).

        Parameters
        ----------
        num : int
            The number of models to create.
        model : str
            The name of the models to create. Must be present inside
            the simulator's meta.

        Returns
        -------
        list
            A list with information on the created entity.
        """
        entities = list()

        for _ in range(num):
            eid = f"{model}-{len(self.models)}"
            seed = self.rng.randint(self.seed_max)

            if model == "WeatherCurrent":
                self.models[eid] = WeatherCurrent(
                    wdata=self.wdata,
                    start_date=self.now_dt,
                    step_size=self.step_size,
                    interpolate=model_params.get("interpolate", False),
                    randomize=model_params.get("randomize", False),
                    seed=model_params.get("seed", seed),
                )

            elif model == "WeatherForecast":
                self.models[eid] = WeatherForecast(
                    wdata=self.wdata,
                    start_date=self.now_dt,
                    step_size=self.step_size,
                    interpolate=model_params.get("interpolate", False),
                    randomize=model_params.get("randomize", False),
                    seed=model_params.get("seed", seed),
                    forecast_horizon_hours=model_params.get(
                        "forecast_horizon_hours", self.forecast_horizon_hours
                    ),
                    forecast_error=model_params.get(
                        "forecast_error", self.forecast_error
                    ),
                )
            entities.append({"eid": eid, "type": model})

        return entities

    def step(self, time: int, inputs: Dict[str, Any], max_advance: int = 0):
        """Perform a simulation step.

        Parameters
        ----------
        time : int
            The current simulation step (by convention in seconds since
            simulation start.
        inputs : dict
            A *dict* containing inputs for entities of this simulator.

        Returns
        -------
        int
            The next step this simulator wants to be stepped.

        """
        self._time_synced = False
        self._sim_time = time
        if inputs:
            LOG.debug("At step %d received inputs %s", time, mformat(inputs))
            for attrs in inputs.values():
                if self._time_synced:
                    break
                for attr, src_ids in attrs.items():
                    if attr != "now":
                        continue
                    for val in src_ids.values():
                        self.now_dt = datetime.strptime(val, GER)
                        self._time_synced = True
                        break

        for model in self.models.values():
            model.step_size = self.step_size
            model.now_dt = self.now_dt
            model.step()

        if not self._time_synced:
            self.now_dt += timedelta(seconds=self.step_size)

        return time + self.step_size

    def get_data(self, outputs):
        """Return the requested output (if feasible).

        Parameters
        ----------
        outputs : dict
            A *dict* containing requested outputs of each entity.

        Returns
        -------
        dict
            A *dict* containing the values of the requested outputs.

        """

        data = dict()
        for eid, attrs in outputs.items():
            data[eid] = dict()
            model = eid.split("-")[0]
            for attr in attrs:
                if attr not in self.meta["models"][model]["attrs"]:
                    raise ValueError(f"Unknown output attribute {attr}")

                value = getattr(self.models[eid], attr)
                if isinstance(value, pd.DataFrame):
                    value = value.to_json()
                if not isinstance(value, str):
                    value = float(value)
                data[eid][attr] = value

        LOG.debug(
            "At step %d gathered ouputs %s", self._sim_time, mformat(data)
        )
        return data


if __name__ == "__main__":
    set_and_init_logger(
        0, "weather-logfile", "midas-weather.log", replace=True
    )
    LOG.info("Starting mosaik simulation...")
    mosaik_api.start_simulation(WeatherDataSimulator())
