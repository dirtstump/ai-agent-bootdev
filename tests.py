"""tests for get_files_info"""
from functions.get_files_info import get_files_info

def main():
    """test funciton for get_files_info"""
    cases = [
        ("calculator", "."),
        ("calculator", "pkg"),
        ("calculator", "/bin"),
        ("calculator", "../"),
    ]
    list(map(lambda i: print(get_files_info(i[0], i[1])), cases))

if __name__ == "__main__":
    main()
