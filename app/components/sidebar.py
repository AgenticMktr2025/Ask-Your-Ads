import reflex as rx
from app.state import AppState


def nav_item(text: str, href: str, icon: str) -> rx.Component:
    is_active = rx.State.router.page.path == href
    return rx.el.a(
        rx.el.div(
            rx.icon(icon, class_name="h-5 w-5"),
            rx.el.span(text, class_name="font-medium"),
            class_name=rx.cond(
                is_active,
                "flex items-center gap-3 rounded-lg bg-violet-100 px-3 py-2 text-violet-700 transition-all",
                "flex items-center gap-3 rounded-lg px-3 py-2 text-gray-500 transition-all hover:text-gray-900",
            ),
        ),
        href=href,
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.a(
                rx.icon("bar-chart-3", class_name="h-8 w-8 text-violet-600"),
                rx.el.span(
                    "AskYourAds", class_name="text-xl font-semibold text-gray-800"
                ),
                class_name="flex items-center gap-2 font-semibold",
                href="/",
            ),
            class_name="flex h-16 items-center border-b px-6 shrink-0",
        ),
        rx.el.nav(
            nav_item("Dashboard", "/dashboard", "layout-dashboard"),
            nav_item("AI Copilot", "/copilot", "bot-message-square"),
            nav_item("Client Onboarding", "/onboarding", "users"),
            class_name="flex-1 overflow-auto py-4 px-4 flex flex-col gap-1",
        ),
        class_name="h-screen w-64 border-r bg-gray-50 flex flex-col fixed",
    )


def main_content(child: rx.Component) -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.main(child, class_name="flex-1 p-6 md:p-8 lg:p-10 ml-64"),
        class_name="min-h-screen bg-white font-['Inter']",
    )