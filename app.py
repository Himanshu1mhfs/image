from fastapi import FastAPI, Request
from fastapi.responses import Response
import pytracking
import io

app = FastAPI()

@app.get("/")
async def home():
    return {"message": "Welcome to the email tracking server!"}

@app.get("/favicon.ico")
async def favicon():
    return Response(status_code=204)

@app.get("/track")
async def track_email(request: Request):
    # Log the tracking event
    log_message = f"Email opened: ID=1, IP={request.client.host}, Time={request.headers.get('Date')}"
    print(log_message)  # Log the event to the terminal

    # Return a 1x1 transparent pixel
    pixel_byte_string, mime_type = pytracking.get_open_tracking_pixel()
    return Response(content=pixel_byte_string, media_type=mime_type)
