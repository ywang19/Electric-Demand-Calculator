import reflex as rx
from app.state import DemandState


def slider_input(
    label: str, default_value: rx.Var, on_change: rx.event.EventHandler, unit: str = "%"
) -> rx.Component:
    return rx.el.div(
        rx.el.label(label, class_name="text-sm font-medium text-gray-700 mb-2 block"),
        rx.el.div(
            rx.el.div(
                rx.el.div(class_name="absolute w-full h-2 bg-gray-200 rounded-lg"),
                rx.el.div(
                    style={"width": (default_value * 100).to_string() + "%"},
                    class_name="absolute h-2 bg-blue-600 rounded-lg",
                ),
                rx.el.input(
                    type="range",
                    min=0,
                    max=100,
                    default_value=(default_value * 100).to_string(),
                    on_change=lambda value: on_change([value]),
                    class_name="absolute w-full h-2 opacity-0 cursor-pointer",
                ),
                class_name="relative w-full h-2",
            ),
            rx.el.span(
                (default_value * 100).to_string() + unit,
                class_name="text-sm font-semibold text-blue-600 w-16 text-right",
            ),
            class_name="flex items-center gap-4",
        ),
        class_name="w-full",
    )


def pv_slider_input(
    label: str,
    default_value: rx.Var,
    on_change: rx.event.EventHandler,
    unit: str = "kWp",
) -> rx.Component:
    return rx.el.div(
        rx.el.label(label, class_name="text-sm font-medium text-gray-700 mb-2 block"),
        rx.el.div(
            rx.el.div(
                rx.el.div(class_name="absolute w-full h-2 bg-gray-200 rounded-lg"),
                rx.el.div(
                    style={"width": (default_value / 20 * 100).to_string() + "%"},
                    class_name="absolute h-2 bg-green-500 rounded-lg",
                ),
                rx.el.input(
                    type="range",
                    min=0,
                    max=20,
                    step=0.5,
                    default_value=default_value.to_string(),
                    on_change=lambda value: on_change([value]),
                    class_name="absolute w-full h-2 opacity-0 cursor-pointer",
                ),
                class_name="relative w-full h-2",
            ),
            rx.el.span(
                default_value.to_string() + f" {unit}",
                class_name="text-sm font-semibold text-green-600 w-20 text-right",
            ),
            class_name="flex items-center gap-4",
        ),
        class_name="w-full",
    )


def pv_toggle() -> rx.Component:
    return rx.el.div(
        rx.el.label("Enable PV System", class_name="text-sm font-medium text-gray-700"),
        rx.el.button(
            rx.el.span(
                class_name=rx.cond(
                    DemandState.pv_enabled,
                    "translate-x-5 bg-white",
                    "translate-x-0 bg-gray-300",
                )
                + " inline-block w-5 h-5 rounded-full transform transition-transform duration-200 ease-in-out"
            ),
            on_click=DemandState.toggle_pv_enabled,
            class_name=rx.cond(DemandState.pv_enabled, "bg-green-500", "bg-gray-200")
            + " relative inline-flex items-center h-6 rounded-full w-11 transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2",
        ),
        class_name="flex items-center justify-between",
    )


def bess_slider_input(
    label: str,
    default_value: rx.Var,
    on_change: rx.event.EventHandler,
    max_val: int,
    unit: str,
) -> rx.Component:
    return rx.el.div(
        rx.el.label(label, class_name="text-sm font-medium text-gray-700 mb-2 block"),
        rx.el.div(
            rx.el.div(
                rx.el.div(class_name="absolute w-full h-2 bg-gray-200 rounded-lg"),
                rx.el.div(
                    style={"width": (default_value / max_val * 100).to_string() + "%"},
                    class_name="absolute h-2 bg-orange-500 rounded-lg",
                ),
                rx.el.input(
                    type="range",
                    min=0,
                    max=max_val,
                    step=0.5,
                    default_value=default_value.to_string(),
                    on_change=lambda value: on_change([value]),
                    class_name="absolute w-full h-2 opacity-0 cursor-pointer",
                ),
                class_name="relative w-full h-2",
            ),
            rx.el.span(
                default_value.to_string() + f" {unit}",
                class_name="text-sm font-semibold text-orange-600 w-20 text-right",
            ),
            class_name="flex items-center gap-4",
        ),
        class_name="w-full",
    )


