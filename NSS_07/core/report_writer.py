from core.utils import timestamp

def write_report(title, data, path="report.txt"):
    with open(path, "a") as f:
        f.write(f"\n=== {title} ({timestamp()}) ===\n")
        for line in data:
            f.write(f"{line}\n")
    return path
