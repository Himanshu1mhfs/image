from fastapi import FastAPI, Request
from fastapi.responses import Response
import pytracking
import io
from datetime import datetime
import uuid
from fastapi import Query

app = FastAPI()

@app.get("/")
async def home():
    return {"message": "Welcome to the email tracking server!"}

@app.get("/favicon.ico")
async def favicon():
    return Response(status_code=204)

@app.get("/track")
async def track_email(request: Request, email: str = Query(...)):
    # Generate a unique ID for each request
    unique_id = str(uuid.uuid4())

    # Capture the current timestamp and store it as a list
    current_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
    time_list = [current_time]

    # Log the tracking event with the receiver's email
    log_message = (
        f"Email opened: ID={unique_id}, IP={request.client.host}, "
        f"Time={time_list}, Email={email}, Headers={request.headers}"
    )
    print(log_message)  # Log the event to the terminal

    # Return a 1x1 transparent pixel
    pixel_byte_string, mime_type = pytracking.get_open_tracking_pixel()
    return Response(content=pixel_byte_string, media_type=mime_type)
