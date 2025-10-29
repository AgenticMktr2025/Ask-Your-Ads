import reflex as rx
from app.state import AppState, KPIRow
from app.components.sidebar import main_content


def kpi_table() -> rx.Component:
    return rx.el.div(
        rx.el.h1("Marketing KPIs", class_name="text-3xl font-bold text-gray-900 mb-6"),
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
                    rx.el.p(AppState.kpi_error, class_name="text-sm text-red-700 mt-1"),
                    rx.el.button(
                        "Try again",
                        on_click=AppState.load_summary,
                        class_name="mt-4 px-3 py-1.5 text-sm font-medium text-white bg-violet-600 rounded-md hover:bg-violet-700",
                    ),
                    class_name="p-4 bg-red-50 border border-red-200 rounded-lg",
                ),
                rx.el.div(
                    rx.el.table(
                        rx.el.thead(
                            rx.el.tr(
                                rx.el.th(
                                    "Platform",
                                    class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Spend",
                                    class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Clicks",
                                    class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Conversions",
                                    class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Revenue",
                                    class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                ),
                            )
                        ),
                        rx.el.tbody(
                            rx.foreach(
                                AppState.formatted_kpi_rows,
                                lambda row: rx.el.tr(
                                    rx.el.td(
                                        rx.el.span(row["platform"]),
                                        class_name="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900",
                                    ),
                                    rx.el.td(
                                        rx.el.span(row["total_spend"]),
                                        class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-600",
                                    ),
                                    rx.el.td(
                                        row["total_clicks"],
                                        class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-600",
                                    ),
                                    rx.el.td(
                                        row["total_conversions"],
                                        class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-600",
                                    ),
                                    rx.el.td(
                                        rx.el.span(row["total_revenue"]),
                                        class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-600",
                                    ),
                                    class_name="even:bg-gray-50",
                                ),
                            ),
                            class_name="bg-white divide-y divide-gray-200",
                        ),
                        class_name="min-w-full divide-y divide-gray-200 table-auto",
                    ),
                    class_name="border border-gray-200 rounded-lg overflow-hidden shadow-sm",
                ),
            ),
        ),
    )


def dashboard() -> rx.Component:
    return main_content(kpi_table())