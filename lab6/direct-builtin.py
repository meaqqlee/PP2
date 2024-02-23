import os
import time
import math

def multiply_numbers(numbers):
    return math.prod(numbers)

def count_upper_lower_case(s):
    upper_case = sum(1 for c in s if c.isupper())
    lower_case = sum(1 for c in s if c.islower())
    return upper_case, lower_case

def is_palindrome(s):
    return s == s[::-1]

def invoke_square_root(number, milliseconds):
    time.sleep(milliseconds / 1000)
    return math.sqrt(number)

def all_true(elements):
    return all(elements)

def list_directories_files(path):
    dirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    all_dirs_files = [d for d in os.listdir(path)]
    return dirs, files, all_dirs_files

def check_path_access(path):
    access = {
        "exists": os.path.exists(path),
        "readable": os.access(path, os.R_OK),
        "writable": os.access(path, os.W_OK),
        "executable": os.access(path, os.X_OK)
    }
    return access

def count_lines_in_file(file_path):
    with open(file_path, 'r') as file:
        return sum(1 for _ in file)

def write_list_to_file(file_path, lst):
    with open(file_path, 'w') as file:
        for item in lst:
            file.write(str(item) + '\n')

def generate_files():
    for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        file_name = char + '.txt'
        with open(file_name, 'w') as file:
            file.write("This is file: " + file_name)

def copy_file(source_file, dest_file):
    with open(source_file, 'r') as src, open(dest_file, 'w') as dest:
        dest.write(src.read())

def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        return True
    return False

numbers = [1, 2, 3, 4, 5]
print("Multiply all numbers in list:", multiply_numbers(numbers))

s = "Hello World"
print("Upper case and lower case counts:", count_upper_lower_case(s))

s = "madam"
print("Is palindrome:", is_palindrome(s))

number = 25100
milliseconds = 2123
print(f"Square root of {number} after {milliseconds} milliseconds is {invoke_square_root(number, milliseconds)}")

elements = (True, True, False)
print("All elements are true:", all_true(elements))

path = './test_dir'
print("List directories, files, and all directories, files:", list_directories_files(path))

path = './test_dir'
print("Check path access:", check_path_access(path))

file_path = 'sample.txt'
print("Number of lines in file:", count_lines_in_file(file_path))

lst = ['apple', 'banana', 'cherry']
file_path = 'list.txt'
write_list_to_file(file_path, lst)

generate_files()

source_file = 'sample.txt'
dest_file = 'copy.txt'
copy_file(source_file, dest_file)

file_path = 'copy.txt'
print("Delete file:", delete_file(file_path))
