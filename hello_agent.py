import os
from dotenv import load_dotenv

load_dotenv()

from agents import Agent, Runner

# Create a simple agent with a name and role
agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant"
)

# Ask the agent to write a haiku about recursion
result = Runner.run_sync(agent, "Write a haiku about recursion in programming.")

# Print the final answer from the agent
print(result.final_output)
