from fastapi import FastAPI, Request, HTTPException,Query
from fastapi.responses import JSONResponse
import hashlib
import hmac
import json
import os
from pydantic import BaseModel

# Your app's secret key from the App Dashboard
APP_SECRET = "2105b4996a04f3d70781a8173290056d"
VERIFY_TOKEN = "12345"  # The verify token you set in the App Dashboard

app = FastAPI()

# # Model to validate the incoming payload structure
# class WebhookNotification(BaseModel):
#     entry: list
#     object: str

@app.get("/webhook")
async def verify_webhook(
    hub_mode: str = Query(..., alias="hub.mode"),
    hub_challenge: int = Query(..., alias="hub.challenge"),
    hub_verify_token: str = Query(..., alias="hub.verify_token")
):
    # Verify the mode is 'subscribe'
    if hub_mode != "subscribe":
        raise HTTPException(status_code=403, detail="Invalid hub.mode")
    
    # Verify the verify token matches
    if hub_verify_token != VERIFY_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid verify token")
    
    # Return the challenge if verification is successful
    return hub_challenge

@app.post("/webhooks")
async def handle_event_notification(request: Request):
    """
    Handle incoming event notifications (e.g., changes to user photos).
    """
    # Get the payload from the request body
    payload = await request.json()
    
    # Get the signature from the headers
    signature = request.headers.get('X-Hub-Signature-256', '').replace('sha256=', '')

    # Validate the payload
    if not validate_payload(payload, signature):
        raise HTTPException(status_code=400, detail="Invalid payload signature")

    # Process the payload (e.g., logging, triggering further actions)
    # Here, we just print it for demonstration purposes
    print(json.dumps(payload, indent=2))

    # Acknowledge the event by responding with HTTP 200 OK
    return {"status": "success"}

# Example: To run the app, use the command:
# uvicorn main:app --reload
