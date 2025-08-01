from fastapi import FastAPI
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()
client = Groq()

@app.get("/")
def home():
    return {"message": "Nova Atlas Agent API is running"}

@app.post("/chat")
def chat():
    completion = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {"role": "user", "content": "I NEED travel agent models to discuss each other based on user instructions."},
            {"role": "assistant", "content": "Here are five travel agent models with unique skills..."},
        ],
        temperature=1,
        max_tokens=1024
    )
    return {"response": completion.choices[0].message.content}
