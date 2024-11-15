import os

from swarm import Agent, Swarm
from client import client
from utils import pretty_print_messages, process_and_print_streaming_response

def instructions(context_variables):
    """
    Define the instructions for the User Interface Agent, utilizing context variables.
    """
    return (
        "You are a helpful agent that provides information. When a user provides a location, "
        "store the associated zip code in the context variables and use it in your responses."
    )

def set_zip_code(context_variables, message):
    """
    Function to set the zip code in the context based on the user's message.
    Assumes the user provides the zip code directly.
    """
    zip_code = message.strip()
    context_variables["zip_code"] = zip_code
    return {"zip_code": zip_code}

def get_zip_code(context_variables):
    """
    Function to retrieve the zip code from the context variables.
    """
    zip_code = context_variables.get("zip_code", "Not provided")
    return {"zip_code": zip_code}

# Define the User Interface Agent with context-aware instructions and functions
user_interface_agent = Agent(
    name="User Interface Agent",
    instructions=instructions,
    functions=[set_zip_code, get_zip_code],
)

def run_demo_loop(
    starting_agent,
    context_variables=None,
    stream=False,
    debug=False,
) -> None:
    print("Starting Swarm CLI 🐝")
    
    messages = []
    agent = starting_agent
    context = context_variables or {}

    while True:
        user_input = input("\033[90mUser\033[0m: ")
        messages.append({"role": "user", "content": user_input})

        response = client.run(
            agent=agent,
            messages=messages,
            context_variables=context,
            stream=stream,
            debug=debug,
            model_override=os.getenv("AZURE_DEPLOYMENT_NAME"),
        )

        if stream:
            response_content = process_and_print_streaming_response(response)
        else:
            pretty_print_messages(response.messages)
            response_content = response.messages[-1]["content"]

        if hasattr(response, "context_variables") and response.context_variables:
            context.update(response.context_variables)

        messages.extend(response.messages)
        agent = response.agent

if __name__ == "__main__":
    initial_context = {"user_id": 123, "name": "Brendan"}
    run_demo_loop(
        starting_agent=user_interface_agent,
        context_variables=initial_context,
        debug=True,
    )