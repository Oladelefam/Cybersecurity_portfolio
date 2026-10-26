"""🛡️ Cybersecurity Project Brief — File Integrity Monitor
Project title

FileGuard — File Integrity Monitoring System

Difficulty

Beginner → Intermediate

Objective

Build a Python cybersecurity tool that monitors a selected folder and detects when files have been modified, created, or deleted.

The system should establish what the files looked like originally and then compare their current state against that baseline.
"""

import hashlib
import json
from pathlib import Path


TRACKED_BASELINES = Path("file_that_has_been_checked.txt")


def baseline_path(folder_name):
    """Return the baseline file for a folder name in the current working directory."""
    name = Path(folder_name).name
    if not name:
        raise ValueError("A folder name is required.")
    return Path.cwd() / f"{name} - monitor.txt"


def scan_folder(folder):
    """Return hashes keyed by paths relative to the monitored folder."""
    folder = Path(folder).expanduser().resolve()
    if not folder.exists():
        raise FileNotFoundError(f"Folder does not exist: {folder}")
    if not folder.is_dir():
        raise NotADirectoryError(f"Not a folder: {folder}")

    hashes = {}
    excluded_paths = {
        baseline_path(folder.name).resolve(),
        TRACKED_BASELINES.resolve(),
    }
    for file_path in folder.rglob("*"):
        if file_path.is_file() and file_path.resolve() not in excluded_paths:
            relative_path = file_path.relative_to(folder).as_posix()
            file_hash = hashlib.sha256()
            with file_path.open("rb") as file:
                for chunk in iter(lambda: file.read(4096), b""):
                    file_hash.update(chunk)
            hashes[relative_path] = file_hash.hexdigest()
    return hashes


def _register_baseline(path):
    baseline_name = path.name
    tracked = []
    if TRACKED_BASELINES.exists():
        with TRACKED_BASELINES.open("r", encoding="utf-8") as file:
            tracked = [line.strip() for line in file if line.strip()]
    if baseline_name not in tracked:
        with TRACKED_BASELINES.open("a", encoding="utf-8") as file:
            file.write(f"{baseline_name}\n")


def write_baseline(folder):
    """Create or explicitly update a folder's saved baseline."""
    folder = Path(folder).expanduser().resolve()
    hashes = scan_folder(folder)
    path = baseline_path(folder.name)
    with path.open("w", encoding="utf-8") as file:
        json.dump(
            {"root": str(folder), "files": hashes},
            file,
            indent=2,
            sort_keys=True,
        )
        file.write("\n")
    _register_baseline(path)
    return hashes


def _legacy_root(folder_name, paths):
    selected_path = Path(folder_name).expanduser()
    if selected_path.is_dir():
        return selected_path.resolve()

    folder_basename = selected_path.name
    for saved_path in paths:
        path = Path(saved_path)
        if path.is_absolute():
            for parent in (path.parent, *path.parents):
                if parent.name == folder_basename:
                    return parent
    return selected_path.resolve()


def _load_baseline(folder_name):
    path = baseline_path(folder_name)
    with path.open("r", encoding="utf-8") as file:
        contents = file.read()

    try:
        data = json.loads(contents)
    except json.JSONDecodeError:
        lines = contents.splitlines()
        if len(lines) % 2:
            raise ValueError(f"Invalid legacy baseline format: {path}")
        saved_paths = lines[::2]
        root = _legacy_root(folder_name, saved_paths)
        files = {}
        for saved_path, file_hash in zip(saved_paths, lines[1::2]):
            saved_file = Path(saved_path)
            if saved_file.is_absolute():
                try:
                    relative_path = saved_file.resolve().relative_to(root).as_posix()
                except ValueError as error:
                    raise ValueError(
                        f"Baseline path is outside the monitored folder: {saved_path}"
                    ) from error
            else:
                relative_path = saved_file.as_posix()
                folder_prefix = Path(folder_name).name
                if relative_path.startswith(f"{folder_prefix}/"):
                    relative_path = relative_path[len(folder_prefix) + 1 :]
            files[relative_path] = file_hash
        return root, files

    if not isinstance(data, dict) or not isinstance(data.get("files"), dict):
        raise ValueError(f"Invalid baseline format: {path}")
    root = Path(data["root"]).expanduser().resolve()
    files = data["files"]
    if not all(
        isinstance(relative_path, str) and isinstance(file_hash, str)
        for relative_path, file_hash in files.items()
    ):
        raise ValueError(f"Invalid path/hash data in baseline: {path}")
    return root, files


def read_for_hash(folder_name):
    """Read a baseline as a mapping of relative paths to hashes."""
    _, files = _load_baseline(folder_name)
    return files


def monitor_folder(folder):
    """Compare the current folder with its saved baseline and report file changes."""
    selected_folder = Path(folder).expanduser()
    root, saved_hashes = _load_baseline(selected_folder.name)
    if selected_folder.is_dir():
        selected_root = selected_folder.resolve()
        if selected_root != root:
            raise ValueError(
                f"The selected folder does not match this baseline: {selected_root}"
            )

    current_hashes = scan_folder(root)
    added = current_hashes.keys() - saved_hashes.keys()
    deleted = saved_hashes.keys() - current_hashes.keys()
    common = current_hashes.keys() & saved_hashes.keys()
    modified = {
        path for path in common if current_hashes[path] != saved_hashes[path]
    }
    unchanged = common - modified

    for status, paths in (
        ("MODIFIED", modified),
        ("ADDED", added),
        ("DELETED", deleted),
        ("UNCHANGED", unchanged),
    ):
        for relative_path in sorted(paths):
            print(f"{status}: {relative_path}")

    return bool(added or deleted or modified)


def delete_baseline(folder_name):
    """Delete only the selected baseline file and remove its registry entry."""
    path = baseline_path(folder_name)
    if path.parent.resolve() != Path.cwd().resolve():
        raise ValueError("Refusing to delete a baseline outside the current directory.")
    if not path.is_file():
        raise FileNotFoundError(f"Baseline does not exist: {path}")
    path.unlink()

    if TRACKED_BASELINES.exists():
        with TRACKED_BASELINES.open("r", encoding="utf-8") as file:
            tracked = file.readlines()
        with TRACKED_BASELINES.open("w", encoding="utf-8") as file:
            for line in tracked:
                if line.strip() != path.name:
                    file.write(line)


def main():
    user_input = input(
        "Enter the folder name or path to monitor (enter S to create a baseline): "
    ).strip()

    if user_input.lower() == "s":
        folder_input = input("Enter the folder path: ").strip().strip('"')
        folder = Path(folder_input).expanduser().resolve()
        write_baseline(folder)
        folder_name = folder.name
    else:
        folder = Path(user_input).expanduser()
        folder_name = folder.name

    baseline = baseline_path(folder_name)
    if not baseline.is_file():
        print(f"No saved baseline found for {folder_name}.")
        return

    choice = input(
        """
1. Show file-level report (type reports)
2. Read the saved baseline (type read)
3. Update the baseline (type update)
4. Delete the baseline (type delete)
Q. Quit
Choice: """
    ).strip().lower()

    if choice == "reports":
        monitor_folder(folder)
    elif choice == "read":
        for relative_path, file_hash in sorted(read_for_hash(folder_name).items()):
            print(f"{relative_path}: {file_hash}")
    elif choice == "update":
        root, _ = _load_baseline(folder_name)
        write_baseline(root)
        print("Baseline updated.")
    elif choice == "delete":
        delete_baseline(folder_name)
        print("Baseline deleted.")
    elif choice not in ("q", "quit"):
        print("Unrecognized choice.")


if __name__ == "__main__":
    main()
