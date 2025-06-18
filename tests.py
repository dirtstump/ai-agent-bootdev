"""tests for get_files_info"""
from functions.write_file import write_file

def main():
    """test funciton for get_files_info"""
    cases = [
        ("calculator", "lorem.txt", "wait, this isn't lorem ipsum"),
        ("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"),
        ("calculator", "/tmp/temp.txt", "this should not be allowed"),
    ]
    list(map(lambda i: print(write_file(i[0], i[1], i[2])), cases))

if __name__ == "__main__":
    main()
