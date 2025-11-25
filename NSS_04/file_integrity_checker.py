import hashlib
import csv
import time
from pathlib import Path


def hash_file(path: Path) -> str:
    """Return the SHA-256 hash of the file."""
    sha256 = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(4096), b""):
            sha256.update(block)
    return sha256.hexdigest()


def generate_baseline(directory: str, output_csv: str = "file_baseline.csv") -> None:
    """Scan all files in a folder and save their hashes to a CSV baseline."""
    directory = Path(directory)
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["File Name", "SHA-256 Hash", "Timestamp"])
        
        # Hash every file and store the results
        for file in directory.rglob("*"):
            if file.is_file():
                file_hash = hash_file(file)
                writer.writerow([str(file), file_hash, timestamp])

    print(f"Baseline created: {output_csv}")

if __name__ == "__main__":
    generate_baseline("test_folder")
