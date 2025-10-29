import reflex as rx
from app.state import AppState, ChatMessage
from app.components.sidebar import main_content


def chat_message_bubble(message: ChatMessage) -> rx.Component:
    is_user = message["role"] == "user"
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                rx.el.strong(rx.cond(is_user, "You", "Copilot")),
                class_name="text-xs font-semibold text-gray-600 mb-1",
            ),
            rx.el.p(message["content"], class_name="text-sm text-gray-800"),
            class_name=rx.cond(
                is_user,
                "bg-violet-100 text-gray-800 p-3 rounded-lg rounded-br-none",
                "bg-gray-100 text-gray-800 p-3 rounded-lg rounded-bl-none",
            ),
        ),
        class_name=rx.cond(is_user, "flex justify-end", "flex justify-start"),
    )


def chat_interface() -> rx.Component:
    return rx.el.div(
        rx.el.h1("AI Copilot", class_name="text-3xl font-bold text-gray-900 mb-6"),
        rx.el.div(
            rx.foreach(AppState.chat_messages, chat_message_bubble),
            rx.cond(
                AppState.is_loading_chat,
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "bot-message-square", class_name="h-5 w-5 animate-pulse"
                        ),
                        rx.el.p(
                            "Copilot is thinking...", class_name="text-sm text-gray-500"
                        ),
                        class_name="flex items-center gap-2 p-3",
                    )
                ),
                None,
            ),
            class_name="flex-1 overflow-y-auto p-4 space-y-4 border border-gray-200 rounded-lg shadow-sm mb-4 h-[65vh]",
        ),
        rx.cond(
            AppState.chat_error != "",
            rx.el.div(
                rx.icon("flag_triangle_right", class_name="h-6 w-6 text-red-500"),
                rx.el.p("Error:", class_name="font-semibold"),
                rx.el.p(AppState.chat_error),
                class_name="flex items-center gap-2 p-4 bg-red-50 border border-red-200 text-red-800 rounded-lg mb-4",
            ),
            None,
        ),
        rx.el.form(
            rx.el.input(
                placeholder="Ask a question about your performance...",
                name="question",
                class_name="flex-1 px-4 py-2 border border-gray-300 rounded-l-lg focus:outline-none focus:ring-2 focus:ring-violet-500",
                disabled=AppState.is_loading_chat,
            ),
            rx.el.button(
                rx.icon("arrow-up", class_name="h-5 w-5"),
                type="submit",
                class_name="bg-violet-600 text-white px-4 py-2 rounded-r-lg hover:bg-violet-700 disabled:bg-violet-300",
                disabled=AppState.is_loading_chat,
            ),
            on_submit=AppState.ask_copilot,
            reset_on_submit=True,
            class_name="flex",
        ),
        class_name="flex flex-col h-full",
    )


def copilot() -> rx.Component:
    return main_content(chat_interface())