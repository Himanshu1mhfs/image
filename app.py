from fastapi import FastAPI, Request, HTTPException
import hmac
import hashlib

app = FastAPI()

# Replace with your webhook verification token
VERIFICATION_TOKEN = "my_secure_verification_token_12345"

# Route to handle WhatsApp Webhook verification and incoming messages
@app.get("/")
async def verify_webhook(hub_mode: str, hub_challenge: str, hub_verify_token: str):
    """
    Verifies the webhook during setup.
    WhatsApp sends a GET request with these parameters.
    """
    if hub_mode == "subscribe" and hub_verify_token == VERIFICATION_TOKEN:
        return int(hub_challenge)  # Return the challenge to verify
    raise HTTPException(status_code=403, detail="Verification failed")

@app.post("/webhook")
async def receive_message(request: Request):
    """
    Handles incoming messages from WhatsApp.
    """
    try:
        # Get the request body as JSON
        body = await request.json()

        # (Optional) Verify the request using a signature (if provided by WhatsApp)
        signature = request.headers.get("X-Hub-Signature-256")
        if signature:
            verify_signature(request.body, signature)

        # Process the incoming message
        # Here, extract details like sender, message text, etc.
        message = body.get("entry", [])[0].get("changes", [])[0].get("value", {}).get("messages", [])[0]

        if message:
            sender = message["from"]
            text = message["text"]["body"]
            print(f"Message from {sender}: {text}")

        return {"status": "Message received"}

    except Exception as e:
        print(f"Error processing message: {e}")
        raise HTTPException(status_code=400, detail="Invalid request format")


def verify_signature(request_body, signature):
    """
    Verifies the request signature using your app's secret.
    """
    app_secret = "EAAMlYUQ59ZBMBO8eJpZBh3LP31eTpGO1ZAJ2UYNeas5XSLkytF4hfOF8zFZC5kAMlAreHO8PFyKparRNTQOG9doVRs9HYZCVuYrfrGD42MQ7LxRZBsrkAvZCDs1a5t7nW3e6baygy0WDbWTmEM1kR7SToa5NN4brqXWFl1phMeJfgW8wvG9lHzTF1I2iuBMWJxMdZCLryZAifXrVbUG1ZCfhkcgraFhIkZD"  # Replace with your App Secret
    expected_signature = hmac.new(
        app_secret.encode(),
        request_body,
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(expected_signature, signature.split("=")[-1]):
        raise HTTPException(status_code=403, detail="Invalid signature")


# Run the app using `uvicorn filename:app --reload`
