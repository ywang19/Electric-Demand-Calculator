import reflex as rx
from app.state import DemandState
from app.components.header import header
from app.components.results import results_display
from app.components.parameters import parameters_section
from app.components.appliance_table import appliance_table
import reflex as rx
from app.state import DemandState
from app.components.header import header
from app.components.results import results_display
from app.components.parameters import parameters_section
from app.components.appliance_table import appliance_table
from app.components.appliance_form import appliance_form
from app.components.demand_chart import demand_chart
from app.components.edit_appliance_modal import edit_appliance_modal
from app.components.annual_demand_chart import annual_demand_chart


def index() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            header(),
            results_display(),
            demand_chart(),
            annual_demand_chart(),
            parameters_section(),
            appliance_table(),
            appliance_form(),
            edit_appliance_modal(),
            class_name="max-w-7xl mx-auto p-4 md:p-8 space-y-6",
        ),
        class_name="font-['Inter'] bg-gray-50 min-h-screen",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", crossorigin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index, title="Electric Demand Calculator")