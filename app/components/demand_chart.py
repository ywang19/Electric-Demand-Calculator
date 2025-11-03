import reflex as rx
from app.state import DemandState


def legend_item(text: str, color: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(class_name=f"w-3 h-3 rounded-sm {color}"),
        rx.el.span(text, class_name="text-sm text-gray-600"),
        class_name="flex items-center gap-2",
    )


def demand_chart() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "24-Hour Demand Profile",
                class_name="text-lg font-semibold text-gray-800",
            ),
            rx.el.div(
                legend_item("Gross Demand", "bg-blue-200"),
                legend_item("PV Generation", "bg-green-500"),
                legend_item("BESS Power", "bg-orange-500"),
                legend_item("Net Demand", "bg-blue-500"),
                class_name="flex flex-wrap items-center gap-4",
            ),
            class_name="flex justify-between items-center mb-4",
        ),
        rx.recharts.composed_chart(
            rx.recharts.cartesian_grid(stroke_dasharray="3 3", vertical=False),
            rx.recharts.graphing_tooltip(),
            rx.recharts.x_axis(data_key="hour"),
            rx.recharts.y_axis(
                rx.recharts.label(value="Demand (kW)", angle=-90, position="insideLeft")
            ),
            rx.recharts.area(
                data_key="gross_demand",
                type_="monotone",
                stroke="#a5b4fc",
                fill="#e0e7ff",
                stroke_width=2,
            ),
            rx.recharts.area(
                data_key="net_demand",
                type_="monotone",
                stroke="#3b82f6",
                fill="#60a5fa",
                stroke_width=2,
            ),
            rx.recharts.line(
                data_key="pv_power",
                type_="monotone",
                stroke="#22c55e",
                stroke_width=2,
                dot=False,
            ),
            rx.recharts.line(
                data_key="bess_power",
                type_="monotone",
                stroke="#f97316",
                stroke_width=2,
                dot=False,
            ),
            data=DemandState.demand_profile,
            height=300,
            width="100%",
            margin={"top": 5, "right": 20, "left": 20, "bottom": 5},
        ),
        class_name="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm mt-6",
    )