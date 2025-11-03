import reflex as rx


def header() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("bar-chart-2", class_name="size-8 text-blue-600"),
            rx.el.h1(
                "Electric Max Demand Calculator",
                class_name="text-2xl md:text-3xl font-bold text-gray-800",
            ),
            class_name="flex items-center gap-4",
        ),
        rx.el.p(
            "A simulation tool to estimate the maximum electrical demand for a given set of appliances and parameters.",
            class_name="text-gray-500 mt-2",
        ),
        class_name="mb-8",
    )