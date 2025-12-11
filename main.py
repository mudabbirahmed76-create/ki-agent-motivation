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

    # 1. Create motivational script
    prompt = (
        f"Write a powerful, emotional motivational script in {request.language} "
        f"about the topic: {request.topic}. "
        f"Make it short, cinematic and highly inspiring."
    )

    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt
    )

    script_text = response.output[0].content[0].text

    # 2. Build final JSON response
    return {
        "status": "success",
        "script": script_text,
        "amount": request.amount,
        "platforms": request.platforms,
        "message": "AI server successfully reached!"
    }
