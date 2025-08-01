# agent_memory.py
import redis

# Connect to DragonflyDB (default port)
r = redis.Redis(host='localhost', port=6379)

# Set and get memory
r.set("agent1_context", "User asked about budget API.")
print(r.get("agent1_context").decode())  # Output: User asked about budget API.
