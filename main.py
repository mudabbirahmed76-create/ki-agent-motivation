from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from openai import OpenAI
import os
import random

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class VideoRequest(BaseModel):
    amount: int
    language: str
    platforms: List[str]

MOTIVATION_TOPICS = [
    "strength", "discipline", "success", "never give up", "mindset",
    "growth", "courage", "ambition", "healing", "winning mentality",
    "self confidence", "overcoming fear", "patience", "focus"
]

@app.post("/create-motivation-videos")
def create_videos(request: VideoRequest):

    results = []

    for i in range(request.amount):

        # 1. Pick random topic
        topic = random.choice(MOTIVATION_TOPICS)

        # 2. Create motivational script
        script_prompt = (
            f"Create a powerful motivational video script in {request.language} "
            f"about the topic: {topic}. Make it emotional, cinematic, and 20 seconds long."
        )

        chat = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": script_prompt}]
        )

        script_text = chat.choices[0].message["content"]

        # 3. Create image for video
        image_prompt = f"Cinematic motivational scene representing: {topic}"

        img = client.images.generate(
            model="gpt-image-1",
            prompt=image_prompt,
            size="1024x1024"
        )

        image_base64 = img.data[0].b64_json

        # 4. Generate video
        video_prompt = (
            f"Create a motivational video with cinematic visuals and music. "
            f"Use this script:\n{script_text}"
        )

        video = client.videos.generate(
            model="gpt-4o-mini-vid",
            prompt=video_prompt,
            duration=15,
            size="1080x1920"
        )

        video_base64 = video.data[0].b64_json

        # 5. Append result for this video
        results.append({
            "topic": topic,
            "script": script_text,
            "image_base64": image_base64,
            "video_base64": video_base64,
            "platforms_ready": request.platforms
        })

    return {
        "status": "success",
        "videos_generated": len(results),
        "videos": results
    }
