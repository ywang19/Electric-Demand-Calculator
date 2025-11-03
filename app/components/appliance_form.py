import reflex as rx
from app.state import DemandState


def form_input(
    label: str,
    placeholder: str,
    value: rx.Var,
    on_change: rx.event.EventHandler,
    type: str = "text",
) -> rx.Component:
    return rx.el.div(
        rx.el.label(label, class_name="text-sm font-medium text-gray-700 mb-1 block"),
        rx.el.input(
            placeholder=placeholder,
            on_change=on_change,
            type=type,
            class_name="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition",
            default_value=value,
        ),
    )


def appliance_form() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Add New Appliance", class_name="text-lg font-semibold text-gray-800 mb-4"
        ),
        rx.el.form(
            rx.el.div(
                form_input(
                    "Appliance Name",
                    "e.g., Laptop",
                    DemandState.new_appliance_name,
                    DemandState.set_new_appliance_name,
                ),
                form_input(
                    "Peak Power (Watts)",
                    "e.g., 65",
                    DemandState.new_appliance_peak_power,
                    DemandState.set_new_appliance_peak_power,
                    "number",
                ),
                form_input(
                    "Quantity",
                    "e.g., 2",
                    DemandState.new_appliance_quantity,
                    DemandState.set_new_appliance_quantity,
                    "number",
                ),
                form_input(
                    "Start Hour (0-23)",
                    "e.g., 9",
                    DemandState.new_appliance_start_hour,
                    DemandState.set_new_appliance_start_hour,
                    "number",
                ),
                form_input(
                    "End Hour (0-24)",
                    "e.g., 17",
                    DemandState.new_appliance_end_hour,
                    DemandState.set_new_appliance_end_hour,
                    "number",
                ),
                rx.el.div(
                    rx.el.button(
                        rx.icon("plus", class_name="mr-2"),
                        "Add Appliance",
                        on_click=DemandState.add_appliance,
                        type="button",
                        class_name="w-full flex items-center justify-center bg-blue-600 text-white font-semibold py-2 px-4 rounded-lg shadow-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all duration-200",
                    ),
                    class_name="flex items-end",
                ),
                class_name="grid grid-cols-1 md:grid-cols-6 gap-4",
            ),
            reset_on_submit=True,
        ),
        class_name="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm mt-6",
    )