from flask import Flask, request, jsonify
from dotenv import load_dotenv
from groq import Groq
import os

app = Flask(__name__)
load_dotenv()

client = Groq()

@app.route("/generate", methods=["POST"])
def generate_response():
    data = request.get_json()
    user_input = data.get("prompt", "")

    system_msg = {
        "role": "system",
        "content": (
            "You are simulating a conversation between two agents:\n"
            "**Nova** - a creative strategist for branding, storytelling, and ideas.\n"
            "**Atlas** - a logical planner who structures timelines and content strategies.\n"
            "They collaborate on travel, marketing, social media, etc. End with a suggestion or social post if possible."
        )
    }

    messages = [
        system_msg,
        {"role": "user", "content": user_input}
    ]

    completion = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=messages,
        temperature=0.9,
        max_completion_tokens=1024,
        top_p=1,
        stream=False,
    )

    return jsonify({"response": completion.choices[0].message.content})


if __name__ == "__main__":
    app.run(port=5001, debug=True)
