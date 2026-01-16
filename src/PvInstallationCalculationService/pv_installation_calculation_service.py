# -*- coding: utf-8 -*-
from datetime import datetime
from esdl import esdl
import helics as h
from dots_infrastructure.DataClasses import EsdlId, HelicsCalculationInformation, PublicationDescription, SubscriptionDescription, TimeStepInformation, TimeRequestType
from dots_infrastructure.HelicsFederateHelpers import HelicsSimulationExecutor
from dots_infrastructure.Logger import LOGGER
from dots_infrastructure.CalculationServiceHelperFunctions import get_single_param_with_name
from esdl import EnergySystem

from PvInstallationCalculationService.pv_installation_calculation_service_base import PvInstallationCalculationServiceBase
from PvInstallationCalculationService.pv_installation_calculation_service_dataclasses import CurrentPvPowerProductionOutput, PredictSolarPowerOutput

class CalculationServicePVSystem(PvInstallationCalculationServiceBase):

    def init_calculation_service(self, energy_system: esdl.EnergySystem):
        LOGGER.info("init calculation service")
        self.surface_area: dict[EsdlId, float] = {}
        self.panel_efficiency: dict[EsdlId, float] = {}

        for esdl_id in self.simulator_configuration.esdl_ids:
            for obj in energy_system.eAllContents():
                if hasattr(obj, "id") and obj.id == esdl_id:
                    pvsystem = obj

            self.surface_area[esdl_id]      = pvsystem.surfaceArea
            self.panel_efficiency[esdl_id]  = pvsystem.panelEfficiency


    def predict_solar_power(self, param_dict : dict, simulation_time : datetime, time_step_number : TimeStepInformation, esdl_id : EsdlId, energy_system : EnergySystem):
        # Receive solar irradiance data from param_dict.
        solar_irradiance = get_single_param_with_name(param_dict, "solar_irradiance")
        surface_area = self.surface_area[esdl_id]
        panel_efficiency = self.panel_efficiency[esdl_id]

        assert surface_area > 0.0, "provide surface area with value bigger than 0"
        assert panel_efficiency > 0.0, "provide panel efficiency with value bigger than 0"

        solar_power = [panel_efficiency * surface_area * irr for irr in solar_irradiance]

        ret_val = PredictSolarPowerOutput(solar_power)

        return ret_val
    

    def current_pv_power_production(self, param_dict : dict, simulation_time : datetime, time_step_number : TimeStepInformation, esdl_id : EsdlId, energy_system : EnergySystem):
        solar_irradiance = get_single_param_with_name(param_dict, "current_solar_irradiance")

        surface_area = self.surface_area[esdl_id]
        panel_efficiency = self.panel_efficiency[esdl_id]

        assert surface_area > 0.0, "provide surface area with value bigger than 0"
        assert panel_efficiency > 0.0, "provide panel efficiency with value bigger than 0"

        solar_power = panel_efficiency * surface_area * solar_irradiance

        ret_val = CurrentPvPowerProductionOutput(solar_power)

        return ret_val

if __name__ == "__main__":
    helics_simulation_executor = CalculationServicePVSystem()
    helics_simulation_executor.start_simulation()
    helics_simulation_executor.stop_simulation()
