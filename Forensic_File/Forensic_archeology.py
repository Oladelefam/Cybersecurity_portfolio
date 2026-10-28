"""
# Project Brief: Forensic File Archaeology Tool

## 1. Project Overview
**Project name:** Forensic File Archaeology Tool  
**Language:** Python  
**Primary library:** `pathlib`  
**Difficulty:** Intermediate to Advanced

## 2. Objective
Develop a command-line tool that analyses a directory and its contents to produce a detailed filesystem report. The project aims to master Python's `pathlib` library while developing practical skills in filesystem analysis, metadata collection, file integrity checking and basic digital forensics.

## 3. Core Features

### Phase 1: Filesystem Mapping
- Recursively scan directories and subdirectories.
- Generate a directory tree.
- Count files and directories.
- Calculate total file sizes.
- Identify empty directories.

### Phase 2: File Analysis
- Extract file names, extensions, parent directories and paths.
- Find files by extension, size and modification time.
- Identify files with unusual or misleading extensions.
- Handle files without extensions and compound extensions.

### Phase 3: Evidence Collection
- Calculate SHA-256 hashes to identify files with identical contents.
- Record file paths and relevant metadata.
- Save filesystem snapshots in JSON format.
- Compare snapshots to detect added, removed or modified files.

### Phase 4: Reporting and Reliability
- Generate readable TXT and JSON reports.
- Accept directory paths through command-line arguments.
- Handle inaccessible files, broken symbolic links and filesystem changes during scanning.
- Keep the original files unmodified.

## 4. Technical Requirements
- Use `pathlib` for path manipulation and filesystem operations.
- Use `hashlib` for SHA-256 hashing.
- Use `json` for storing snapshots and reports.
- Use `argparse` for command-line arguments.
- Use `unittest` or `pytest` to test functionality.
- Use temporary directories to create safe test environments.

## 5. Learning Objectives
By completing the project, I should be able to:
- Confidently use `Path`, `PurePath`, `glob()`, `rglob()`, `iterdir()` and `stat()`.
- Understand path components, absolute paths, relative paths and symbolic links.
- Read, write and inspect files using pathlib.
- Handle filesystem errors and edge cases.
- Design reusable functions and write meaningful tests.
- Understand how file hashing and metadata snapshots support digital investigations.

## 6. Development Constraints
- Use `pathlib` instead of `os.path` for path manipulation.
- Avoid copying complete implementations from tutorials or AI.
- Keep the initial tool read-only.
- Do not automatically delete, rename or move files.
- Avoid following symbolic links in ways that could cause directory loops or duplicate counting.
- Do not treat file extensions or timestamps alone as proof of malicious activity.

## 7. Success Criteria
The project is complete when the tool can reliably scan a test directory, analyse its contents, detect duplicate files, create and compare snapshots, export reports, and handle common filesystem errors. Its core functions must be tested, documented and usable through the command line.

## 8. Final Deliverable
A documented Python command-line application, accompanied by source code, automated tests, sample reports and a README explaining installation, usage, limitations and design decisions.

**Primary goal:** Master `pathlib` through a realistic filesystem investigation project while building a useful cybersecurity portfolio project.

"""