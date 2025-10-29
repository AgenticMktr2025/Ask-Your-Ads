import httpx
import logging
from app.config import CONNEXIFY_API_URL, CONNEXIFY_BRAND_NAME
from .schemas import (
    OnboardingLinkRequest,
    OnboardingLinkResponse,
    ConnexifyClient,
    ConnectedAccount,
)


class ConnexifyAPIClient:
    def __init__(self, api_key: str, timeout: int = 30):
        if not api_key:
            raise ValueError("Connexify API key is required.")
        self.base_url = CONNEXIFY_API_URL
        self.brand_name = CONNEXIFY_BRAND_NAME
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            timeout=timeout,
        )

    async def create_onboarding_link(
        self, request: OnboardingLinkRequest
    ) -> OnboardingLinkResponse:
        try:
            response = await self.client.post("/api/data/links", json=request.dict())
            response.raise_for_status()
            return OnboardingLinkResponse(**response.json())
        except httpx.HTTPStatusError as e:
            logging.exception(f"HTTP error creating onboarding link: {e}")
            raise

    async def list_clients(self) -> list[ConnexifyClient]:
        try:
            response = await self.client.get("/api/data/clients")
            response.raise_for_status()
            response_data = response.json()
            return [ConnexifyClient(**c) for c in response_data.get("data", [])]
        except httpx.HTTPStatusError as e:
            logging.exception(f"HTTP error listing clients: {e}")
            raise

    async def get_connected_accounts(self, client_id: str) -> list[ConnectedAccount]:
        try:
            response = await self.client.get(f"/api/data/clients/{client_id}/accounts")
            response.raise_for_status()
            return [ConnectedAccount(**acc) for acc in response.json()]
        except httpx.HTTPStatusError as e:
            logging.exception(f"HTTP error getting connected accounts: {e}")
            raise

    async def close(self):
        await self.client.aclose()