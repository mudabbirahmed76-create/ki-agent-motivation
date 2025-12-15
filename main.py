from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import os
import random
from openai import OpenAI

app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---------- REQUEST MODEL ----------
class ScriptRequest(BaseModel):
    amount: int
    platforms: List[str]

# ---------- TOPICS ----------
MOTIVATION_TOPICS = [
    "discipline",
    "self confidence",
    "never give up",
    "success mindset",
    "hard work",
    "focus",
    "mental strength",
    "growth",
    "winning mentality",
    "overcoming fear"
]

# ---------- HEALTH CHECK ----------
@app.get("/")
def root():
    return {"status": "running"}

# ---------- SCRIPT GENERATOR ----------
@app.post("/create-motivation-scripts")
def create_scripts(request: ScriptRequest):
    results = []

    for _ in range(request.amount):
        topic = random.choice(MOTIVATION_TOPICS)

        prompt = (
            f"Write a powerful motivational video script in ENGLISH.\n"
            f"Topic: {topic}\n"
            f"Length: 20–30 seconds.\n"
            f"Style: emotional, cinematic, strong hook, short sentences."
        )

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )

        script_text = response.output_text

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

# ---------- REQUIRED FOR RAILWAY ----------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
