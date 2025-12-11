from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from openai import OpenAI
import os
import random

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# HEALTH CHECK für Railway
@app.get("/")
def home():
    return {"status": "running"}

class VideoRequest(BaseModel):
    amount: int
    language: str
    platforms: List[str]

MOTIVATION_TOPICS = [
    "strength", "discipline", "success", "never give up",
    "mindset", "growth", "courage", "ambition",
    "transformation", "winning mentality",
    "self-confidence", "overcoming fear",
    "patience", "focus"
]

@app.post("/create-scripts")
def create_scripts(request: VideoRequest):
    results = []

    for i in range(request.amount):
        topic = random.choice(MOTIVATION_TOPICS)

        prompt = (
            f"Write a powerful motivational script about '{topic}' in "
            f"{request.language}. Make it emotional and cinematic. "
            f"Length: 20 seconds."
        )

        chat = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        script_text = chat.choices[0].message["content"]

        results.append({
            "topic": topic,
            "script": script_text,
            "platforms_ready": request.platforms
        })

    return {
        "status": "success",
        "scripts_generated": len(results),
        "scripts": results
    }


# Railway Start
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
