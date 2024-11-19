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
    """Perform a semantic search of Northwestern University Library digital collections."""
    query_results = opensearch_vector_store.similarity_search(query, size=20)
    return json.dumps(query_results, default=str)


@tool
def aggregate(aggregation_query: str):
    """Perform a quantitative aggregation on the OpenSearch index.

    Available fields:
        ['accession_number', 'api_link', 'api_model', 'ark', 'box_name', 'box_number', 'catalog_key', 'collection.title.keyword', 'contributor.label.keyword', 'create_date', 'creator.id', 'date_created', 'embedding_model', 'embedding_text_length', 'genre.id', 'id', 'indexed_at', 'language.id', 'legacy_identifier', 'library_unit', 'license.id', 'location.id', 'modified_date', 'preservation_level', 'provenance', 'published', 'publisher', 'related_url.label', 'rights_holder', 'rights_statement.id', 'scope_and_contents', 'series', 'source', 'status', 'style_period.label.keyword', 'style_period.variants', 'subject.id', 'subject.variants', 'table_of_contents', 'technique.id', 'technique.variants', 'terms_of_use', 'title.keyword', 'visibility', 'work_type']

    Examples:
    Query about the number of collections: collection.title.keyword
    Query about the number of works by work type: work_type
    """
    try:
        response = opensearch_vector_store.aggregations_search(aggregation_query)
        return json.dumps(response, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})


tools = [search, aggregate]

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
workflow.add_edge(START, "agent")

# Add a conditional edge
workflow.add_conditional_edges(
    "agent",
    should_continue,
)

# Add a normal edge from `tools` to `agent`
workflow.add_edge("tools", "agent")

# Initialize memory to persist state between graph runs
checkpointer = MemorySaver()

# Compile the graph
app = workflow.compile(checkpointer=checkpointer, debug=True)

# Use the Runnable
final_state = app.invoke(
    {"messages": [HumanMessage(content="What is the document count by work type?")]},
    config={"configurable": {"thread_id": 42}},
)
final_state["messages"][-1].content

print(final_state["messages"][-1].content)

followup_question = app.invoke(
    {
        "messages": [
            HumanMessage(content="What's the total count of works by collection?")
        ]
    },
    config={"configurable": {"thread_id": 42}},
)

print(followup_question["messages"][-1].content)
