from pydantic import BaseModel, Field
from typing import Literal


class OnboardingLinkRequest(BaseModel):
    client_name: str
    client_email: str
    permissions: list[str] = Field(default=["read"])


class OnboardingLinkResponse(BaseModel):
    onboarding_url: str
    expires_at: str


class ConnexifyClient(BaseModel):
    id: str
    name: str
    onboarding_status: Literal["pending", "completed", "expired"]


class ConnectedAccount(BaseModel):
    id: str
    platform: str
    display_name: str
    status: Literal["active", "disconnected", "error"]