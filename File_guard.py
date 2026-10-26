"""🛡️ Cybersecurity Project Brief — File Integrity Monitor
Project title

FileGuard — File Integrity Monitoring System

Difficulty

Beginner → Intermediate

Objective

Build a Python cybersecurity tool that monitors a selected folder and detects when files have been modified, created, or deleted.

The system should establish what the files looked like originally and then compare their current state against that baseline.
"""





from hashlib import *
from pathlib import *
import os
import shutil
import logging




def write_baseline(folder):
    folder = Path(folder)

    if folder.exists():
        hashes = []

        for i in folder.rglob("*"):
            if i.is_dir():
                print(f"[DIR]    {i}")
            else:
                print(f"    |______ {i}")

                file_hash = sha256()
                with i.open("rb") as f:
                    for chunk in iter(lambda: f.read(4096), b""):
                        file_hash.update(chunk)

                hashes.append((i, file_hash.hexdigest()))


        with open(f"{folder.name} - monitor.txt", "w") as file:
            for path, file_hash in hashes:
                file.write(f"{path}\n{file_hash}\n")

        with open("file_that_has_been_checked.txt", 'a') as fil:
            fil.write(f"{folder.name} - monitor.txt\n")
                    

# So basically if i have multiple file baselines I need to get the user input to see what file they want to check so read_for_hash needs a folder name


def read_for_hash(folder_name):

    with open(f'{Path(folder_name).name} - monitor.txt', 'r') as saved_hash:
        lines = saved_hash.read().splitlines()
    Hashes = []
    for line_number in range(1, len(lines), 2):
        Hashes.append(lines[line_number])

    return Hashes



def monitor_folder(folder):
    """ Needs to detect change in baseline and highlight towrds the end gives whether the file has been modified in anyway """
    folder = Path(folder)
    modified = False
    monfold = read_for_hash(folder)
    newbase = write_baseline(folder)

    if newbase == monfold:
        modified = True
        print("This file has been editted either through deleting or changes")
    else:
        modified = False
        print("This file hasn't been editted")


    return modified


    
User_input = input("Enter the folder/file you wish to monitor(if file never been scanned press S): ").strip(' ')

if User_input == "S":
    File_dir = input("Enter the file directory: ").strip(' " ')
    folder = Path(File_dir)
    write_baseline(folder)
    User_input = folder.name
else:
    folder = Path(User_input)


with open("file_that_has_been_checked.txt", "r") as read_file:
    checked_files = [line.strip() for line in read_file]

if f"{User_input} - monitor.txt" in checked_files:
    Choices = input("""
    1. Read file reports (type reports)
    2. Read file baseline (type read)
    3. Delete baseline (type Delete)
    (Q to quit): """).strip().capitalize()

    if Choices == "Reports":
        monitor_folder(folder)
    elif Choices == "Read":
        read_for_hash(folder)
    elif Choices == "Delete":
        if os.path.exists(folder):
            if folder.is_dir:
                os.rmdir(folder)
            else:
                os.remove(f"{folder.name} - monitor.txt")

            with open("file_that_has_been_checked.txt", 'r') as del_file:
                dels = del_file.readlines()

            with open("file_that_has_been_checked.txt", 'w') as del_file:
                for delt in dels:
                    if f"{folder.name} - monitor.txt" not in delt:
                        del_file.write(delt)
else:
    print("That folder has no saved baseline.")
