from ollama import chat
from ollama import ChatResponse
import os
import difflib


def list_directory(path: str) -> list:
    """
    Lists all files and directories in the given path.

    Args:
      path (str): The directory path to list contents of.

    Returns:
      list: A list of files and directories in the given path.
    """
    try:
        return os.listdir(path)
    except Exception as e:
        return [str(e)]


def search_directory(path: str, filename: str, cutoff: float = 0.6) -> list:
    """
    Performs a fuzzy search for a file in the given directory and its subdirectories.

    Args:
      path (str): The directory path to search in.
      filename (str): The name of the file to search for.
      cutoff (float): The similarity threshold between 0 and 1.

    Returns:
      list: A list of paths where similar files are found.
    """
    matches = []
    for root, dirnames, filenames in os.walk(path):
        # Use difflib.get_close_matches to find similar filenames
        similar_files = difflib.get_close_matches(filename, filenames, cutoff=cutoff)
        for match in similar_files:
            matches.append(os.path.join(root, match))
    return matches


# Define tool metadata
list_directory_tool = {
    "type": "function",
    "function": {
        "name": "list_directory",
        "description": "List all files and directories in the specified path.",
        "parameters": {
            "type": "object",
            "required": ["path"],
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The directory path to list contents of.",
                },
            },
        },
    },
}

search_directory_tool = {
    "type": "function",
    "function": {
        "name": "search_directory",
        "description": "Perform a fuzzy search for a file within a directory and its subdirectories.",
        "parameters": {
            "type": "object",
            "required": ["path", "filename"],
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The directory path to search in.",
                },
                "filename": {
                    "type": "string",
                    "description": "The name of the file to search for.",
                },
                "cutoff": {
                    "type": "number",
                    "description": "The similarity threshold between 0 and 1.",
                    "default": 0.6,
                },
            },
        },
    },
}

messages = [
    {
        "role": "user",
        "content": "Search for files similar to 'coffee' in the '/Users/brendan/Desktop' directory.",
    }
]
print("Prompt:", messages[0]["content"])

available_functions = {
    "list_directory": list_directory,
    "search_directory": search_directory,
}

response: ChatResponse = chat(
    "llama3.2",
    messages=messages,
    tools=[list_directory_tool, search_directory_tool],
)

if response.message.tool_calls:
    # There may be multiple tool calls in the response
    for tool in response.message.tool_calls:
        # Ensure the function is available, and then call it
        if function_to_call := available_functions.get(tool.function.name):
            print("Calling function:", tool.function.name)
            print("Arguments:", tool.function.arguments)

            arguments = tool.function.arguments

            # Convert 'cutoff' to float if it exists, else set to default
            if "cutoff" in arguments:
                try:
                    arguments["cutoff"] = float(arguments["cutoff"])
                except ValueError:
                    print("Invalid cutoff value provided. Using default cutoff of 0.6.")
                    arguments["cutoff"] = 0.6
            else:
                arguments["cutoff"] = 0.6  # default cutoff value

            output = function_to_call(**arguments)
            print("Function output:", output)
        else:
            print("Function", tool.function.name, "not found")

    # Only needed to chat with the model using the tool call results
    if response.message.tool_calls:
        # Add the function response to messages for the model to use
        messages.append(response.message)
        messages.append(
            {"role": "tool", "content": str(output), "name": tool.function.name}
        )

        # Get final response from model with function outputs
        final_response = chat("qwq", messages=messages)
        print("Final response:", final_response.message.content)

else:
    print("No tool calls returned from model")
