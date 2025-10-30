import reflex as rx
from typing import TypedDict
import uuid


class AvailableWidget(TypedDict):
    type: str
    name: str
    description: str
    icon: str


class SelectedWidget(AvailableWidget):
    id: str


class WidgetState(rx.State):
    available_widgets: list[AvailableWidget] = []
    selected_widgets: list[SelectedWidget] = []

    def _get_widget_id(self) -> str:
        return str(uuid.uuid4())

    @rx.event
    def load_available_widgets(self):
        self.available_widgets = [
            {
                "type": "kpi_summary",
                "name": "KPI Summary Card",
                "description": "Shows top-line metrics like Spend, ROAS, and Conversions.",
                "icon": "bar-chart-big",
            },
            {
                "type": "performance_chart",
                "name": "Performance Over Time",
                "description": "Line chart showing trends for key metrics over a selected date range.",
                "icon": "line-chart",
            },
            {
                "type": "platform_breakdown",
                "name": "Platform Breakdown",
                "description": "A table or pie chart comparing performance across ad platforms.",
                "icon": "pie-chart",
            },
            {
                "type": "top_campaigns",
                "name": "Top Campaigns",
                "description": "List of the best performing campaigns by a selected metric.",
                "icon": "trophy",
            },
        ]

    @rx.event
    def add_widget(self, widget: AvailableWidget):
        new_widget = SelectedWidget(**widget, id=self._get_widget_id())
        self.selected_widgets.append(new_widget)

    @rx.event
    def remove_widget(self, widget_id: str):
        self.selected_widgets = [
            w for w in self.selected_widgets if w["id"] != widget_id
        ]