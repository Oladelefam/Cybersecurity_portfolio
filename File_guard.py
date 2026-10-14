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


File_dir = input("Enter the file directory: ").strip(' " ')
folder = Path(File_dir)

def write_baseline():

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
            fil.write(f"{folder.name} - monitor.txt")
                    

# So basically if i have multiple file baselines I need to get the user input to see what file they want to check so read_for_hash needs a folder name


def read_for_hash(folder_name):

    with open(f'{folder.name} - monitor.txt', 'r') as saved_hash:
        lines = saved_hash.read().splitlines()
    Hashes = []
    for line_number in range(1, len(lines), 2):
        Hashes.append(lines[line_number])

    return Hashes



def monitor_folder():
    """ Needs to detect change in baseline """
    monfold = read_for_hash
    print(monfold)

User_input = input("Enter the folder you wish to monitor: ").strip(' ')

with open("file_that_has_been_checked.txt", 'r') as read_file:
 
    read = read_file.readline().splitlines()
    for item in read:
        if item == User_input:
            monitor_folder(User_input)

