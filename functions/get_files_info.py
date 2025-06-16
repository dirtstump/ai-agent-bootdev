"""function for limiting the files available to AI"""
import os

def get_files_info(working_directory, directory=None):
    """limit the reach of the AI"""
    working_path = os.path.abspath(working_directory)
    # print(working_path)
    check_path = os.path.abspath(working_path + "/" + directory)
    # print(check_path)

    if not check_path.startswith(working_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(check_path):
        return f'Error: "{directory}" is not a directory'

    check_list_short = os.listdir(check_path)
    check_list = ["/".join([check_path, i]) for i in check_list_short]
    check_isdir = list(map(lambda i: os.path.isdir(os.path.abspath(i)), check_list))
    check_sizes = list(map(lambda i: os.path.getsize(os.path.abspath(i)), check_list))
    return "\n".join([
        f"{check_list_short[i]}: file_size={check_sizes[i]} bytes, is_dir={check_isdir[i]}"
        for i in range(len(check_isdir))
    ])


def main():
    """main"""
    print("tests")
    cases = [
        ("calculator", "."),
        ("calculator", "pkg"),
        ("calculator", "/bin"),
        ("calculator", "../"),
    ]
    list(map(lambda i: print(get_files_info(i[0], i[1])), cases))
    print("end")

if __name__ == "__main__":
    main()
