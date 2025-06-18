"""tests for get_files_info"""
from functions.run_python import run_python_file

def main():
    """test funciton for get_files_info"""
    cases = [
        ("calculator", "main.py"),
        ("calculator", "tests.py"),
        ("calculator", "../main.py"),
        ("calculator", "nonexistent.py"),
    ]
    list(map(lambda i: print(run_python_file(i[0], i[1])), cases))

if __name__ == "__main__":
    main()
