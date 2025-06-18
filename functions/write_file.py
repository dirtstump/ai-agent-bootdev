""" function for writing to a file """
import os

def write_file(working_directory, file_path, content):
    """ function for writing to a file """
    working_path = os.path.abspath(working_directory)
    check_path = os.path.join(working_path, file_path)

    try:
        if not check_path.startswith(working_path):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(check_path):
            os.makedirs(file_path)
        with open(file_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {repr(e)}'
