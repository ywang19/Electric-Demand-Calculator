import reflex as rx
from app.state import DemandState


def metric_card(
    icon: str, label: str, value: rx.Var, unit: str, color: str
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(tag=icon, class_name="size-6 text-gray-500"),
            class_name=f"p-3 rounded-full {color}",
        ),
        rx.el.div(
            rx.el.p(label, class_name="text-sm font-medium text-gray-500"),
            rx.el.div(
                rx.el.span(value, class_name="text-2xl font-bold text-gray-800"),
                rx.el.span(unit, class_name="text-lg font-medium text-gray-600 ml-1"),
                class_name="flex items-baseline",
            ),
        ),
        class_name="flex items-center gap-4 bg-white p-4 rounded-2xl border border-gray-100 shadow-sm",
    )


def results_display() -> rx.Component:
    return rx.el.div(
        metric_card(
            "dollar-sign",
            "Daily Electricity Charges",
            DemandState.daily_charges,
            "USD",
            "bg-teal-100",
        ),
        metric_card(
            "sun", "Peak PV Power", DemandState.peak_pv_power_kw, "kW", "bg-green-100"
        ),
        metric_card(
            "activity",
            "Net Maximum Demand",
            DemandState.maximum_demand_kw,
            "kW",
            "bg-blue-100",
        ),
        metric_card(
            "zap",
            "Grid Max Demand",
            DemandState.maximum_demand_kva,
            "kVA",
            "bg-purple-100",
        ),
        class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6",
    )