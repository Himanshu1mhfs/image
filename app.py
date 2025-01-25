from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import hashlib
import hmac
import json
import os
from pydantic import BaseModel

# Your app's secret key from the App Dashboard
APP_SECRET = "EAAMlYUQ59ZBMBO8eJpZBh3LP31eTpGO1ZAJ2UYNeas5XSLkytF4hfOF8zFZC5kAMlAreHO8PFyKparRNTQOG9doVRs9HYZCVuYrfrGD42MQ7LxRZBsrkAvZCDs1a5t7nW3e6baygy0WDbWTmEM1kR7SToa5NN4brqXWFl1phMeJfgW8wvG9lHzTF1I2iuBMWJxMdZCLryZAifXrVbUG1ZCfhkcgraFhIkZD"
VERIFY_TOKEN = "meatyhamhock"  # The verify token you set in the App Dashboard

app = FastAPI()

# Helper function to validate the payload
def validate_payload(payload: dict, signature: str) -> bool:
    # Recreate the SHA256 signature using the payload and your app secret
    payload_str = json.dumps(payload, separators=(',', ':'))
    computed_signature = hmac.new(
        key=APP_SECRET.encode('utf-8'),
        msg=payload_str.encode('utf-8'),
        digestmod=hashlib.sha256
    ).hexdigest()

    # Compare the computed signature with the signature from the header
    return hmac.compare_digest(computed_signature, signature)

# Model to validate the incoming payload structure
class WebhookNotification(BaseModel):
    entry: list
    object: str

@app.get("/")
async def verify_webhook(hub_mode: str, hub_challenge: str, hub_verify_token: str):
    """
    Webhook verification endpoint. Respond to the verification request from the platform.
    """
    if hub_verify_token != VERIFY_TOKEN:
        raise HTTPException(status_code=400, detail="Invalid verify token")

    return JSONResponse(content={"hub.challenge": hub_challenge})

@app.post("/")
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
