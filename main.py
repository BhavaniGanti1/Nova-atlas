from travel_agents import app 
from fastapi import FastAPI, Request
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()
client = Groq()

@app.get("/")
def home():
    return {"message": "Nova Atlas Agent API is running"}

@app.post("/generate")
async def generate(request: Request):
    body = await request.json()
    instruction = body.get("instruction", "")

    # Process instruction using Groq, or return mock output for now
    return {
        "travel_plan": "Here is a 3-day trip to Goa...",
        "social_post": "🌴 Ready for the ultimate Goa experience?..."
    }
