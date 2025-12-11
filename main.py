from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from openai import OpenAI
import os
import random

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ScriptRequest(BaseModel):
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

@app.get("/")
def home():
    return {"status": "running"}

@app.post("/create-motivation-scripts")
def create_scripts(request: ScriptRequest):

    results = []

    for _ in range(request.amount):

        topic = random.choice(MOTIVATION_TOPICS)

        prompt = (
            f"Write a powerful motivational speech in {request.language}. "
            f"The topic is: {topic}. "
            f"Length: 20–30 seconds. Emotional cinematic style."
        )

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        script_text = completion.choices[0].message["content"]

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


# RAILWAY STARTUP
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
