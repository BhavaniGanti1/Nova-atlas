import os
import redis
from dotenv import load_dotenv
from agents import Agent, Runner
from agents.tool.tool_decorator import tool  # ✅ Correct decorator import

# Load environment variables
load_dotenv()

# Connect to Redis (on your local system)
store = redis.Redis(host="localhost", port=6379, decode_responses=True)

# Tool to store a value
@tool()
def store_value(key: str, value: str) -> str:
    store.set(key, value)
    return f"Stored {key} = {value}"

# Tool to retrieve a value
@tool()
def get_value(key: str) -> str:
    result = store.get(key)
    return result or "No value found for this key."

# Create agent with tools
agent = Agent(
    name="DataAgent",
    instructions="You help store and retrieve values using Redis.",
    tools=[store_value, get_value]
)

# Ask it to store something
response1 = Runner.run_sync(agent, "Store key 'username' with value 'bhavani'")
print("Store Response:", response1.final_output)

# Ask it to retrieve the value
response2 = Runner.run_sync(agent, "What is the value for key 'username'?")
print("Retrieve Response:", response2.final_output)
