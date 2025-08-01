import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq()

def chat_with_agents(user_prompt):
    system_msg = {
        "role": "system",
        "content": (
            "You are simulating a conversation between two agents:\n"
            "**Nova** - a creative strategist who specializes in branding, storytelling, and ideas.\n"
            "**Atlas** - an analytical planner who structures timelines, tasks, and systems for execution.\n"
            "Both collaborate closely on tasks like travel planning, marketing, or social media content.\n"
            "They should respond as themselves, referencing each other’s ideas and improving collaboratively.\n"
            "End with a complete plan or a social media post if applicable."
        )
    }

    messages = [
        system_msg,
        {"role": "user", "content": user_prompt}
    ]

    completion = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=messages,
        temperature=0.9,
        max_completion_tokens=1024,
        top_p=1,
        stream=False,
    )

    return completion.choices[0].message.content

# Example usage
if __name__ == "__main__":
    user_input = input("Enter your instruction for Nova and Atlas: ")
    response = chat_with_agents(user_input)
    print("\n🤖 Nova & Atlas Collaboration:\n")
    print(response)
