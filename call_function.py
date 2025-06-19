""" function for calling the callable functions """
from google.genai import types
from functions import (
    get_file_content,
    get_files_info,
    run_python_file,
    write_file,
)


def call_function(function_call_part, verbose=False):
    """ function for calling the callable funcitons """
    function_name = function_call_part.name
    function_args = function_call_part.args
    functions = [
        'get_files_content',
        'get_files_info',
        'run_python_file',
        'write_file',
    ]

    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")

    if function_name not in functions:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    print(f"hello {function_name}({function_args})")
    return 0
