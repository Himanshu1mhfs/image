# Install required packages
# pip install flask requests

from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# Configuration (Replace with your credentials)
VERIFY_TOKEN = "12345"  # Set in WhatsApp Business API settings
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"  # From Facebook Developer Portal
API_VERSION = "v18.0"
PHONE_NUMBER_ID = "YOUR_PHONE_NUMBER_ID"

# Verification endpoint (GET)
@app.route('/webhook', methods=['GET'])
def verify_webhook():
    """
    WhatsApp will send a GET request to verify the webhook
    """
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')

    if mode and token:
        if mode == 'subscribe' and token == VERIFY_TOKEN:
            print("WEBHOOK VERIFIED")
            return challenge, 200
        else:
            return "Verification failed", 403
    return "Missing parameters", 400

# Main webhook endpoint (POST)
@app.route('/webhook', methods=['POST'])
def handle_webhook():
    """
    Handle incoming messages and events
    """
    data = request.get_json()
    print("Received webhook data:", json.dumps(data, indent=2))

    # Check if it's a message
    if 'object' in data and 'entry' in data:
        if data['object'] == 'whatsapp_business_account':
            try:
                for entry in data['entry']:
                    for change in entry.get('changes', []):
                        value = change.get('value')
                        if 'messages' in value:
                            message = value['messages'][0]
                            handle_message(message)
            except Exception as e:
                print(f"Error processing message: {str(e)}")
                return jsonify({'status': 'error'}), 500

    return jsonify({'status': 'success'}), 200

def handle_message(message):
    """
    Process individual messages
    """
    message_type = message['type']
    from_number = message['from']
    message_id = message['id']
    
    print(f"New {message_type} message from {from_number}")
    
    # Handle different message types
    if message_type == 'text':
        text_body = message['text']['body']
        print(f"Message content: {text_body}")
        send_reply(from_number, f"You said: {text_body}")
    elif message_type == 'image':
        image = message['image']
        # Handle image message
    elif message_type == 'document':
        document = message['document']
        # Handle document message
    # Add other message types as needed

def send_reply(to_number, message_text):
    """
    Send reply through WhatsApp API
    """
    url = f"https://graph.facebook.com/{API_VERSION}/{PHONE_NUMBER_ID}/messages"
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to_number,
        "type": "text",
        "text": {
            "body": message_text
        }
    }
    
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        print("Message sent successfully")
    else:
        print(f"Failed to send message: {response.text}")

if __name__ == '__main__':
    app.run(port=5000, debug=True)
