# server.py
# A tiny MCP server in Python exposing:
#  - generatePlan(instruction)
#  - sendTelegram(chatId, text, replyMarkup?, parseMode?)
#  - requestTravelPlan(instruction, chatId) - triggers n8n workflow
#
# Same purpose as the Node version: developer helper from Cursor.

import os
import json
import requests
from dotenv import load_dotenv
import time

# The Python MCP SDK may expose a simple server API.
# Here we use a minimal interface consistent with FastMCP-like patterns.
# If your installed SDK differs, we can adjust imports easily.
from mcp.server.fastmcp import FastMCP

load_dotenv()

mcp = FastMCP("nova-atlas-mcp")

@mcp.tool()
def generatePlan(instruction: str) -> str:
    r = requests.post(
        "https://nova-atlas-2.onrender.com/generate",
        json={"instruction": instruction},
        timeout=60
    )
    r.raise_for_status()
    j = r.json()
    travel = j.get("travel_plan", "(missing travel_plan)")
    post = j.get("social_post", "(missing social_post)")
    return f"✅ Generated from FastAPI\n\n🧭 Travel Plan:\n{travel}\n\n📝 Social Post:\n{post}"

@mcp.tool()
def sendTelegram(chatId: str, text: str, replyMarkup: dict | None = None, parseMode: str | None = None) -> str:
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError("Missing TELEGRAM_BOT_TOKEN in environment.")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chatId,
        "text": text
    }
    if replyMarkup is not None:
        payload["reply_markup"] = replyMarkup
    if parseMode is not None:
        payload["parse_mode"] = parseMode
    r = requests.post(url, json=payload, timeout=60)
    data = r.json()
    if not data.get("ok"):
        raise RuntimeError(f"Telegram error: {data.get('description')}")
    return "📤 Sent to Telegram ✅"

@mcp.tool()
def requestTravelPlan(instruction: str, chatId: str) -> str:
    """
    Request a travel plan through n8n workflow with confirmation.
    This triggers the n8n webhook which will handle the Telegram interaction.
    """
    # Get n8n webhook URL from environment
    n8n_webhook_url = os.environ.get("N8N_WEBHOOK_URL")
    if not n8n_webhook_url:
        raise RuntimeError("Missing N8N_WEBHOOK_URL in environment.")
    
    # Prepare the payload for n8n
    payload = {
        "instruction": instruction,
        "chat_id": chatId,
        "timestamp": str(int(time.time())),
        "request_id": f"req_{int(time.time())}"
    }
    
    try:
        r = requests.post(n8n_webhook_url, json=payload, timeout=30)
        r.raise_for_status()
        return f"✅ Travel plan request sent to n8n workflow!\n\n📋 Instruction: {instruction}\n👤 Chat ID: {chatId}\n\nn8n will now send a confirmation message to Telegram with Yes/No buttons."
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to trigger n8n workflow: {str(e)}")

@mcp.tool()
def sendTravelConfirmation(chatId: str, instruction: str) -> str:
    """
    Send a confirmation message with Yes/No buttons for travel plan request.
    This is a helper function that can be called directly if needed.
    """
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError("Missing TELEGRAM_BOT_TOKEN in environment.")
    
    # Create inline keyboard with Yes/No buttons
    reply_markup = {
        "inline_keyboard": [
            [
                {
                    "text": "✅ Yes, generate plan",
                    "callback_data": f"confirm_yes:{instruction[:50]}"
                },
                {
                    "text": "❌ No, cancel",
                    "callback_data": "confirm_no"
                }
            ]
        ]
    }
    
    message_text = f"""🤖 **Nova-Atlas Travel Assistant**

I received your request: *{instruction}*

Would you like me to generate a detailed travel plan and social media caption for you?

Please confirm with the buttons below or reply with "yes" or "no"."""
    
    return sendTelegram(chatId, message_text, reply_markup, "Markdown")

if __name__ == "__main__":
    mcp.run()  # stdin/stdout transport for Cursor
