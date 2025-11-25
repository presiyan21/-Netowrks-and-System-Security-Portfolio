import re

def extract_strings(file_path, min_length=4):
    """Extract printable ASCII strings from a binary file."""
    with open(file_path, 'rb') as f:
        data = f.read()

    # Match printable characters
    pattern = rb"[ -~]{%d,}" % min_length
    raw_strings = re.findall(pattern, data)

    # Decode to text and ignore invalid bytes
    return [s.decode(errors='ignore') for s in raw_strings]
