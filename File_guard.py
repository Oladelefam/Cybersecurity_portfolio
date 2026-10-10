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
                    
write_baseline()


def read_for_hash():

    with open(f'{folder.name} - monitor.txt', 'r') as saved_hash:
        lines = saved_hash.read().splitlines()

    for line_number in range(1, len(lines), 2):
        return lines[line_number]



