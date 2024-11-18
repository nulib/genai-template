import json

from opensearch_client import opensearch_vector_store

from swarm import Agent
from utils import run_demo_loop


def similarity_search(context_variables, query):
    """Query the search index for relevant documents."""
    print(f"Searching with query: {query}")
    query_results = opensearch_vector_store.similarity_search(query, size=100)
    context_variables["source"] = query_results
    return json.dumps(query_results, default=str)

def flag_problematic_records(context_variables):
    """Flag problematic records in the source."""
    source = context_variables.get("source", None)
    print(f"Flagging problematic records: {source}")
    return "Problematic records flagged"

def mark_as_approved(context_variables):
    """Mark a record as approved."""
    source = context_variables.get("source", None)
    print(f"Marking records as approved: {source}")
    return "Record marked as approved"


def transfer_to_formatter():
    return formatter_agent


def transfer_to_search():
    return search_agent


def transfer_to_triage():
    """Call this function when a user needs to be transferred to a different agent and a different policy.
    For instance, if a user is asking about a topic that is not handled by the current agent, call this function.
    """
    return triage_agent


def triage_instructions(context_variables):
    name = context_variables.get("name", "friend")
    return f"""You are to triage a users request, and call a tool to transfer to the right intent.
    Once you are ready to transfer to the right intent, call the tool to transfer to the right intent.
    You dont need to know specifics, just the topic of the request.
    When you need more information to triage the request to an agent, ask a direct question without explaining why you're asking it.
    Do not share your thought process with the user! Do not make unreasonable assumptions on behalf of user.
    The user context is here: {name}"""


triage_agent = Agent(
    name="Triage Agent",
    instructions=triage_instructions,
    functions=[transfer_to_search, mark_as_approved, flag_problematic_records],
)


def search_agent_instructions(context_variables):
    source = context_variables.get("source", None)
    return f"""You are a search agent. Your current source information is: {source}
    Ask clarifying questions to make sure you know the user's search intent if necessary. 
    Queries are stored in your context when the function is called. 
    If you already have the proper sources in context, transfter to the appropriate agent."""


search_agent = Agent(
    name="Search Agent",
    instructions=search_agent_instructions,
    functions=[transfer_to_triage, transfer_to_formatter, similarity_search, mark_as_approved],
)


def formatter_instructions(context_variables):
    source = context_variables.get("source", None)
    return f"""You are a formatter agent. Your current source information is: {source}
    Format the source documents according to the user's instructions. Focus only on the source information that is relevant to the user's request."""


formatter_agent = Agent(
    name="Formatter Agent",
    instructions=formatter_instructions,
    functions=[transfer_to_triage],
)

if __name__ == "__main__":
    run_demo_loop(
        context_variables={"name": "Brendan"},
        starting_agent=triage_agent,
        debug=False,
    )
