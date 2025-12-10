from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class VideoRequest(BaseModel):
    amount: int
    topic: str
    language: str
    platforms: list[str]

@app.post("/create-motivation-videos")
def create_videos(request: VideoRequest):
    # Platzhalter – später kommt hier die echte KI-Videogenerierung rein
    return {
        "status": "received",
        "amount": request.amount,
        "topic": request.topic,
        "message": "KI-Server wurde erfolgreich erreicht! Videoproduktion kommt als nächstes."
    }
