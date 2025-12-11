from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from openai import OpenAI
import os

app = FastAPI()

# Load OpenAI key from Railway environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class VideoRequest(BaseModel):
    amount: int
    topic: str
    language: str
    platforms: List[str]

@app.post("/create-motivation-videos")
def create_videos(request: VideoRequest):

    # 1. Create motivational script
    chat = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": (
                    f"Create a short motivational script in {request.language} "
                    f"about {request.topic}. Make it emotional, powerful and inspiring."
                )
            }
        ]
    )
    script_text = chat.choices[0].message["content"]

    # 2. Generate motivational image
    image = client.images.generate(
        model="gpt-image-1",
        prompt=f"Cinematic motivational image about {request.topic}",
        size="1024x1024"
    )
    image_base64 = image.data[0].b64_json

    # 3. Generate Motivational video
    video = client.videos.generate(
        model="gpt-4o-mini",
        prompt=f"Create a cinematic motivational video using this script:\n{script_text}",
        duration=12
    )
    video_base64 = video.data[0].b64_json

    return {
        "status": "success",
        "script": script_text,
        "image_base64": image_base64,
        "video_base64": video_base64,
        "platforms_ready": request.platforms,
        "message": "AI server successfully generated your content."
    }
