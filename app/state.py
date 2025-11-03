import reflex as rx
from typing import TypedDict, Optional
import logging
import copy

SOLAR_GENERATION_CURVE = [
    0,
    0,
    0,
    0,
    0,
    0,
    0.05,
    0.2,
    0.5,
    0.8,
    0.95,
    1.0,
    0.95,
    0.8,
    0.5,
    0.2,
    0.05,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
]


class OperatingHours(TypedDict):
    start: int
    end: int


class Appliance(TypedDict):
    name: str
    peak_power: float
    quantity: int
    operating_hours: list[OperatingHours]


class DemandState(rx.State):
    appliances: list[Appliance] = [
        {
            "name": "LED Lights",
            "peak_power": 10.0,
            "quantity": 15,
            "operating_hours": [{"start": 18, "end": 23}],
        },
        {
            "name": "Air Conditioner",
            "peak_power": 2500.0,
            "quantity": 2,
            "operating_hours": [{"start": 12, "end": 18}],
        },
        {
            "name": "Refrigerator",
            "peak_power": 200.0,
            "quantity": 1,
            "operating_hours": [{"start": 0, "end": 24}],
        },
        {
            "name": "Computer",
            "peak_power": 150.0,
            "quantity": 3,
            "operating_hours": [{"start": 9, "end": 17}],
        },
    ]
    new_appliance_name: str = ""
    new_appliance_peak_power: str = ""
    new_appliance_quantity: str = ""
    new_appliance_start_hour: str = "9"
    new_appliance_end_hour: str = "17"
    load_factor: float = 0.75
    power_factor: float = 0.95
    pv_capacity_kwp: float = 5.0
    pv_enabled: bool = True
    bess_enabled: bool = True
    bess_capacity_kwh: float = 13.5
    bess_power_kw: float = 5.0
    bess_efficiency: float = 0.9
    grid_capacity_kw: float = 10.0
    electricity_price_per_kwh: float = 0.2
    simulation_days: int = 365
    editing_appliance_index: Optional[int] = None
    editing_appliance: Optional[Appliance] = None

    @rx.var
    def is_editing(self) -> bool:
        return self.editing_appliance is not None

    @rx.var
    def annual_demand_data(self) -> list[dict]:
        import math

        daily_data = []
        daily_gross_demand_kwh = sum(self.hourly_gross_demand_profile) / 1000
        daily_pv_generation_kwh_base = sum(
            [factor * self.pv_capacity_kwp for factor in SOLAR_GENERATION_CURVE]
        )
        for day in range(self.simulation_days):
            seasonal_factor = 1 - 0.4 * math.cos(2 * math.pi * (day - 182.5) / 365)
            pv_generation = (
                daily_pv_generation_kwh_base * seasonal_factor if self.pv_enabled else 0
            )
            appliance_load = daily_gross_demand_kwh
            daily_data.append(
                {
                    "day": day + 1,
                    "pv_generation_kwh": round(pv_generation, 2),
                    "appliance_load_kwh": round(appliance_load, 2),
                }
            )
        return daily_data

    @rx.var
    def pv_generation_profile(self) -> list[float]:
        if not self.pv_enabled:
            return [0.0] * 24
        return [
            factor * self.pv_capacity_kwp * 1000 for factor in SOLAR_GENERATION_CURVE
        ]

    @rx.var
    def peak_pv_power_kw(self) -> float:
        if not self.pv_generation_profile:
            return 0.0
        return round(max(self.pv_generation_profile) / 1000, 2)

    @rx.var
    def hourly_gross_demand_profile(self) -> list[float]:
        profile = [0.0] * 24
        for hour in range(24):
            total_power_at_hour = 0
            for app in self.appliances:
                power = app["peak_power"] * app["quantity"]
                for op_hours in app["operating_hours"]:
                    start = op_hours["start"]
                    end = op_hours["end"]
                    is_on = False
                    if start < end:
                        is_on = start <= hour < end
                    else:
                        is_on = hour >= start or hour < end
                    if is_on:
                        total_power_at_hour += power
                        break
            profile[hour] = total_power_at_hour * self.load_factor
        return profile

    @rx.var
    def hourly_net_demand_profile(self) -> list[float]:
        if not self.bess_enabled:
            return [
                max(0, gross - pv)
                for gross, pv in zip(
                    self.hourly_gross_demand_profile, self.pv_generation_profile
                )
            ]
        return self.bess_simulation_results["final_net_demand"]

    @rx.var
    def bess_simulation_results(self) -> dict:
        demand_after_pv = [
            gross - pv
            for gross, pv in zip(
                self.hourly_gross_demand_profile, self.pv_generation_profile
            )
        ]
        if not self.bess_enabled:
            final_demand = [
                min(max(0, d), self.grid_capacity_kw * 1000) for d in demand_after_pv
            ]
            return {
                "bess_power_flow": [0.0] * 24,
                "bess_soc": [0.0] * 24,
                "final_net_demand": final_demand,
            }
        bess_power_w = self.bess_power_kw * 1000
        bess_capacity_wh = self.bess_capacity_kwh * 1000
        soc_wh = [bess_capacity_wh * 0.5] * 25
        bess_power_flow_w = [0.0] * 24
        avg_demand_after_pv = sum((max(0, d) for d in demand_after_pv)) / 24
        for _ in range(3):
            for h in range(24):
                demand_w = demand_after_pv[h]
                current_soc_wh = soc_wh[h]
                power_flow = 0.0
                if demand_w < 0:
                    surplus_w = -demand_w
                    charge_power_w = min(
                        surplus_w,
                        bess_power_w,
                        (bess_capacity_wh - current_soc_wh) / self.bess_efficiency,
                    )
                    power_flow = -charge_power_w
                elif demand_w > avg_demand_after_pv:
                    demand_to_shave_w = demand_w - avg_demand_after_pv
                    discharge_power_w = min(
                        demand_to_shave_w,
                        bess_power_w,
                        current_soc_wh * self.bess_efficiency,
                    )
                    power_flow = discharge_power_w
                bess_power_flow_w[h] = power_flow
                if power_flow < 0:
                    soc_change = -power_flow * self.bess_efficiency
                else:
                    soc_change = -power_flow
                soc_wh[h + 1] = max(
                    0, min(bess_capacity_wh, current_soc_wh + soc_change)
                )
        demand_before_grid = [d - p for d, p in zip(demand_after_pv, bess_power_flow_w)]
        final_net_demand = [
            min(max(0, d), self.grid_capacity_kw * 1000) for d in demand_before_grid
        ]
        return {
            "bess_power_flow": bess_power_flow_w,
            "bess_soc": [
                s / bess_capacity_wh if bess_capacity_wh > 0 else 0 for s in soc_wh[:24]
            ],
            "final_net_demand": final_net_demand,
        }

    @rx.var
    def demand_profile(self) -> list[dict]:
        bess_results = self.bess_simulation_results
        return [
            {
                "hour": f"{h:02d}:00",
                "gross_demand": round(self.hourly_gross_demand_profile[h] / 1000, 2),
                "pv_power": round(self.pv_generation_profile[h] / 1000, 2),
                "net_demand": round(bess_results["final_net_demand"][h] / 1000, 2),
                "bess_power": round(bess_results["bess_power_flow"][h] / 1000, 2),
            }
            for h in range(24)
        ]

    @rx.var
    def total_connected_load_kw(self) -> float:
        total_load = sum(
            (app["peak_power"] * app["quantity"] for app in self.appliances)
        )
        return round(total_load / 1000, 2)

    @rx.var
    def maximum_demand_kw(self) -> float:
        if not self.hourly_net_demand_profile:
            return 0.0
        return round(max(self.hourly_net_demand_profile) / 1000, 2)

    @rx.var
    def maximum_demand_kva(self) -> float:
        if self.power_factor == 0:
            return 0.0
        return round(self.maximum_demand_kw / self.power_factor, 2)

    @rx.var
    def daily_charges(self) -> float:
        total_kwh = sum(self.hourly_net_demand_profile) / 1000
        return round(total_kwh * self.electricity_price_per_kwh, 2)

    @rx.event
    def add_appliance(self):
        if (
            not self.new_appliance_name
            or not self.new_appliance_peak_power
            or (not self.new_appliance_quantity)
        ):
            return rx.toast.error("Please fill in all appliance fields.")
        try:
            peak_power = float(self.new_appliance_peak_power)
            quantity = int(self.new_appliance_quantity)
            start_hour = int(self.new_appliance_start_hour)
            end_hour = int(self.new_appliance_end_hour)
            if not (0 <= start_hour <= 23 and 0 <= end_hour <= 24):
                return rx.toast.error("Hour must be between 0 and 24.")
            new_app = {
                "name": self.new_appliance_name,
                "peak_power": peak_power,
                "quantity": quantity,
                "operating_hours": [{"start": start_hour, "end": end_hour}],
            }
            self.appliances.append(new_app)
            self.new_appliance_name = ""
            self.new_appliance_peak_power = ""
            self.new_appliance_quantity = ""
            self.new_appliance_start_hour = "9"
            self.new_appliance_end_hour = "17"
        except (ValueError, TypeError) as e:
            logging.exception(f"Error adding appliance: {e}")
            return rx.toast.error("Invalid input. Please check your values.")

    @rx.event
    def remove_appliance(self, index: int):
        if 0 <= index < len(self.appliances):
            self.appliances.pop(index)

    @rx.event
    def start_edit(self, index: int):
        self.editing_appliance_index = index
        self.editing_appliance = copy.deepcopy(self.appliances[index])

    @rx.event
    def cancel_edit(self):
        self.editing_appliance_index = None
        self.editing_appliance = None

    @rx.event
    def save_edit(self):
        if self.editing_appliance_index is not None and self.editing_appliance:
            self.appliances[self.editing_appliance_index] = self.editing_appliance
            self.cancel_edit()

    @rx.event
    def update_editing_field(self, field: str, value: str):
        if self.editing_appliance:
            if field in ["peak_power", "quantity"]:
                try:
                    self.editing_appliance[field] = float(value)
                except (ValueError, TypeError) as e:
                    logging.exception(f"Error updating editing field: {e}")
            else:
                self.editing_appliance[field] = value

    @rx.event
    def update_operating_hour(self, index: int, field: str, value: str):
        if self.editing_appliance and 0 <= index < len(
            self.editing_appliance["operating_hours"]
        ):
            try:
                self.editing_appliance["operating_hours"][index][field] = int(value)
            except (ValueError, TypeError) as e:
                logging.exception(f"Error updating operating hour: {e}")

    @rx.event
    def add_operating_hour(self):
        if self.editing_appliance:
            self.editing_appliance["operating_hours"].append({"start": 9, "end": 17})

    @rx.event
    def remove_operating_hour(self, index: int):
        if self.editing_appliance and 0 <= index < len(
            self.editing_appliance["operating_hours"]
        ):
            self.editing_appliance["operating_hours"].pop(index)

    @rx.event
    def set_load_factor(self, value: list[str]):
        self.load_factor = float(value[0]) / 100

    @rx.event
    def set_power_factor(self, value: list[str]):
        self.power_factor = float(value[0]) / 100

    @rx.event
    def set_pv_capacity(self, value: list[str]):
        self.pv_capacity_kwp = float(value[0])

    @rx.event
    def toggle_pv_enabled(self):
        self.pv_enabled = not self.pv_enabled

    @rx.event
    def set_bess_capacity(self, value: list[str]):
        self.bess_capacity_kwh = float(value[0])

    @rx.event
    def set_bess_power(self, value: list[str]):
        self.bess_power_kw = float(value[0])

    @rx.event
    def toggle_bess_enabled(self):
        self.bess_enabled = not self.bess_enabled

    @rx.event
    def set_grid_capacity(self, value: list[str]):
        self.grid_capacity_kw = float(value[0])