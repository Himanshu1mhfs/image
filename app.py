from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI()

# Replace with your WhatsApp Business API credentials
WHATSAPP_API_URL = "https://graph.facebook.com/v13.0/your_phone_number_id/messages"
WHATSAPP_API_TOKEN = "EAAMlYUQ59ZBMBOZBWbJNAIp2gZCT7mp4pcGM9tHFATfpEGYZCZCxZAY3MPIjy9jyfAOZCGIMRugYcjjERRZCDudZAwc04a1ZAtVDmNwSQdP1HdGQKO4QHtnGN6hkZAmFMlig2lc2ZC1bbT8ZAbY0666Vfxl3Qw94ebjoYEEkZBCcESDkhDMdUjzhvX901zZAAELPAcfQQFP87L01GP4c2i5ZBMuZAMnKdYc4YktsZD"

# Replace with your LLM API endpoint and token
LLM_API_URL = "https://api.yourllmprovider.com/v1/completions"
LLM_API_TOKEN = "your_llm_api_token"

# Webhook verification token
VERIFY_TOKEN = "12345"

class WebhookRequest(BaseModel):
    entry: list

@app.get('/webhook')
async def verify_webhook(hub_mode: str, hub_challenge: str, hub_verify_token: str):
    if hub_mode == 'subscribe' and hub_verify_token == VERIFY_TOKEN:
        return hub_challenge
    else:
        raise HTTPException(status_code=403, detail="Verification token mismatch")

@app.post('/webhook')
async def handle_webhook(request: WebhookRequest):
    data = await request.json()
    message = data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
    sender = data['entry'][0]['changes'][0]['value']['contacts'][0]['wa_id']

    # Generate response using LLM
    response = generate_response(message)

    # Send response back to user
    send_message(sender, response)

    return {"status": "success"}

def generate_response(message: str) -> str:
    headers = {
        'Authorization': f'Bearer {LLM_API_TOKEN}',
        'Content-Type': 'application/json'
    }
    payload = {
        'model': 'your_model_name',
        'prompt': message,
        'max_tokens': 150
    }
    response = requests.post(LLM_API_URL, headers=headers, json=payload)
    response_json = response.json()
    return response_json['choices'][0]['text'].strip()

def send_message(phone_number: str, message: str):
    headers = {
        'Authorization': f'Bearer {WHATSAPP_API_TOKEN}',
        'Content-Type': 'application/json'
    }
    payload = {
        'messaging_product': 'whatsapp',
        'recipient_type': 'individual',
        'to': phone_number,
        'type': 'text',
        'text': {
            'body': message
        }
    }
    response = requests.post(WHATSAPP_API_URL, headers=headers, json=payload)
    return response.json()



