import os
import string

def list_directories_files(path):
    print("Directories:")
    for item in os.listdir(path):
        if os.path.isdir(os.path.join(path, item)):
            print(item)
    print("\nFiles:")
    for item in os.listdir(path):
        if os.path.isfile(os.path.join(path, item)):
            print(item)
    print("\nAll Directories and Files:")
    for item in os.listdir(path):
        print(item)

def check_access(path):
    print("Existence:", os.path.exists(path))
    print("Readability:", os.access(path, os.R_OK))
    print("Writability:", os.access(path, os.W_OK))
    print("Executability:", os.access(path, os.X_OK))

def path_info(path):
    if os.path.exists(path):
        print("Path exists.")
        print("Filename:", os.path.basename(path))
        print("Directory:", os.path.dirname(path))
    else:
        print("Path does not exist.")

def count_lines(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        print("Number of lines:", len(lines))

def write_list_to_file(file_path, my_list):
    with open(file_path, 'w') as file:
        for item in my_list:
            file.write(item + '\n')

def generate_text_files():
    for letter in string.ascii_uppercase:
        with open(f"{letter}.txt", 'w') as file:
            file.write(f"This is file {letter}.txt")

def copy_file_contents(source, destination):
    with open(source, 'r') as src:
        with open(destination, 'w') as dest:
            dest.write(src.read())

def delete_file(file_path):
    if os.path.exists(file_path) and os.access(file_path, os.W_OK):
        os.remove(file_path)
        print(f"File {file_path} has been deleted.")
    else:
        print(f"Cannot delete {file_path}. Check if the file exists and has write access.")

list_directories_files('.')
check_access('example.txt')
path_info('example.txt')
count_lines('example.txt')
write_list_to_file('list.txt', ['apple', 'banana', 'cherry'])
generate_text_files()
copy_file_contents('source.txt', 'destination.txt')
delete_file('file_to_delete.txt')