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
            f"Write a short, powerful motivational script in {request.language} "
            f"about the topic: {request.topic}. "
            f"Make it emotional, inspiring, and impactful."
        )

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        script_text = response.choices[0].message["content"]

        # 2. Generate an image
        image_prompt = f"Cinematic motivational image based on: {request.topic}"
        img = client.images.generate(
            model="gpt-image-1",
            prompt=image_prompt,
            size="1024x1024"
        )
        image_base64 = img.data[0].b64_json

        # 3. Generate a video
        video_prompt = (
            f"Create a cinematic motivational video using this script:\n{script_text}\n"
            f"Use cinematic music, dramatic visuals, and emotional tone."
        )

        video_response = client.videos.generate(
            model="gpt-4o-mini-vid",
            prompt=video_prompt,
            duration=12,
            size="1920x1080"
        )

        video_base64 = video_response.data[0].b64_json

        # 4. Final response
        return {
            "status": "success",
            "script": script_text,
            "image_base64": image_base64,
            "video_base64": video_base64,
            "platforms_ready": request.platforms,
            "message": "Motivational video successfully generated!"
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}
