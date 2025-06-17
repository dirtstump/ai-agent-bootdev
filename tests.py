"""tests for get_files_info"""
from functions.get_file_content import get_file_content

def main():
    """test funciton for get_files_info"""
    cases = [
        ("calculator", "main.py"),
        ("calculator", "pkg/calculator.py"),
        ("calculator", "/bin/cat"),
    ]
    list(map(lambda i: print(get_file_content(i[0], i[1])), cases))

if __name__ == "__main__":
    main()
