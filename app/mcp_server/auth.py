import httpx
from app.config import LEMONADO_BEARER_TOKEN


def get_auth_headers() -> dict[str, str]:
    """Get authentication headers for Lemonado MCP."""
    headers = {
        "Accept": "application/json, text/event-stream",
        "Content-Type": "application/json",
    }
    if LEMONADO_BEARER_TOKEN:
        headers["Authorization"] = f"Bearer {LEMONADO_BEARER_TOKEN}"
    return headers


async def authenticate_client(client: httpx.AsyncClient):
    """Placeholder for more complex authentication flows like OAuth."""
    pass