""" a function to run python files """
import os
import subprocess

def run_python_file(working_directory, file_path):
    """ a function to run python files """
    # print(f"~~~~~~~~~~\ntesting {file_path}\n~~~~~~~~~~")
    working_path = os.path.abspath(working_directory)
    check_path = os.path.abspath(os.path.join(working_path, file_path))
    try:
        if not check_path.startswith(working_path):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.exists(check_path):
            return f'Error: File "{file_path}" not found.'
        if not check_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'
    except Exception as e:
        return f'Error: {repr(e)}'
    try:
        result = subprocess.run([ "python", check_path ], capture_output=True, timeout=30, text=True, cwd=working_path)
        if not result.stdout and not result.stderr:
            return "No output produced."
        return_str = f"STDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}"
        if result.returncode != 0:
            return_str += f"\nProcess exited with code {result.returncode}"
        return return_str
    except Exception as e:
        return f"Error: executing Python file: {e}"
