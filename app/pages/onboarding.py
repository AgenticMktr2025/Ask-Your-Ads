import reflex as rx
from app.components.sidebar import main_content
from app.connexify.state import OnboardingState
from app.connexify.schemas import ConnexifyClient


def client_card(client: ConnexifyClient) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(client.name, class_name="font-semibold text-gray-900"),
            rx.el.div(
                rx.el.span(client.onboarding_status.title()),
                class_name=rx.cond(
                    client.onboarding_status == "completed",
                    "px-2 py-1 text-xs font-medium text-green-700 bg-green-100 rounded-full",
                    "px-2 py-1 text-xs font-medium text-yellow-700 bg-yellow-100 rounded-full",
                ),
            ),
            class_name="flex items-center justify-between",
        ),
        class_name="p-4 border border-gray-200 rounded-lg shadow-sm",
    )


def onboarding_form() -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            "Create Onboarding Link", class_name="text-xl font-bold text-gray-900 mb-4"
        ),
        rx.el.form(
            rx.el.div(
                rx.el.label(
                    "Client Name",
                    class_name="block text-sm font-medium text-gray-700 mb-1",
                ),
                rx.el.input(
                    placeholder="Acme Corp",
                    name="client_name",
                    class_name="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-violet-500 focus:border-violet-500",
                    required=True,
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Client Email",
                    class_name="block text-sm font-medium text-gray-700 mb-1",
                ),
                rx.el.input(
                    placeholder="contact@acme.com",
                    name="client_email",
                    type="email",
                    class_name="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-violet-500 focus:border-violet-500",
                    required=True,
                ),
                class_name="mb-4",
            ),
            rx.el.button(
                "Generate Link",
                type="submit",
                is_loading=OnboardingState.is_loading,
                class_name="w-full bg-violet-600 text-white py-2 px-4 rounded-md hover:bg-violet-700 disabled:bg-violet-300",
            ),
            on_submit=OnboardingState.create_onboarding_link,
        ),
        rx.cond(
            OnboardingState.onboarding_link != "",
            rx.el.div(
                rx.el.p(
                    "Onboarding link created successfully:",
                    class_name="text-sm font-medium text-gray-700 mt-4 mb-2",
                ),
                rx.el.input(
                    default_value=OnboardingState.onboarding_link,
                    is_read_only=True,
                    class_name="w-full px-3 py-2 bg-gray-100 border border-gray-300 rounded-md",
                ),
                class_name="mt-4 p-4 border border-green-200 bg-green-50 rounded-lg",
            ),
            None,
        ),
        class_name="p-6 border border-gray-200 rounded-lg shadow-sm",
    )


def client_list() -> rx.Component:
    return rx.el.div(
        rx.el.h2("Clients", class_name="text-xl font-bold text-gray-900 mb-4"),
        rx.cond(
            OnboardingState.is_loading,
            rx.el.div(
                rx.el.p("Loading clients..."), class_name="text-center text-gray-500"
            ),
            rx.cond(
                OnboardingState.clients.length() > 0,
                rx.el.div(
                    rx.foreach(OnboardingState.clients, client_card),
                    class_name="space-y-3",
                ),
                rx.el.p("No clients found.", class_name="text-center text-gray-500"),
            ),
        ),
    )


def onboarding() -> rx.Component:
    return main_content(
        rx.el.div(
            rx.el.h1(
                "Client Onboarding", class_name="text-3xl font-bold text-gray-900 mb-6"
            ),
            rx.cond(
                OnboardingState.error != "",
                rx.el.div(
                    rx.icon("badge_alert", class_name="h-5 w-5 text-red-500 mr-2"),
                    rx.el.p(OnboardingState.error),
                    class_name="flex items-center p-4 mb-4 text-sm text-red-800 border border-red-300 rounded-lg bg-red-50",
                ),
                None,
            ),
            rx.el.div(
                onboarding_form(),
                client_list(),
                class_name="grid grid-cols-1 lg:grid-cols-2 gap-8",
            ),
            class_name="max-w-4xl mx-auto",
        )
    )