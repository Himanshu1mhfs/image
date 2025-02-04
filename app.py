import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

VERIFY_TOKEN = "12345"
ACCESS_TOKEN = "EAAMlYUQ59ZBMBOykcLV3lf5a5xwgPcxZBT9jiEWwJDmIBvnfK2H0YHOhON9JuA1TTlWXnWxErNuBksu3KP0aNcXeFZB1llg0W6JILslbGkoy59xHqVj2ufi48lXw6C8X8dMSbBZA0HecoFWdeDOhVawN7ZBrGHPZC7bYFFaj3AZCbw3QXpnsSHZA4xXruRL1KmlXynBuzUFSPsxPWC2cnYRNkDqtoJEZD"  # Store in environment variable

@app.route("/", methods=["GET"])
def webhook_verify():
    """Verify webhook for WhatsApp API."""
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200  # Meta (Facebook) needs this response
    return "Verification failed", 403

@app.route("/", methods=["POST"])
def receive_message():
    """Handle incoming WhatsApp messages."""
    data = request.get_json()
    print("Received webhook data:", data)  # Log the data for debugging

    # Process incoming messages
    if "entry" in data:
        for entry in data["entry"]:
            for change in entry.get("changes", []):
                if "value" in change and "messages" in change["value"]:
                    for message in change["value"]["messages"]:
                        sender_id = message["from"]  # Sender's WhatsApp number
                        message_text = message.get("text", {}).get("body", "")

                        print(f"New message from {sender_id}: {message_text}")

                        # Optional: Auto-reply to the message
                        send_whatsapp_message(sender_id, "Hello! This is an automated response.")

    return jsonify({"status": "success"}), 200  # Respond to WhatsApp API

def send_whatsapp_message(phone_number, message):
    """Send a WhatsApp message using Meta API."""
    url = "https://graph.facebook.com/v18.0/YOUR_PHONE_NUMBER_ID/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "text": {"body": message}
    }

    response = requests.post(url, json=payload, headers=headers)
    print("WhatsApp API Response:", response.json())  # Log API response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

