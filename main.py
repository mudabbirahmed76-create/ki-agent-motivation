from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Videoanfrage(BaseModel):
    Menge: int
    Thema: str
    Sprache: str
    Plattformen: list[str]

@app.post("/create-motivation-videos")
def videos_erstellen(anfrage: Videoanfrage):
    return {
        "status": "erhalten",
        "Menge": anfrage.Menge,
        "Thema": anfrage.Thema,
        "Nachricht": "KI-Server wurde erfolgreich erreicht! Videoproduktion kommt als nächstes."
    }
