import re
from pathlib import Path

# Define suspicious patterns (signatures)
SIGNATURES = [
    r"eval\(",
    r"base64\.b64decode",
    r"socket\.connect",
    r"exec\(",
    r"import os"
]


def scan_file(file_path: Path, patterns: list) -> list:
    """Scan a single file for any signature matches and return a list of matches."""
    matches = []
    try:
         # Read as text
        content = file_path.read_text(errors="ignore")  # ignore non-text files
        for pattern in patterns:
            if re.search(pattern, content):
                matches.append(pattern)
    except Exception as e:
        print(f"Could not read {file_path}: {e}")
    return matches


def scan_folder(folder: str):
    """Scan all files in a folder and report suspicious matches."""
    folder = Path(folder)
    report = {}

    for file in folder.rglob("*"):
        if file.is_file():
            matches = scan_file(file, SIGNATURES)
            if matches:
                report[str(file)] = matches

    print("\n----- Signature Scan Report -----")
    if not report:
        print("No suspicious patterns detected.")
    else:
         # Show each flagged file and its matched signatures
        for file, patterns_found in report.items():
            print(f"{file} -> Matches: {patterns_found}")
    print("--------------------------------\n")

if __name__ == "__main__":
    scan_folder("test_folder")
