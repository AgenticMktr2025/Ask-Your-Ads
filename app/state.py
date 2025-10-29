import reflex as rx
import httpx
import logging
from typing import TypedDict, Literal
from app.config import API_BACKEND_URL, TENANT_ID, CLIENT_NAME, DATE_RANGE_DEFAULT


class KPIRow(TypedDict):
    platform: str
    total_spend: float
    total_clicks: int
    total_conversions: int
    total_revenue: float


class ChatMessage(TypedDict):
    role: Literal["user", "assistant"]
    content: str


class AppState(rx.State):
    kpi_rows: list[KPIRow] = []
    chat_messages: list[ChatMessage] = []
    is_loading_kpis: bool = False
    is_loading_chat: bool = False
    kpi_error: str = ""
    chat_error: str = ""
    chat_input: str = ""
    dashboard_configured: bool = False

    @rx.event
    def configure_dashboard(self):
        self.dashboard_configured = True

    @rx.var
    def formatted_kpi_rows(self) -> list[dict[str, str]]:
        return [
            {
                "platform": row["platform"].replace("_", " ").title(),
                "total_spend": f"${row['total_spend']:.2f}",
                "total_clicks": str(row["total_clicks"]),
                "total_conversions": str(row["total_conversions"]),
                "total_revenue": f"${row['total_revenue']:.2f}",
            }
            for row in self.kpi_rows
        ]

    @rx.event(background=True)
    async def load_summary(self):
        async with self:
            self.is_loading_kpis = True
            self.kpi_error = ""
        try:
            params = {
                "tenant_id": TENANT_ID,
                "client_name": CLIENT_NAME,
                "date_range": DATE_RANGE_DEFAULT,
            }
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{API_BACKEND_URL}/metrics/summary", params=params
                )
                response.raise_for_status()
                data = response.json()
            async with self:
                self.kpi_rows = data
        except httpx.HTTPStatusError as e:
            logging.exception(f"HTTP error loading summary: {e}")
            async with self:
                self.kpi_error = f"API Error: {e.response.status_code}. Please ensure the api-backend service is running and accessible."
        except httpx.ConnectError as e:
            logging.exception(f"Connection error loading summary: {e}")
            async with self:
                self.kpi_error = "Connection Error: Cannot connect to the API backend. Is the service running?"
        except Exception as e:
            logging.exception(f"Error loading summary: {e}")
            async with self:
                self.kpi_error = f"An unexpected error occurred: {e}"
        finally:
            async with self:
                self.is_loading_kpis = False

    @rx.event(background=True)
    async def ask_copilot(self, form_data: dict):
        question = form_data.get("question", "").strip()
        if not question:
            return
        async with self:
            self.chat_messages.append({"role": "user", "content": question})
            self.is_loading_chat = True
            self.chat_error = ""
        try:
            from app.config import MISTRAL_API_KEY, LEMONADO_BEARER_TOKEN
            from app.mcp_server.client import LemonadoMCPClient

            if LEMONADO_BEARER_TOKEN:
                logging.info("Attempting to use Lemonado MCP client.")
                mcp_client = LemonadoMCPClient()
                try:
                    if await mcp_client.health_check():
                        logging.info(
                            f"MCP session established: {mcp_client.session_id}"
                        )
                        tool_response = await mcp_client.call_tool(
                            tool_name="list_objects", arguments={}
                        )
                        answer = f"MCP tool 'list_objects' executed. Result: {str(tool_response)}"
                        async with self:
                            self.chat_messages.append(
                                {"role": "assistant", "content": answer}
                            )
                        return
                    else:
                        logging.warning("MCP health check failed, falling back.")
                except Exception as e:
                    logging.exception(
                        "MCP tool call failed, falling back to other methods."
                    )
                finally:
                    await mcp_client.close()
            logging.info("Falling back to Mistral or API query.")
            if MISTRAL_API_KEY:
                try:
                    from app.mistral_client import query_mistral

                    answer = await query_mistral(question, self.kpi_rows)
                    async with self:
                        self.chat_messages.append(
                            {"role": "assistant", "content": answer}
                        )
                    return
                except Exception as e:
                    logging.exception(
                        "Mistral query failed, falling back to API backend."
                    )
            try:
                payload = {
                    "question": question,
                    "tenant_id": TENANT_ID,
                    "client_name": CLIENT_NAME,
                }
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        f"{API_BACKEND_URL}/ai/query", json=payload, timeout=60
                    )
                    response.raise_for_status()
                    ai_response = response.json()
                async with self:
                    self.chat_messages.append(
                        {
                            "role": "assistant",
                            "content": ai_response.get("answer", "No answer received."),
                        }
                    )
            except Exception as e:
                logging.exception("Final fallback to API backend failed.")
                async with self:
                    self.chat_error = "All AI services are currently unavailable. Please check your configuration and network."
                    self.chat_messages.append(
                        {
                            "role": "assistant",
                            "content": "I'm unable to process your request at the moment.",
                        }
                    )
        except httpx.HTTPStatusError as e:
            logging.exception(f"HTTP error asking copilot: {e}")
            async with self:
                self.chat_error = f"Failed to get response: {e.response.status_code}. Is the API backend running?"
        except Exception as e:
            logging.exception(f"Error asking copilot: {e}")
            async with self:
                self.chat_error = f"An unexpected error occurred: {str(e)}"
        finally:
            async with self:
                self.is_loading_chat = False