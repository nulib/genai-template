import json
import os

from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI

from opensearch_client import opensearch_vector_store

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

from typing import Annotated, Literal, TypedDict

from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph, MessagesState
from langgraph.prebuilt import ToolNode


@tool
def search(query: str):
    """Call for semantic search of Northwestern University Library digital collections."""
    # This is a placeholder, but don't tell the LLM that...
    query_results = opensearch_vector_store.similarity_search(query, size=20)
    return json.dumps(query_results, default=str)


tools = [search]

tool_node = ToolNode(tools)

model = model.bind_tools(tools)


# Define the function that determines whether to continue or not
def should_continue(state: MessagesState) -> Literal["tools", END]:
    messages = state["messages"]
    last_message = messages[-1]
    # If the LLM makes a tool call, then we route to the "tools" node
    if last_message.tool_calls:
        return "tools"
    # Otherwise, we stop (reply to the user)
    return END


# Define the function that calls the model
def call_model(state: MessagesState):
    messages = state["messages"]
    response = model.invoke(messages, model=os.getenv("AZURE_DEPLOYMENT_NAME"))
    # We return a list, because this will get added to the existing list
    return {"messages": [response]}


# Define a new graph
workflow = StateGraph(MessagesState)

# Define the two nodes we will cycle between
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

# Set the entrypoint as `agent`
# This means that this node is the first one called
workflow.add_edge(START, "agent")

# We now add a conditional edge
workflow.add_conditional_edges(
    # First, we define the start node. We use `agent`.
    # This means these are the edges taken after the `agent` node is called.
    "agent",
    # Next, we pass in the function that will determine which node is called next.
    should_continue,
)

# We now add a normal edge from `tools` to `agent`.
# This means that after `tools` is called, `agent` node is called next.
workflow.add_edge("tools", "agent")

# Initialize memory to persist state between graph runs
checkpointer = MemorySaver()

# Finally, we compile it!
# This compiles it into a LangChain Runnable,
# meaning you can use it as you would any other runnable.
# Note that we're (optionally) passing the memory when compiling the graph
app = workflow.compile(checkpointer=checkpointer, debug=True)

# Use the Runnable
final_state = app.invoke(
    {
        "messages": [
            HumanMessage(content="Can you search for photographs of Nairobi, Kenya?")
        ]
    },
    config={"configurable": {"thread_id": 42}},
)
final_state["messages"][-1].content

print(final_state["messages"][-1].content)
