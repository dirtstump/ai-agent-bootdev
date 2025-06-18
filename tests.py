"""tests for get_files_info"""
from functions.write_file import write_file

def main():
    """test funciton for get_files_info"""
    cases = [
        ("calculator", "main.py"),
        ("calculator", "tests.py"),
        ("calculator", "../main.py"),
        ("calculator", "nonexistent.py"),
    ]
    list(map(lambda i: print(write_file(i[0], i[1], i[2])), cases))

if __name__ == "__main__":
    main()
