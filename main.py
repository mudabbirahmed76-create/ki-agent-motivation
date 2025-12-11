from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from openai import OpenAI
import os

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class VideoRequest(BaseModel):
    amount: int
    topic: str
    language: str
    platforms: List[str]

@app.post("/create-motivation-videos")
def create_videos(request: VideoRequest):

    try:
        # 1. Generate script
        prompt = (
            f"Create a motivational script in {request.language} about: {request.topic}. "
            f"Make it short, powerful, emotional and engaging."
        )

        chat = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        script_text = chat.choices[0].message.content  # ✔ KORREKT

        # Return only the script for now
        return {
            "status": "success",
            "script": script_text,
            "platforms_ready": request.platforms
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
