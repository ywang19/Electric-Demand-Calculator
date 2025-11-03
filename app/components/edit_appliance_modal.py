import reflex as rx
from app.state import DemandState


def modal_input(
    label: str, value: rx.Var, on_change: rx.event.EventHandler, type: str = "text"
) -> rx.Component:
    return rx.el.div(
        rx.el.label(label, class_name="text-sm font-medium text-gray-700"),
        rx.el.input(
            default_value=value,
            on_change=on_change,
            type=type,
            class_name="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm",
        ),
        class_name="w-full",
    )


def operating_hours_editor() -> rx.Component:
    return rx.el.div(
        rx.el.label("Operating Hours", class_name="text-sm font-medium text-gray-700"),
        rx.el.div(
            rx.foreach(
                DemandState.editing_appliance["operating_hours"],
                lambda op_hour, index: rx.el.div(
                    modal_input(
                        "Start Hour",
                        op_hour["start"].to_string(),
                        lambda val: DemandState.update_operating_hour(
                            index, "start", val
                        ),
                        type="number",
                    ),
                    modal_input(
                        "End Hour",
                        op_hour["end"].to_string(),
                        lambda val: DemandState.update_operating_hour(
                            index, "end", val
                        ),
                        type="number",
                    ),
                    rx.el.button(
                        rx.icon("trash-2", class_name="size-4"),
                        on_click=lambda: DemandState.remove_operating_hour(index),
                        class_name="mt-6 p-2 rounded-md text-gray-400 hover:text-red-500 hover:bg-red-50 transition-colors",
                    ),
                    class_name="flex items-center gap-2 mt-2",
                ),
            ),
            class_name="space-y-2 mt-2",
        ),
        rx.el.button(
            "Add Time Range",
            on_click=DemandState.add_operating_hour,
            class_name="mt-3 text-sm font-medium text-blue-600 hover:text-blue-800",
        ),
    )


def edit_appliance_modal() -> rx.Component:
    return rx.cond(
        DemandState.is_editing,
        rx.el.div(
            rx.el.div(
                class_name="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.h3(
                            "Edit Appliance",
                            class_name="text-lg font-medium leading-6 text-gray-900",
                        ),
                        rx.el.div(
                            rx.el.div(
                                modal_input(
                                    "Appliance Name",
                                    DemandState.editing_appliance["name"],
                                    lambda val: DemandState.update_editing_field(
                                        "name", val
                                    ),
                                ),
                                modal_input(
                                    "Peak Power (Watts)",
                                    DemandState.editing_appliance[
                                        "peak_power"
                                    ].to_string(),
                                    lambda val: DemandState.update_editing_field(
                                        "peak_power", val
                                    ),
                                    type="number",
                                ),
                                modal_input(
                                    "Quantity",
                                    DemandState.editing_appliance[
                                        "quantity"
                                    ].to_string(),
                                    lambda val: DemandState.update_editing_field(
                                        "quantity", val
                                    ),
                                    type="number",
                                ),
                                class_name="grid grid-cols-1 md:grid-cols-3 gap-4",
                            ),
                            operating_hours_editor(),
                            class_name="mt-4 space-y-4",
                        ),
                        class_name="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4",
                    ),
                    rx.el.div(
                        rx.el.button(
                            "Save Changes",
                            on_click=DemandState.save_edit,
                            class_name="inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-blue-600 text-base font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:ml-3 sm:w-auto sm:text-sm",
                        ),
                        rx.el.button(
                            "Cancel",
                            on_click=DemandState.cancel_edit,
                            class_name="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:mt-0 sm:w-auto sm:text-sm",
                        ),
                        class_name="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse",
                    ),
                    class_name="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full",
                ),
                class_name="fixed inset-0 z-10 overflow-y-auto flex items-center justify-center min-h-screen",
            ),
            class_name="relative z-10",
        ),
    )