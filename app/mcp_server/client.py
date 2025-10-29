import httpx
import logging
import json
from typing import Any
from app.config import LEMONADO_MCP_URL
from .auth import get_auth_headers
from .schemas import MCPTool, MCPResource


class LemonadoMCPClient:
    def __init__(self, timeout: int = 30):
        self.base_url = LEMONADO_MCP_URL
        self.client = httpx.AsyncClient(timeout=timeout, http2=True)
        self.session_id: str | None = None
        self.request_id_counter = 0

    async def _get_next_request_id(self) -> int:
        self.request_id_counter += 1
        return self.request_id_counter

    def _parse_sse_response(
        self, text: str
    ) -> dict[str, object] | list[dict[str, object]]:
        """Parse a Server-Sent Events (SSE) response to extract JSON data."""
        for line in text.splitlines():
            if line.startswith("data:"):
                try:
                    return json.loads(line[5:].strip())
                except json.JSONDecodeError as e:
                    logging.exception(f"Failed to parse SSE JSON: {e}")
                    raise ValueError(f"Invalid JSON in SSE response: {line[5:]}")
        raise ValueError("No 'data:' field found in SSE response.")

    async def health_check(self) -> bool:
        """Initialize the MCP session and check if it's successful."""
        if self.session_id:
            return True
        try:
            self.request_id_counter = 0
            payload = {
                "jsonrpc": "2.0",
                "id": await self._get_next_request_id(),
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"roots": {"listChanged": True}, "sampling": {}},
                    "clientInfo": {"name": "ask-your-ads", "version": "1.0.0"},
                },
            }
            response = await self.client.post(
                self.base_url, json=payload, headers=get_auth_headers()
            )
            response.raise_for_status()
            self.session_id = response.headers.get("mcp-session-id")
            if not self.session_id:
                raise ValueError("MCP session ID not found in response headers.")
            parsed_data = self._parse_sse_response(response.text)
            return "result" in parsed_data
        except (httpx.HTTPError, ValueError) as e:
            logging.exception(f"MCP health check (initialize) failed: {e}")
            self.session_id = None
            return False

    async def _make_jsonrpc_request(
        self, method: str, params: dict
    ) -> dict[str, object] | list[dict[str, object]]:
        """Helper to make a JSON-RPC request after session is initialized."""
        if not self.session_id:
            await self.health_check()
        if not self.session_id:
            raise ConnectionError("Failed to establish MCP session.")
        headers = get_auth_headers()
        headers["mcp-session-id"] = self.session_id
        payload = {
            "jsonrpc": "2.0",
            "id": await self._get_next_request_id(),
            "method": method,
            "params": params,
        }
        response = await self.client.post(self.base_url, json=payload, headers=headers)
        response.raise_for_status()
        data = self._parse_sse_response(response.text)
        if isinstance(data, dict) and "error" in data:
            raise ConnectionAbortedError(f"MCP Error: {data['error']}")
        if isinstance(data, dict):
            return data.get("result", {})
        return data

    async def list_resources(self) -> list[MCPResource]:
        """Fetch the list of available resources from the Lemonado MCP."""
        logging.warning(
            "The 'resources/list' method is not supported by the Lemonado MCP server."
        )
        return []

    async def call_tool(self, tool_name: str, arguments: dict[str, object]) -> object:
        """Invoke a specific tool on the Lemonado MCP."""
        params = {"name": tool_name, "arguments": arguments}
        return await self._make_jsonrpc_request(method="tools/call", params=params)

    async def close(self):
        """Close the underlying HTTP client session."""
        await self.client.aclose()