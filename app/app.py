import reflex as rx
from app.state import AppState
from app.pages.dashboard import dashboard
from app.pages.copilot import copilot
from app.pages.onboarding import onboarding
from app.components.sidebar import main_content
from app.connexify.state import OnboardingState


def index() -> rx.Component:
    return main_content(
        rx.el.div(
            rx.el.h1(
                "Welcome to AskYourAds",
                class_name="text-3xl font-bold text-gray-900 mb-2",
            ),
            rx.el.p(
                "Select a page from the sidebar to get started.",
                class_name="text-gray-600",
            ),
            class_name="flex flex-col items-center justify-center h-full text-center",
        )
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index, route="/")
app.add_page(dashboard, route="/dashboard")
app.add_page(copilot, route="/copilot")
app.add_page(onboarding, route="/onboarding", on_load=OnboardingState.load_clients)