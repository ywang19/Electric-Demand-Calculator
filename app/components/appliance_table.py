import reflex as rx
from app.state import DemandState


def appliance_table() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Appliance List", class_name="text-lg font-semibold text-gray-800 mb-4"
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            "Appliance",
                            class_name="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Peak Power (W)",
                            class_name="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Qty",
                            class_name="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Operating Hours",
                            class_name="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Total Load (W)",
                            class_name="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Action",
                            class_name="px-4 py-3 text-right text-xs font-semibold text-gray-500 uppercase tracking-wider",
                        ),
                    ),
                    class_name="bg-gray-50",
                ),
                rx.el.tbody(
                    rx.foreach(
                        DemandState.appliances,
                        lambda appliance, index: rx.el.tr(
                            rx.el.td(
                                appliance["name"],
                                class_name="px-4 py-4 whitespace-nowrap text-sm font-medium text-gray-900",
                            ),
                            rx.el.td(
                                appliance["peak_power"].to_string(),
                                class_name="px-4 py-4 whitespace-nowrap text-sm text-gray-500",
                            ),
                            rx.el.td(
                                appliance["quantity"].to_string(),
                                class_name="px-4 py-4 whitespace-nowrap text-sm text-gray-500",
                            ),
                            rx.el.td(
                                rx.el.div(
                                    rx.foreach(
                                        appliance["operating_hours"],
                                        lambda hours: rx.el.span(
                                            f"{hours['start'].to_string()}:00 - {hours['end'].to_string()}:00",
                                            class_name="inline-block bg-gray-100 rounded-full px-2 py-0.5 text-xs font-medium text-gray-600 mr-1 mb-1",
                                        ),
                                    ),
                                    class_name="flex flex-wrap items-center",
                                ),
                                class_name="px-4 py-4 text-sm text-gray-500",
                            ),
                            rx.el.td(
                                (
                                    appliance["peak_power"] * appliance["quantity"]
                                ).to_string(),
                                class_name="px-4 py-4 whitespace-nowrap text-sm text-gray-500 font-semibold",
                            ),
                            rx.el.td(
                                rx.el.div(
                                    rx.el.button(
                                        rx.icon("share_2", class_name="size-4"),
                                        on_click=lambda: DemandState.start_edit(index),
                                        class_name="p-2 rounded-md text-gray-400 hover:text-blue-500 hover:bg-blue-50 transition-colors",
                                    ),
                                    rx.el.button(
                                        rx.icon("trash-2", class_name="size-4"),
                                        on_click=lambda: DemandState.remove_appliance(
                                            index
                                        ),
                                        class_name="p-2 rounded-md text-gray-400 hover:text-red-500 hover:bg-red-50 transition-colors",
                                    ),
                                    class_name="flex items-center justify-end",
                                ),
                                class_name="px-4 py-4 whitespace-nowrap text-sm text-gray-500 text-right",
                            ),
                            class_name="border-b border-gray-200 hover:bg-gray-50/50 transition-colors",
                        ),
                    ),
                    rx.cond(
                        DemandState.appliances.length() == 0,
                        rx.el.tr(
                            rx.el.td(
                                "No appliances added yet. Add one using the form below.",
                                col_span=6,
                                class_name="text-center py-10 text-gray-500 italic",
                            )
                        ),
                    ),
                ),
                class_name="min-w-full divide-y divide-gray-200",
            ),
            class_name="overflow-x-auto rounded-xl border border-gray-200",
        ),
        class_name="mt-6",
    )