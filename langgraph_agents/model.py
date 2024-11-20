import os
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI

load_dotenv()

# Setup token provider
token_provider = get_bearer_token_provider(
    DefaultAzureCredential(),
    os.getenv("AZURE_ENDPOINT_SCOPE", "https://cognitiveservices.azure.com/.default"),
)

# Initialize AzureOpenAI client
model = AzureChatOpenAI(
    api_version=os.getenv("AZURE_API_VERSION", "2024-08-01-preview"),
    azure_endpoint=os.getenv("AZURE_ENDPOINT"),
    azure_ad_token_provider=token_provider,
)

print("AzureOpenAI client initialized")