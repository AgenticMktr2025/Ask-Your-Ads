import reflex as rx
import logging
from fastapi import FastAPI, Request, Depends, HTTPException
from app.connexify.webhooks import verify_signature
from pydantic import BaseModel
from typing import Literal


class WebhookPayload(BaseModel):
    event: str
    data: dict


async def connexify_webhook_handler(
    payload: WebhookPayload,
    request: Request,
    signature: str = Depends(verify_signature),
):
    """
    Handle incoming webhooks from Connexify.
    The signature is verified by the `verify_signature` dependency.
    """
    logging.info(
        f"Received Connexify webhook. Event: {payload.event}, Client ID: {payload.data.get('client_id')}"
    )
    if payload.event == "account.connected":
        logging.info(
            f"Account connected for client: {payload.data.get('client_id')}. Triggering sync."
        )
    elif payload.event == "onboarding.completed":
        logging.info(
            f"Onboarding completed for client: {payload.data.get('client_id')}."
        )
    else:
        logging.warning(f"Received unhandled Connexify event type: {payload.event}")
    return {"status": "ok", "event_received": payload.event}


api = FastAPI()
api.add_api_route(
    "/api/webhooks/connexify",
    endpoint=connexify_webhook_handler,
    methods=["POST"],
    name="connexify_webhook",
)