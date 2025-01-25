from fastapi import FastAPI, HTTPException, Query, Request
import hmac
import hashlib
import logging

app = FastAPI()

# Replace with your verification token
VERIFICATION_TOKEN = "my_secure_verification_token_12345"
APP_SECRET = "EAAMlYUQ59ZBMBO8eJpZBh3LP31eTpGO1ZAJ2UYNeas5XSLkytF4hfOF8zFZC5kAMlAreHO8PFyKparRNTQOG9doVRs9HYZCVuYrfrGD42MQ7LxRZBsrkAvZCDs1a5t7nW3e6baygy0WDbWTmEM1kR7SToa5NN4brqXWFl1phMeJfgW8wvG9lHzTF1I2iuBMWJxMdZCLryZAifXrVbUG1ZCfhkcgraFhIkZD"  # Replace with your App Secret from WhatsApp

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.get("/")
async def verify_webhook(
    hub_mode: str = Query(None),
    hub_challenge: str = Query(None),
    hub_verify_token: str = Query(None),
):
    """
    Verifies the webhook during setup.
    """
    logging.info(
        f"Received verification request: mode={hub_mode}, challenge={hub_challenge}, token={hub_verify_token}"
    )
    
    if hub_mode == "subscribe" and hub_verify_token == VERIFICATION_TOKEN:
        # Respond with the hub_challenge to complete the verification
        return int(hub_challenge) if hub_challenge.isdigit() else hub_challenge
    raise HTTPException(status_code=403, detail="Verification failed")


@app.post("/webhook")
async def receive_message(request: Request):
    """
    Handles incoming messages from WhatsApp.
    """
    try:
        # Get the request body as JSON
        body = await request.body()
        json_body = await request.json()

        # (Optional) Verify the request signature if provided by WhatsApp
        signature = request.headers.get("X-Hub-Signature-256")
        if signature:
            verify_signature(body, signature)

        # Process the incoming message
        entry = json_body.get("entry", [])[0]
        changes = entry.get("changes", [])[0]
        value = changes.get("value", {})
        message = value.get("messages", [])[0]

        if message:
            sender = message["from"]
            text = message["text"]["body"]
            logging.info(f"Message received from {sender}: {text}")
        else:
            logging.warning("No message found in the webhook payload.")

        return {"status": "Message received"}
    except Exception as e:
        logging.error(f"Error processing message: {e}")
        raise HTTPException(status_code=400, detail="Invalid request format")


def verify_signature(request_body: bytes, signature: str):
    """
    Verifies the request signature using your app's secret.
    """
    try:
        expected_signature = hmac.new(
            APP_SECRET.encode(),
            request_body,
            hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(expected_signature, signature.split("=")[-1]):
            raise HTTPException(status_code=403, detail="Invalid signature")
    except Exception as e:
        logging.error(f"Signature verification failed: {e}")
        raise HTTPException(status_code=403, detail="Signature verification error")
