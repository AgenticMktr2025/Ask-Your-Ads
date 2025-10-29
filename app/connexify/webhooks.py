import hashlib
import hmac
import logging
from fastapi import Request, HTTPException, Header
from app.config import CONNEXIFY_WEBHOOK_SECRET


async def verify_signature(request: Request, x_connexify_signature: str = Header(...)):
    if not CONNEXIFY_WEBHOOK_SECRET:
        logging.error(
            "CONNEXIFY_WEBHOOK_SECRET is not set. Cannot verify webhook signature."
        )
        raise HTTPException(status_code=500, detail="Webhook secret not configured.")
    body = await request.body()
    expected_signature = hmac.new(
        CONNEXIFY_WEBHOOK_SECRET.encode(), body, hashlib.sha256
    ).hexdigest()
    if not hmac.compare_digest(expected_signature, x_connexify_signature):
        logging.warning("Invalid webhook signature received.")
        raise HTTPException(status_code=403, detail="Invalid signature.")