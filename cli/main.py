from swarm import Agent
from utils import run_demo_loop


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

if __name__ == "__main__":
    initial_context = {"user_id": 123, "name": "Brendan"}
    run_demo_loop(
        starting_agent=user_interface_agent,
        context_variables=initial_context,
        debug=True,
    )
