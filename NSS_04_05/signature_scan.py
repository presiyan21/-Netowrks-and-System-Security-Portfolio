import re
from pathlib import Path

# Suspicious patterns
SIGNATURES = [
    r"\beval\s*\(",          
    r"base64\.b64decode",    
    r"socket\.connect",      
    r"\bexec\s*\(",          
    r"import\s+os"           
]

# Pre-compile regexes for speed
COMPILED = [re.compile(p) for p in SIGNATURES]


def scan_file(file_path: Path, compiled_patterns: list) -> list:
    """Scan a single file for any signature matches and return a list of matched patterns."""
    matches = []
    try:
        content = file_path.read_text(errors="ignore")  # ignore non-text bytes
        for pat in compiled_patterns:
            found = pat.findall(content)
            if found:
                # show the pattern and some matched substrings
                matches.append({"pattern": pat.pattern, "matches": list(set(found))})
    except Exception as e:
        print(f"Could not read {file_path}: {e}")
    return matches


def scan_folder(folder: str):
    """Scan all files in a folder and report suspicious matches."""
    folder = Path(folder)
    print(f"Scanning folder: {folder.resolve()}\n")
    report = {}

    for file in folder.rglob("*"):
        if file.is_file():
            print(f"Scanning: {file}")
            matches = scan_file(file, COMPILED)
            if matches:
                report[str(file)] = matches

    print("\n----- Signature Scan Report -----")
    if not report:
        print("No suspicious patterns detected.")
    else:
        for file, patterns_found in report.items():
            print(f"{file} ->")
            for entry in patterns_found:
                print(f"    pattern: {entry['pattern']}  matches: {entry['matches']}")
    print("--------------------------------\n")


if __name__ == "__main__":
    scan_folder(Path(__file__).parent / "test_folder")

