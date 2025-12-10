from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class VideoRequest(BaseModel):
    amount: int
    topic: str
    language: str
    platforms: List[str]

@app.post("/create-motivation-videos")
def create_videos(request: VideoRequest):
    return {
        "status": "received",
        "amount": request.amount,
        "topic": request.topic,
        "language": request.language,
        "platforms": request.platforms,
        "message": "AI server successfully reached! Video generation will start next."
    }
