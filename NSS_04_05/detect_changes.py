import hashlib
import csv
from pathlib import Path


def hash_file(path: Path) -> str:
    """Return the SHA-256 hash of the file."""
    sha256 = hashlib.sha256()
    with open(path, "rb") as f:
        # Read file in chunks to handle large files efficiently
        for block in iter(lambda: f.read(4096), b""):
            sha256.update(block)
    return sha256.hexdigest()


def load_baseline(csv_file: str) -> dict:
    """Load baseline hashes from CSV into a dictionary."""
    baseline = {}
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        # Map file paths to their saved hash values
        for row in reader:
            baseline[row["File Name"]] = row["SHA-256 Hash"]
    return baseline


def detect_changes(directory: str, baseline_csv: str = "file_baseline.csv") -> None:
    """Compare current file hashes to the baseline and report changes."""
    directory = Path(directory)
    baseline = load_baseline(baseline_csv)

    current_hashes = {}
    # Hash all files currently in the directory
    for file in directory.rglob("*"):
        if file.is_file():
            current_hashes[str(file)] = hash_file(file)

    modified = []
    deleted = []
    created = []

    # Check for modified or deleted files
    for file, old_hash in baseline.items():
        if file not in current_hashes:
            deleted.append(file)
        elif current_hashes[file] != old_hash:
            modified.append(file)
    
    # Check for new files not in the baseline
    for file in current_hashes:
        if file not in baseline:
            created.append(file)

    print("\n----- File Change Report -----")
    print(f"Modified: {modified or 'None'}")
    print(f"Deleted:  {deleted or 'None'}")
    print(f"Created:  {created or 'None'}")
    print("--------------------------------\n")

if __name__ == "__main__":
    detect_changes("test_folder")