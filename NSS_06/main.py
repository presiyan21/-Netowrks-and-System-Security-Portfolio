from analysis.hashing import compute_hashes
from analysis.strings import extract_strings
from analysis.pe_analysis import inspect_pe
from analysis.ioc import extract_iocs
from analysis.yara_analysis import match_yara

sample_file = "samples/hello.exe"

# YARA rule example
rule_source = """
rule ContainsHTTP {
    strings:
        $s = "http"
    condition:
        $s
}
"""

# Compute Hashes
hashes = compute_hashes(sample_file)
print("=== File Hashes ===")
for k, v in hashes.items():
    print(f"{k.upper()}: {v}")

# Extract Strings
strings = extract_strings(sample_file)
print("\n=== Extracted Strings (Top 10) ===")
for s in strings[:10]:
    print(s)

# PE Inspection
pe_info = inspect_pe(sample_file)
print("\n=== PE Info ===")
print(f"Entry Point: {pe_info['entry_point']}")
print(f"Image Base: {pe_info['image_base']}")
print("Imports:")
for dll, funcs in pe_info['imports'].items():
    print(f" {dll}: {funcs[:5]}")

# IOC Extraction
iocs = extract_iocs(sample_file)
print("\n=== Extracted IOCs ===")
print("URLs:", iocs['urls'])
print("IPs:", iocs['ips'])

# YARA Matching
matches = match_yara(sample_file, rule_source)
print("\n=== YARA Matches ===")
print(matches)
