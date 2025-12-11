from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from openai import OpenAI
import os
import random

app = FastAPI()

# Simple health check so Railway knows the app is running
@app.get("/")
def home():
    return {"status": "running"}

# OpenAI client (reads your key from Railway env variable OPENAI_API_KEY)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class VideoRequest(BaseModel):
    amount: int          # how many scripts you want
    language: str        # "en", "de", ...
    platforms: List[str] # ["youtube", "tiktok", "instagram"]


# Random motivation topics
MOTIVATION_TOPICS = [
    "strength",
    "discipline",
    "success",
    "never give up",
    "mindset",
    "growth",
    "courage",
    "ambition",
    "transformation",
    "winning mentality",
    "self-confidence",
    "overcoming fear",
    "patience",
    "focus",
]


@app.post("/create-motivation-videos")
def create_videos(request: VideoRequest):
    results = []

    try:
        for _ in range(request.amount):
            # 1. Pick random topic
            topic = random.choice(MOTIVATION_TOPICS)

            # 2. Create motivational script
            script_prompt = (
                f"Write a short motivational video script in {request.language}.\n"
                f"Topic: {topic}.\n"
                "Length: around 20–30 seconds of spoken text.\n"
                "Write only the voice-over text, with line breaks for natural pauses.\n"
                "Do NOT add scene descriptions or camera directions."
            )

            chat = client.chat.completions.create(
                model="gpt-4.1-mini",   # oder "gpt-4o-mini" falls dein Account das hat
                messages=[{"role": "user", "content": script_prompt}],
            )

            # IMPORTANT: use .message.content (no [\"content\"])
            script_text = chat.choices[0].message.content

            # 3. Create thumbnail image prompt
            image_prompt = (
                f"Cinematic motivational scene representing the topic '{topic}'. "
                "Vertical 9:16, high contrast, dramatic lighting, very inspiring."
            )

            # 4. Generate image (Base64)
            image = client.images.generate(
                model="gpt-image-1",
                prompt=image_prompt,
                size="1024x1024",
            )

            image_base64 = image.data[0].b64_json

            # 5. Collect result for this 'video'
            results.append(
                {
                    "topic": topic,
                    "script": script_text,
                    "image_prompt": image_prompt,
                    "image_base64": image_base64,
                    "platforms_ready": request.platforms,
                }
            )

        return {
            "status": "success",
            "videos_requested": request.amount,
            "videos_generated": len(results),
            "videos": results,
        }

    except Exception as e:
        # If something goes wrong, we return a clear error instead of 500 without info
        return {
            "status": "error",
            "message": str(e),
        }
