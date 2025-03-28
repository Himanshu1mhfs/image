import os
import requests
from flask import Flask, request, jsonify
from mistralai import Mistral

# Store API keys in environment variables for security
api_key = os.getenv("MISTRAL_API_KEY", "ikSxiFOa62gk856aw8wDLpBNU7BLegyU")
ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN", "EAASZCiWzUovMBO6Ts1uxbJpLQj8aYx4lZBLhPWIcBI8DH580Bui8cKRvzLyjjwpNhf4qfSUIo7aI5ZAdDykMligEeRxtr7sd4yFo3L53WG1kc1aiQCGMLOi3Nq2hTgapmw4Atp67ZC8ZBi3zHmSX7G8QC1OY7ZA6Pdb1LD6bFMuHoMgMP9znJOeILjuVSx5Pu3tQooMNZAvY8OtYqv5M229bR82")
PHONE_NUMBER_ID = "559338400603685"  # Your WhatsApp Phone Number ID from Meta

app = Flask(__name__)

VERIFY_TOKEN = "12345"
model = "open-mistral-7b"


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

    if "entry" in data:
        for entry in data["entry"]:
            for change in entry.get("changes", []):
                if "value" in change and "messages" in change["value"]:
                    for message in change["value"]["messages"]:
                        sender_id = message["from"]  # Sender's WhatsApp number
                        message_text = message.get("text", {}).get("body", "").strip()

                        print(f"New message from {sender_id}: {message_text}")

                        if message_text in ["Hi", "Hii", "Hello"]:
                            # Send a greeting template message
                            send_template_message(sender_id)
                        elif message_text == "Portfolio Report":
                            # Send Portfolio Link Message
                            send_whatsapp_message(sender_id, "https://inv.moneyhoney.co.in/#/investor-login")
                        else:
                            send_whatsapp_message(sender_id, "https://inv.moneyhoney.co.in/#/investor-login")

    return jsonify({"status": "success"}), 200  # Respond to WhatsApp API


def send_template_message(phone_number):
    """Send a WhatsApp template message via Meta API."""
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "template",
        "template": {
            "name": "portfolio_link1",  # Kept fixed as requested
            "language": {
                "code": "en"
            }
        }
    }

    response = requests.post(url, json=payload, headers=headers)
    print("WhatsApp Template API Response:", response.json())  # Log API response


def send_whatsapp_message(phone_number, message):
    """Send a normal WhatsApp text message via Meta API."""
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
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
    print("WhatsApp Text API Response:", response.json())  # Log API response


if __name__ == "__main__":
    app.run(debug=True)
