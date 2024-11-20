# Generative AI Template

A Python project template for building AI applications using Azure OpenAI services. This template includes:

- Ready-to-use Azure OpenAI integration
- Example implementation of AI agents using Swarm
- Development environment setup with modern Python tools

## Prerequisites

- Python 3.12 or higher
- [uv](https://github.com/astral-sh/uv) package manager ([installation guide](https://docs.astral.sh/uv/getting-started/installation/))
- Azure subscription with OpenAI service access
- Azure OpenAI deployment with GPT model

## Setup

1. Install uv if you haven't already:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Install and configure Azure CLI using homebrew:

```bash
brew update && brew install azure-cli

# Login to Azure and choose the subscription that enables you to make OpenAI LLM requests
az login
```

3. Clone this repository:

```bash
git clone git@github.com:nulib/genai-template.git
cd genai-template
```

4. Create and activate a virtual environment:

```bash
uv venv
source .venv/bin/activate # On Windows use: .venv\Scripts\activate
```

5. Install dependencies:

```bash
uv sync
```

6. Environment Variables:
   Create a `.env` file in the project root with the following required variables:

```plaintext
AZURE_ENDPOINT=https://<your-resource-name>.openai.azure.com/
AZURE_API_VERSION=2024-08-01-preview
AZURE_ENDPOINT_SCOPE=https://cognitiveservices.azure.com/.default
AZURE_DEPLOYMENT_NAME=<your-model-deployment-name>
OPENSEARCH_ENDPOINT=<your-opensearch-endpoint>
OPENSEARCH_MODEL_ID=<your-opensearch-model-id>
```

Replace:

- `<your-resource-name>` with your Azure OpenAI resource name
- `<your-model-deployment-name>` with your model deployment name (e.g., "gpt-4")
- `<your-opensearch-endpoint>` with your OpenSearch domain endpoint
- `<your-opensearch-model-id>` with your OpenSearch model ID

Note: The `.env` file is already included in `.gitignore`

## Running the Application

Run the OpenSearch client:

```bash
uv run opensearch_client.py
```

Run the `langggraph` agents demo:

```bash
uv run -m langgraph_agents.main
```

Run the `swarm` agents demo:

```bash
uv run -m swarm_agents.main
```

## Project Structure

This project is organized around two main agent frameworks: `langgraph_agents/` for graph-based workflows and `swarm_agents/` for OpenAI's Swarm framework. Each framework directory contains its own implementation of agents, tools, and workflows. A `cli/` directory provides one example of implementing command-line interface capabilities. Shared infrastructure components like the OpenAI client, OpenSearch integration, and utility functions reside in the root directory. Configuration is managed through `pyproject.toml` and environment variables (`.env`).

## Dependencies

The project uses these dependencies:

- `azure-identity` (^1.19.0): Azure authentication
- `langchain` (^0.3.7): LangChain framework
- `langchain-openai` (^0.2.8): LangChain OpenAI integration
- `langgraph` (^0.2.50): Graph-based workflow framework
- `openai` (^1.54.4): Azure OpenAI API client
- `opensearch-py` (^2.7.1): OpenSearch client
- `python-dotenv` (^1.0.1): Environment configuration
- `swarm` (latest): Agent implementation framework from OpenAI
- `boto3` (^1.35.63): AWS SDK for Python
- `requests-aws4auth` (^0.4.3): AWS request signing

## Development

This project uses uv for dependency management. Common commands:

- Add a dependency: `uv add <package-name>`
- Remove a dependency: `uv remove <package-name>`
- Update dependencies: `uv sync`
- Run a script: `uv run <script-name>`
- Run a module: `uv run -m <module-name>`

## Troubleshooting

Common issues and solutions:

1. **Authentication Errors**:

   - Ensure you're logged in with `az login` and `aws sso login`
   - Verify your Azure subscription has OpenAI access
   - Check that your `.env` variables are correct

2. **Model Deployment Issues**:

   - Verify your deployment name matches AZURE_DEPLOYMENT_NAME
   - Ensure your Azure OpenAI service is properly configured
   - Check that your Azure account has either `Cognitive Services OpenAI Contributor` or `Cognitive Services OpenAI User` role ([see Azure RBAC documentation](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/role-based-access-control#cognitive-services-openai-contributor))

3. **Package Installation Problems**:
   - Try removing the `.venv` directory and recreating it
   - Update uv
