from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import AzureOpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), os.getenv("AZURE_ENDPOINT_SCOPE", "https://cognitiveservices.azure.com/.default")
)

azure_client = AzureOpenAI(
    api_version=os.getenv("AZURE_API_VERSION", "2024-08-01-preview"),
    azure_endpoint=os.getenv("AZURE_ENDPOINT"),
    azure_ad_token_provider=token_provider
)

from swarm import Swarm, Agent

client = Swarm(client=azure_client)

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
