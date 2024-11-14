import os

from client import client
from swarm import Agent


def get_weather(location) -> str:
    print(f"Getting weather for {location}")
    return "{'temp':67, 'unit':'F'}"


agent = Agent(
    name="Agent",
    instructions=(
      "You are a helpful agent that provides weather information. "
      "When a user provides a location, respond using the estimated zip code for that location "
      "instead of expanding abbreviations or full names."
      ),
    functions=[get_weather],
)

messages = [{"role": "user", "content": "What's the weather in Buffalo Grove?"}]

response = client.run(
    agent=agent, 
    messages=messages, 
    model_override=os.getenv("AZURE_DEPLOYMENT_NAME"),
    debug=True,
)

print(response.messages[-1]["content"])