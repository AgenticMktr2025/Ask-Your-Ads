import reflex as rx
import logging
from .schemas import ConnexifyClient, OnboardingLinkRequest
from app.config import CONNEXIFY_API_KEY


class OnboardingState(rx.State):
    clients: list[ConnexifyClient] = []
    onboarding_link: str = ""
    is_loading: bool = False
    error: str = ""

    async def _get_client(self):
        from .client import ConnexifyAPIClient

        if not CONNEXIFY_API_KEY:
            async with self:
                self.error = "Connexify API key is not configured."
            return None
        return ConnexifyAPIClient(api_key=CONNEXIFY_API_KEY)

    @rx.event(background=True)
    async def load_clients(self):
        async with self:
            self.is_loading = True
            self.error = ""
        try:
            client = await self._get_client()
            if client:
                clients_data = await client.list_clients()
                async with self:
                    self.clients = clients_data
                await client.close()
        except Exception as e:
            logging.exception("Error loading clients")
            async with self:
                self.error = f"Failed to load clients: {e}"
        finally:
            async with self:
                self.is_loading = False

    @rx.event(background=True)
    async def create_onboarding_link(self, form_data: dict):
        async with self:
            self.is_loading = True
            self.error = ""
            self.onboarding_link = ""
        try:
            client = await self._get_client()
            if client:
                request = OnboardingLinkRequest(
                    client_name=form_data["client_name"],
                    client_email=form_data["client_email"],
                )
                response = await client.create_onboarding_link(request)
                async with self:
                    self.onboarding_link = response.onboarding_url
                await client.close()
        except Exception as e:
            logging.exception("Error creating onboarding link")
            async with self:
                self.error = f"Failed to create link: {e}"
        finally:
            async with self:
                self.is_loading = False