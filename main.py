""" main function for AI course on boot.dev """
import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    """main function for boot.dev AI course"""
    if len(sys.argv) < 2 or sys.argv[1][0] == "-":
        print("error: no prompt given")
        sys.exit(1)

    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")
    user_prompt = sys.argv[1]
    model_name = "gemini-2.0-flash-001"
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)]),]
    available_functions = types.Tool(function_declarations=function_definitions())


    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=model_name,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
        ),
    )
    if "--verbose" in sys.argv:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    if response.function_calls:
        print("\n~~function calls~~")
        print(
            f'Calling function: {response.function_calls[0].name}({response.function_calls[0].args
        })')
    else:
        print("\n~~response~~")
        print(response.text)


def function_definitions():
    schema_get_files_info = types.FunctionDeclaration(
        name="get_files_info",
        description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "directory": types.Schema(
                    type=types.Type.STRING,
                    description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
                ),
            },
        ),
    )
    schema_get_files_content = types.FunctionDeclaration(
        name="get_files_content",
        description="Return contents of a file in the specified directory, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The file to read from, relative to the working directory. The file and relative path must be provided.",
                ),
            },
        ),
    )
    schema_write_file = types.FunctionDeclaration(
        name="write_file",
        description="Overwrite the specified file, constraied to the working directory",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The file to overwrite, relative to the working directory. The file and relative must be provided.",
                ),
                "content": types.Schema(
                    type=types.Type.STRING,
                    description="The contents to write to the file. This should be passed after 'file_path'."
                ),
            },
        ),
    )
    schema_run_python_file = types.FunctionDeclaration(
        name="run_python_file",
        description="Run the specified python file, constrained to the working directory",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The python file to run, relative to the working directory. The file (ending in .py) and relative path must be provided.",
                ),
            },
        ),
    )

    return [
        schema_get_files_info,
        schema_get_files_content,
        schema_write_file,
        schema_run_python_file,
        ]

if __name__ == "__main__":
    main()
