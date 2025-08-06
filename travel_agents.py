from fastapi import FastAPI, Request
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.get("/")
def home():
    return {"message": "Nova Atlas Agent API is running"}

@app.post("/generate")
async def generate(request: Request):
    body = await request.json()
    instruction = body.get("instruction")

    if not instruction:
        return {"error": "Missing instruction"}

    response = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[
            {"role": "user", "content": instruction}
        ]
    )

    output = response.choices[0].message.content

    if "📸 Social Post:" not in output:
        return {"error": "AI response unstructured", "raw": output}

    travel_plan, social_post = output.split("📸 Social Post:")
    return {
        "travel_plan": travel_plan.strip(),
        "social_post": social_post.strip()
    }
