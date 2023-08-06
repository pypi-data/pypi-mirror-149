"""MIDAS scenario upgrade module.

This module adds a mosaikhdf database to the scenario.

"""
import logging

from midas.util.upgrade_module import UpgradeModule

LOG = logging.getLogger(__name__)


class TimeSimModule(UpgradeModule):
    def __init__(self):
        super().__init__(
            module_name="timesim",
            default_scope_name="timesim",
            default_sim_config_name="TimeSim",
            default_import_str=(
                "midas.modules.timesim.simulator:TimeSimulator"
            ),
            default_cmd_str=(
                "%(python)s -m midas.modules.timesim.simulator %(addr)s"
            ),
            log=LOG,
        )
        self.model = "Timegenerator"
        self.attrs = [
            "sin_day_time",
            "sin_week_time",
            "sin_year_time",
            "cos_day_time",
            "cos_week_time",
            "cos_year_time",
            "utc_time",
            "local_time",
        ]

    def check_module_params(self, module_params):
        """Check module params for this upgrade."""
        module_params.setdefault(self.default_scope_name, dict())
        module_params.setdefault("start_date", self.scenario.base.start_date)
        module_params.setdefault("time_schedule", None)

    def check_sim_params(self, module_params):
        self.sim_params.setdefault("start_date", module_params["start_date"])
        self.sim_params.setdefault(
            "time_schedule", module_params["time_schedule"]
        )

    def start_models(self):
        model_key = self.scenario.generate_model_key(self)

        self.start_model(model_key, self.model, {})

    def connect(self):
        pass

    def connect_to_db(self):
        db_key = self.scenario.find_first_model("store", "database")[0]
        model_key = self.scenario.generate_model_key(self)
        self.connect_entities(model_key, db_key, self.attrs)

    def get_sensor(self):
        timesim = self.scenario.get_sim(self.sim_key)

        self.scenario["sensors"].append(
            {
                "sensor_id": f"{timesim.full_id}.sin_day_time",
                "observation_space": (
                    "Box(low=0, high=1, shape=(1,), dtype=np.float32)"
                ),
            }
        )
        self.scenario["sensors"].append(
            {
                "sensor_id": f"{timesim.full_id}.sin_week_time",
                "observation_space": (
                    "Box(low=0, high=1, shape=(1,), dtype=np.float32)"
                ),
            }
        )
        self.scenario["sensors"].append(
            {
                "sensor_id": f"{timesim.full_id}.sin_year_time",
                "observation_space": (
                    "Box(low=0, high=1, shape=(1,), dtype=np.float32)"
                ),
            }
        )
        self.scenario["sensors"].append(
            {
                "sensor_id": f"{timesim.full_id}.cos_day_time",
                "observation_space": (
                    "Box(low=0, high=1, shape=(1,), dtype=np.float32)"
                ),
            }
        )
        self.scenario["sensors"].append(
            {
                "sensor_id": f"{timesim.full_id}.cos_week_time",
                "observation_space": (
                    "Box(low=0, high=1, shape=(1,), dtype=np.float32)"
                ),
            }
        )
        self.scenario["sensors"].append(
            {
                "sensor_id": f"{timesim.full_id}.cos_year_time",
                "observation_space": (
                    "Box(low=0, high=1, shape=(1,), dtype=np.float32)"
                ),
            }
        )
