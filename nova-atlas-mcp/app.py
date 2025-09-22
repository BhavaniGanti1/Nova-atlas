from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq
import json
import os
import re

# ---- config ----
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY is not set")

client = Groq(api_key=GROQ_API_KEY)
app = FastAPI(title="Nova Atlas Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

# ---- models ----
class GenerateIn(BaseModel):
    instruction: str

class GenerateOut(BaseModel):
    travel_plan: str
    social_post: str

# ---- helpers ----
def tg_truncate(s: str, limit: int = 4000) -> str:
    return s if len(s) <= limit else s[: limit - 1] + "…"

def extract_json(s: str) -> dict:
    """
    Try to pull a JSON object from a string. If the whole string is JSON,
    json.loads will succeed; otherwise we look for the first {...} block.
    """
    try:
        return json.loads(s)
    except Exception:
        pass
    m = re.search(r"\{.*\}", s, flags=re.S)
    if m:
        return json.loads(m.group(0))
    raise ValueError("No JSON object found")

# ---- routes ----
@app.get("/")
def health():
    return {"ok": True, "message": "Nova Atlas Agent API is running"}

@app.post("/generate", response_model=GenerateOut)
def generate(body: GenerateIn):
    # Ask the model to return strict JSON only
    system_prompt = (
        "You are a travel assistant. Produce a travel plan and a short social media caption.\n"
        "Return ONLY a JSON object with two string keys:\n"
        '{ "travel_plan": "...", "social_post": "..." }\n'
        "No extra text, no markdown, no explanation."
    )
    user_prompt = body.instruction.strip()

    try:
        resp = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
            max_tokens=1200,
        )
        content = resp.choices[0].message.content or ""
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Groq API error: {e}")

    # Parse as JSON; fall back to a minimal split if model misbehaves
    try:
        data = extract_json(content)
        travel_plan = str(data.get("travel_plan", "")).strip()
        social_post = str(data.get("social_post", "")).strip()
    except Exception:
        # Fallback for older prompt style that used "Social Post"
        if "Social Post" in content:
            parts = re.split(r"(?i)Social Post\s*[:\-]\s*", content, maxsplit=1)
            travel_plan = parts[0].strip()
            social_post = parts[1].strip() if len(parts) > 1 else ""
        else:
            raise HTTPException(
                status_code=500,
                detail={"error": "AI returned unstructured text", "raw": content},
            )

    if not travel_plan:
        raise HTTPException(status_code=500, detail="Empty travel_plan from model")

    return {
        "travel_plan": tg_truncate(travel_plan),
        "social_post": tg_truncate(social_post or "🌍 Your trip is ready!"),
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)