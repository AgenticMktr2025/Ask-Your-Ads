import reflex as rx
from app.state import AppState, KPIRow
from app.components.sidebar import main_content


def kpi_table() -> rx.Component:
    return rx.el.div(
        rx.el.h1("Marketing KPIs", class_name="text-3xl font-bold text-gray-900 mb-6"),
        rx.cond(
            AppState.dashboard_configured,
            rx.cond(
                AppState.is_loading_kpis,
                rx.el.div(
                    rx.el.div(
                        class_name="h-8 bg-gray-200 rounded-md w-full animate-pulse mb-4"
                    ),
                    rx.el.div(
                        class_name="h-12 bg-gray-200 rounded-md w-full animate-pulse mb-2"
                    ),
                    rx.el.div(
                        class_name="h-12 bg-gray-200 rounded-md w-full animate-pulse mb-2"
                    ),
                    rx.el.div(
                        class_name="h-12 bg-gray-200 rounded-md w-full animate-pulse"
                    ),
                    class_name="w-full",
                ),
                rx.cond(
                    AppState.kpi_error != "",
                    rx.el.div(
                        rx.el.div(
                            rx.icon(
                                "flag_triangle_right", class_name="h-5 w-5 text-red-600"
                            ),
                            rx.el.h3(
                                "Could not load KPIs",
                                class_name="font-semibold text-red-800",
                            ),
                        ),
                        rx.el.p(
                            AppState.kpi_error, class_name="text-sm text-red-700 mt-1"
                        ),
                        rx.el.button(
                            "Try again",
                            on_click=AppState.load_summary,
                            class_name="mt-4 px-3 py-1.5 text-sm font-medium text-white bg-violet-600 rounded-md hover:bg-violet-700",
                        ),
                        class_name="p-4 bg-red-50 border border-red-200 rounded-lg",
                    ),
                    rx.el.div(
                        rx.el.p(
                            "Widget selection and data mapping workflow placeholder."
                        ),
                        class_name="border border-gray-200 rounded-lg overflow-hidden shadow-sm p-4",
                    ),
                ),
            ),
            rx.el.div(
                rx.el.h2(
                    "Configure Your Dashboard",
                    class_name="text-2xl font-bold text-gray-800 mb-4",
                ),
                rx.el.p(
                    "Select widgets and map your data sources to get started.",
                    class_name="text-gray-600 mb-6",
                ),
                rx.el.button(
                    "Configure Dashboard",
                    on_click=AppState.configure_dashboard,
                    class_name="px-6 py-2 text-sm font-medium text-white bg-violet-600 rounded-md hover:bg-violet-700",
                ),
                class_name="flex flex-col items-center justify-center text-center p-8 border-2 border-dashed border-gray-300 rounded-lg bg-gray-50",
            ),
        ),
    )


def dashboard() -> rx.Component:
    return main_content(kpi_table())