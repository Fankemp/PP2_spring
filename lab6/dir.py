import os
import shutil
import string

# 1. Function to show folders and files in a given directory
def show_files_and_dirs(path):
    if not os.path.exists(path):
        print("This path does not exist!")
        return
    
    folders = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    print("Folders:", folders)
    print("Files:", files)
    print("All contents:", os.listdir(path))

# 2. Function to check if a path exists and its access permissions
def check_path(path):
    print(f"Exists? {os.path.exists(path)}")
    print(f"Readable? {os.access(path, os.R_OK)}")
    print(f"Writable? {os.access(path, os.W_OK)}")
    print(f"Executable? {os.access(path, os.X_OK)}")

# 3. Function to check file information
def check_file_info(path):
    if os.path.exists(path):
        print("This path exists!")
        print("Folder:", os.path.dirname(path))
        print("File:", os.path.basename(path))
    else:
        print("This path does not exist!")

# 4. Function to count the number of lines in a file
def count_lines(file_path):
    try:
        with open(file_path, 'r') as file:
            return len(file.readlines())
    except FileNotFoundError:
        print("File not found!")
        return 0

# 5. Function to save a list to a file
def save_list_to_file(file_path, items):
    with open(file_path, 'w') as file:
        for item in items:
            file.write(item + "\n")
    print(f"List saved to {file_path}")

# 6. Function to create 26 text files from A.txt to Z.txt
def create_files():
    for letter in string.ascii_uppercase:
        with open(f"{letter}.txt", 'w') as file:
            file.write(f"This is file {letter}.txt\n")
    print("Files A-Z created!")

# 7. Function to copy a file
def copy_file(source, destination):
    try:
        shutil.copy(source, destination)
        print(f"File {source} copied to {destination}")
    except FileNotFoundError:
        print("Source file not found!")

# 8. Function to delete a file
def delete_file(file_path):
    if os.path.exists(file_path):
        if os.access(file_path, os.W_OK):
            os.remove(file_path)
            print(f"File {file_path} deleted!")
        else:
            print("No permission to delete the file!")
    else:
        print("File does not exist!")