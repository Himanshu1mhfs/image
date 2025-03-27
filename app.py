import os
import requests
from flask import Flask, request, jsonify
from mistralai import Mistral
api_key = "ikSxiFOa62gk856aw8wDLpBNU7BLegyU"
model = "open-mistral-7b"

app = Flask(__name__)

VERIFY_TOKEN = "12345"
ACCESS_TOKEN = "EAASZCiWzUovMBO2qZA7BqHtRlmpgcU4moO1sqZCJHSgyYbzBFkCiJdSA7kNItB1dvSRHlUQMrQIsyk7VGcorIWSnKSgqkAKAHY7pKFG8FedD1wNqrHzehXOW1LimY672FDXjcX7aUWRwn5eck6t2ZCNHpdUShqX81MQ48dLV0dcyvrGp3XlZBnXwkqgFLz5ZC6Y4bZCDpFVO9Q8tycZD"  # Store in environment variable

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
                        # client = Mistral(api_key=api_key)
                        # chat_response = client.chat.complete(
                        #     model=model,
                        #     messages=[
                        #         {"role": "system", "content": "You are MHFS, a friendly chatbot that provides helpful and engaging information."},
                        #         {"role": "user", "content":message_text}
                        #     ]
                        # )
                
  
                        # Optional: Auto-reply to the message
                        send_whatsapp_message(sender_id, "Hii")

    return jsonify({"status": "success"}), 200  # Respond to WhatsApp API

def send_whatsapp_message(phone_number, message):
    """Send a WhatsApp message using Meta API."""
    url = "https://graph.facebook.com/v18.0/559338400603685/messages"
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
    app.run(debug=True)

