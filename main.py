from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from openai import OpenAI
import os
import random

# Initialize FastAPI
app = FastAPI()

# Root endpoint for Railway health check
@app.get("/")
def home():
    return {"status": "running"}

# OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Request model
class ScriptRequest(BaseModel):
    amount: int
    language: str
    platforms: List[str]

# Motivational topic pool
MOTIVATION_TOPICS = [
    "strength", "discipline", "success", "never give up",
    "mindset", "growth", "courage", "ambition",
    "transformation", "winning mentality",
    "self-confidence", "overcoming fear",
    "patience", "focus"
]

@app.post("/create-scripts")
def create_scripts(request: ScriptRequest):

    results = []

    for _ in range(request.amount):

        # 1. Pick random topic
        topic = random.choice(MOTIVATION_TOPICS)

        # 2. Generate script text
        prompt = (
            f"Create a powerful motivational video script in {request.language} "
            f"about the topic: {topic}. "
            f"Make it emotional, cinematic, and 20 seconds long."
        )

        chat = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        script_text = chat.choices[0].message["content"]

        # 3. Save result
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


# Railway Startup
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
