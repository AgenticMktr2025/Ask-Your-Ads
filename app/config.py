import os
from dotenv import load_dotenv

load_dotenv()
API_BACKEND_URL = os.getenv("API_BACKEND_URL", "http://localhost:8000")
TENANT_ID = os.getenv("TENANT_ID", "default-tenant")
CLIENT_NAME = os.getenv("CLIENT_NAME", "default-client")
DATE_RANGE_DEFAULT = os.getenv("DATE_RANGE_DEFAULT", "last_30_days")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
LEMONADO_MCP_URL = os.getenv("LEMONADO_MCP_URL", "https://mcp.lemonado.io/mcp")
LEMONADO_BEARER_TOKEN = os.getenv("LEMONADO_BEARER_TOKEN")
CONNEXIFY_API_KEY = os.getenv("CONNEXIFY_API_KEY")
CONNEXIFY_API_URL = os.getenv("CONNEXIFY_API_URL", "https://www.connexify.io")
CONNEXIFY_WEBHOOK_SECRET = os.getenv("CONNEXIFY_WEBHOOK_SECRET")
CONNEXIFY_BRAND_NAME = os.getenv("CONNEXIFY_BRAND_NAME", "AskYourAds")