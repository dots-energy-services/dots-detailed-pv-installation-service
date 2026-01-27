from dataclasses import dataclass
from typing import List

@dataclass
class PredictSolarPowerOutput:
    potential_active_power : List | None = None

@dataclass
class CurrentPvPowerProductionOutput:
    pv_active_power : float | None = None

