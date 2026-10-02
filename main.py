import secrets
import string
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl

app = FastAPI()

db: dict[str, str] = {}   # code -> original url
ALPHABET = string.ascii_letters + string.digits   # 62 characters

class ShortenRequest(BaseModel):
    url: HttpUrl          # invalid URLs automatically reject ho jayenge

def make_code(length: int = 7) -> str:
    return "".join(secrets.choice(ALPHABET) for _ in range(length))

@app.post("/shorten")
def shorten(req: ShortenRequest):
    code = make_code()
    while code in db:             # collision ho jaye to dobara try
        code = make_code()
    db[code] = str(req.url)
    return {"short_url": f"http://localhost:8000/{code}"}

@app.get("/{code}")
def redirect(code: str):
    url = db.get(code)
    if url is None:
        raise HTTPException(status_code=404, detail="Link not found")
    return RedirectResponse(url, status_code=307)