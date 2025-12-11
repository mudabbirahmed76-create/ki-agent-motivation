from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from openai import OpenAI
import os
import random

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ----------- Request Model -----------
class VideoRequest(BaseModel):
    amount: int
    language: str
    platforms: List[str]


# ----------- Helper: Generate random topic -----------
def get_random_topic():
    topics = [
        "motivation", "success", "discipline", "confidence", "focus",
        "mental toughness", "growth mindset", "overcoming fear",
        "never giving up", "self improvement", "work ethic"
    ]
    return random.choice(topics)


# ----------- Main Endpoint -----------
@app.post("/create-motivation-videos")
def create_videos(request: VideoRequest):

    try:
        videos_output = []

        for _ in range(request.amount):

            # 1) Generate a random topic
            topic = get_random_topic()

            # 2) Generate a motivational script
            script_prompt = (
                f"Create a short, powerful motivational speech in {request.language} "
                f"about the topic '{topic}'. Make it inspiring and emotional."
            )

            script_response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": script_prompt}]
            )

            script_text = script_response.choices[0].message["content"]

            # 3) Generate a cinematic video based on the script
            video_prompt = (
                f"Create a cinematic motivational video using this script:\n{script_text}\n"
                "Use inspiring visuals and emotional style."
            )

            video_response = client.videos.generate(
                model="gpt-4o-mini-vid",
                prompt=video_prompt,
                duration=12,
                size="1080x1920"
            )

            video_base64 = video_response.data[0].b64_json

            # Save each video result
            videos_output.append({
                "topic": topic,
                "script": script_text,
                "video_base64": video_base64
            })

        # Final JSON response to n8n
        return {
            "status": "success",
            "videos_generated": request.amount,
            "language": request.language,
            "platforms": request.platforms,
            "results": videos_output
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
