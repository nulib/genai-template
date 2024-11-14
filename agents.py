import os

from client import client
from swarm import Agent

def main():
    def transfer_to_agent_b():
        return agent_b

    agent_a = Agent(
        name="Agent A",
        instructions="You are a helpful agent.",
        functions=[transfer_to_agent_b],
    )

    agent_b = Agent(
        name="Agent B",
        instructions="Only speak in Haikus.",
    )

    response = client.run(
        agent=agent_a,
        messages=[{"role": "user", "content": "I want to talk to agent B."}],
        model_override=os.getenv("AZURE_DEPLOYMENT_NAME"),
    )

    print(response.messages[-1]["content"])

if __name__ == "__main__":
    main()
