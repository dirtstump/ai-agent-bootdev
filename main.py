""" main function for AI course on boot.dev """
import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
import call_function

def main():
    """main function for boot.dev AI course"""
    user_args = sys.argv[1:]

    verbose = False
    if "--verbose" in user_args:
        verbose = True
        user_args.remove("--verbose")

    if len(user_args) > 1:
        print("error: too many prompts/args")
        sys.exit(1)
    if len(user_args) < 1 or user_args[0][0] == "-":
        print("error: no prompt given")
        sys.exit(1)

    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")
    user_prompt = user_args[0]
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



    # Start loop here
    loop_count = 20
    loop = True
    while loop:

        response = client.models.generate_content(
            model=model_name,
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt,
            ),
        )

        # append the AI response to the messages list for looping
        list(map(lambda x: messages.append(x.content), response.candidates))

        if verbose:
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        if response.function_calls:
            function_call_part = response.function_calls[0]
            if verbose:
                print("~~function calls~~")
            function_call_result = call_function.call_function(function_call_part, verbose)
            if not function_call_result.parts[0].function_response.response:
                raise Exception("Error: no response in function response")
            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
            messages.append(function_call_result)
        else:
            loop = False

        loop_count -= 1
        if loop_count <= 0:
            loop = False
            print("Error: out of interations")

    # End loop here
    print("\n\n~~FINAL RESPONSE~~\n")
    print(response.text)




def function_definitions():
    """ function for specifying all the callable function """
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
    schema_get_file_content = types.FunctionDeclaration(
        name="get_file_content",
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
                "args": types.Schema(
                    type=types.Type.STRING,
                    description="Additional args to call with the python file. Will be formatted such as: example.py 'args in a string'",
                ),
            },
        ),
    )

    return [
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
        ]

if __name__ == "__main__":
    main()
