from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import os
import random
from openai import OpenAI

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.get("/")
def home():
    return {"status": "running"}

class ScriptRequest(BaseModel):
    amount: int
    language: str
    platforms: List[str]

MOTIVATION_TOPICS = [
    "discipline", "success", "never give up", "mindset",
    "confidence", "focus", "growth", "winning mentality"
]

@app.post("/create-motivation-scripts")
def create_scripts(request: ScriptRequest):
    results = []

    for _ in range(request.amount):
        topic = random.choice(MOTIVATION_TOPICS)

        prompt = (
            f"Create a powerful motivational script in {request.language}. "
            f"Topic: {topic}. "
            f"Length: 20–30 seconds. Emotional, cinematic."
        )

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        script_text = response.choices[0].message.content  # ✅ RICHTIG

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
