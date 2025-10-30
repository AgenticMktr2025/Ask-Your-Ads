import reflex as rx
from app.state import AppState
from app.components.sidebar import main_content
from app.widgets.state import WidgetState, AvailableWidget, SelectedWidget


def widget_card(widget: AvailableWidget) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(widget.icon, class_name="h-8 w-8 text-violet-500"),
            class_name="mb-4",
        ),
        rx.el.h3(widget.name, class_name="font-semibold text-gray-800"),
        rx.el.p(widget.description, class_name="text-sm text-gray-500 mb-4"),
        rx.el.button(
            "Add Widget",
            on_click=lambda: WidgetState.add_widget(widget),
            class_name="w-full bg-violet-50 text-violet-700 py-1.5 rounded-md hover:bg-violet-100 text-sm font-medium",
        ),
        class_name="p-4 border border-gray-200 rounded-lg shadow-sm bg-white hover:shadow-md transition-shadow",
    )


def widget_selection_panel() -> rx.Component:
    return rx.el.div(
        rx.el.h2("Add Widgets", class_name="text-xl font-bold text-gray-900 mb-4"),
        rx.el.div(
            rx.foreach(WidgetState.available_widgets, widget_card),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4",
        ),
        class_name="p-6 border border-gray-200 rounded-lg bg-gray-50",
    )


def selected_widget_display(widget: SelectedWidget) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(widget.name, class_name="font-semibold text-gray-800"),
            rx.el.button(
                rx.icon("x", class_name="h-4 w-4"),
                on_click=lambda: WidgetState.remove_widget(widget.id),
                class_name="text-gray-400 hover:text-gray-600",
                variant="ghost",
            ),
            class_name="flex justify-between items-center mb-2 pb-2 border-b",
        ),
        rx.el.p("Widget content placeholder..."),
        class_name="p-4 border border-gray-200 rounded-lg shadow-sm bg-white min-h-[200px]",
    )


def configured_dashboard_view() -> rx.Component:
    return rx.el.div(
        rx.cond(
            WidgetState.selected_widgets.length() > 0,
            rx.el.div(
                rx.foreach(WidgetState.selected_widgets, selected_widget_display),
                class_name="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6 mb-8",
            ),
            rx.el.div(
                rx.el.p(
                    "Your dashboard is empty. Add some widgets to get started.",
                    class_name="text-gray-600",
                ),
                class_name="text-center py-16 border-2 border-dashed border-gray-300 rounded-lg bg-gray-50 mb-8",
            ),
        ),
        widget_selection_panel(),
    )


def dashboard_page_content() -> rx.Component:
    return rx.el.div(
        rx.el.h1("Dashboard", class_name="text-3xl font-bold text-gray-900 mb-6"),
        rx.cond(
            AppState.dashboard_configured,
            configured_dashboard_view(),
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
    return main_content(dashboard_page_content())