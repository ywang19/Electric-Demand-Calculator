import reflex as rx
from app.state import DemandState


def legend_item(text: str, color: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(class_name=f"w-3 h-3 rounded-sm {color}"),
        rx.el.span(text, class_name="text-sm text-gray-600"),
        class_name="flex items-center gap-2",
    )


def annual_demand_chart() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "Annual Forecasted Demand",
                class_name="text-lg font-semibold text-gray-800",
            ),
            rx.el.div(
                legend_item("Appliance Load", "bg-blue-500"),
                legend_item("PV Generation", "bg-green-500"),
                class_name="flex flex-wrap items-center gap-4",
            ),
            class_name="flex justify-between items-center mb-4",
        ),
        rx.recharts.line_chart(
            rx.recharts.cartesian_grid(stroke_dasharray="3 3", vertical=False),
            rx.recharts.graphing_tooltip(),
            rx.recharts.x_axis(data_key="day", allow_duplicats=False),
            rx.recharts.y_axis(
                rx.recharts.label(
                    value="Energy (kWh)", angle=-90, position="insideLeft"
                )
            ),
            rx.recharts.line(
                data_key="appliance_load_kwh",
                type_="monotone",
                stroke="#3b82f6",
                stroke_width=2,
                dot=False,
                name="Appliance Load",
            ),
            rx.recharts.line(
                data_key="pv_generation_kwh",
                type_="monotone",
                stroke="#22c55e",
                stroke_width=2,
                dot=False,
                name="PV Generation",
            ),
            data=DemandState.annual_demand_data,
            height=300,
            width="100%",
            margin={"top": 5, "right": 20, "left": 20, "bottom": 5},
        ),
        class_name="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm mt-6",
    )