def bess_toggle() -> rx.Component:
    return rx.el.div(
        rx.el.label("Enable BESS", class_name="text-sm font-medium text-gray-700"),
        rx.el.button(
            rx.el.span(
                class_name=rx.cond(
                    DemandState.bess_enabled,
                    "translate-x-5 bg-white",
                    "translate-x-0 bg-gray-300",
                )
                + " inline-block w-5 h-5 rounded-full transform transition-transform duration-200 ease-in-out"
            ),
            on_click=DemandState.toggle_bess_enabled,
            class_name=rx.cond(DemandState.bess_enabled, "bg-orange-500", "bg-gray-200")
            + " relative inline-flex items-center h-6 rounded-full w-11 transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-orange-500 focus:ring-offset-2",
        ),
        class_name="flex items-center justify-between",
    )


def grid_slider_input(
    label: str,
    default_value: rx.Var,
    on_change: rx.event.EventHandler,
    max_val: int,
    unit: str,
) -> rx.Component:
    return rx.el.div(
        rx.el.label(label, class_name="text-sm font-medium text-gray-700 mb-2 block"),
        rx.el.div(
            rx.el.div(
                rx.el.div(class_name="absolute w-full h-2 bg-gray-200 rounded-lg"),
                rx.el.div(
                    style={"width": (default_value / max_val * 100).to_string() + "%"},
                    class_name="absolute h-2 bg-purple-500 rounded-lg",
                ),
                rx.el.input(
                    type="range",
                    min=0,
                    max=max_val,
                    step=1,
                    default_value=default_value.to_string(),
                    on_change=lambda value: on_change([value]),
                    class_name="absolute w-full h-2 opacity-0 cursor-pointer",
                ),
                class_name="relative w-full h-2",
            ),
            rx.el.span(
                default_value.to_string() + f" {unit}",
                class_name="text-sm font-semibold text-purple-600 w-20 text-right",
            ),
            class_name="flex items-center gap-4",
        ),
        class_name="w-full",
    )


def parameters_section() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Simulation Parameters",
            class_name="text-lg font-semibold text-gray-800 mb-4",
        ),
        rx.el.div(
            rx.el.div(
                slider_input(
                    "Load Factor", DemandState.load_factor, DemandState.set_load_factor
                ),
                slider_input(
                    "Power Factor",
                    DemandState.power_factor,
                    DemandState.set_power_factor,
                    "",
                ),
                class_name="space-y-4 p-4 border rounded-lg bg-gray-50/50",
            ),
            rx.el.div(
                grid_slider_input(
                    "Transformer Capacity",
                    DemandState.grid_capacity_kw,
                    DemandState.set_grid_capacity,
                    50,
                    "kW",
                ),
                class_name="space-y-4 p-4 border rounded-lg bg-gray-50/50",
            ),
            rx.el.div(
                pv_slider_input(
                    "PV Capacity",
                    DemandState.pv_capacity_kwp,
                    DemandState.set_pv_capacity,
                ),
                pv_toggle(),
                class_name="space-y-4 p-4 border rounded-lg bg-gray-50/50",
            ),
            rx.el.div(
                bess_slider_input(
                    "BESS Capacity",
                    DemandState.bess_capacity_kwh,
                    DemandState.set_bess_capacity,
                    20,
                    "kWh",
                ),
                bess_slider_input(
                    "BESS Power",
                    DemandState.bess_power_kw,
                    DemandState.set_bess_power,
                    10,
                    "kW",
                ),
                bess_toggle(),
                class_name="space-y-4 p-4 border rounded-lg bg-gray-50/50",
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6",
        ),
        class_name="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm mt-6",
    )