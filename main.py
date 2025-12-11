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

    # 1. Generate motivational script
    prompt = (
        f"Create a motivational script in {request.language} about {request.topic}. "
        f"Make it short, powerful, emotional and suitable for social media videos."
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    script_text = response.choices[0].message["content"]

    # 2. Generate motivational image
    image_prompt = f"Cinematic motivational image based on {request.topic}"

    img = client.images.generate(
        model="gpt-image-1",
        prompt=image_prompt,
        size="1024x1024"
    )

    image_base64 = img.data[0].b64_json

    # 3. Generate motivational video
    video_prompt = (
        f"Create a motivational video using this script:\n{script_text}\n"
        "Use cinematic music, dynamic visuals, and emotional impact."
    )

    video_response = client.videos.generate(
        model="gpt-4o-mini-vid",
        prompt=video_prompt,
        duration=12,
        size="1920x1080"
    )

    video_base64 = video_response.data[0].b64_json

    # 4. Final Response
    return {
        "status": "success",
        "script": script_text,
        "image_base64": image_base64,
        "video_base64": video_base64,
        "amount": request.amount,
        "platforms_ready": request.platforms,
        "message": "Motivational video successfully generated."
    }
