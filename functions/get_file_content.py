""" function for getting the contents of a file """
import os

def get_file_content(working_directory, file_path):
    """ function for getting the contents of a file """
    working_path = os.path.abspath(working_directory)
    check_path = os.path.join(working_path, file_path)

    if not check_path.startswith(working_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(check_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    max_chars = 10000

    try:
        with open(check_path, "r") as f:
            file_content = f.read(max_chars)
            if len(file_content) == max_chars:
                file_content = file_content + f'...File "{file_path}" truncated at 10000 characters'
    except Exception as e:
        return f'Error: {repr(e)}'

    return file_content
