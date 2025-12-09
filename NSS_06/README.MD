# 🔍 Malware Analysis Toolkit

A Python-based application designed to analyse Windows executable files using automated static analysis techniques.  
The toolkit demonstrates how hashing, string extraction, PE-file inspection, IOC identification, and YARA-rule matching can be combined to support early-stage malware assessment.

---

## 🧰 Technologies Used

- **Python 3** – core development language used throughout the project  
- **pefile** – parses PE (Portable Executable) headers and metadata  
- **yara-python** – enables pattern-based malware signature matching  
- **hashlib** – computes cryptographic file hashes (MD5, SHA-1, SHA-256)  
- **re** – supports regular-expression based IOC extraction  
- **PyInstaller** – used to compile sample executables for testing  
- **os / pathlib** – supports structured file handling within the application  

---

## ⭐ Main Features

- Generates three cryptographic hashes for integrity and identification  
- Extracts readable strings from binaries for manual inspection  
- Analyses PE files to retrieve imports, entry point, and image base  
- Identifies Indicators of Compromise such as URLs and IP addresses  
- Evaluates files using YARA rules to detect suspicious patterns  
- Provides structured terminal output suitable for academic reporting  
- Includes a dedicated **samples** directory for controlled testing  

---

## ⚡ How to Run

### 1️⃣ Install all required packages
```bash
pip install -r requirements.txt
```

### 2️⃣ Add a sample executable for testing

### 3️⃣ Run the analysis tool
```bash
python main.py
```

### 4️⃣ View the output
Results will display in the terminal.

![alt text](<Screenshot 2025-11-20 121029.png>)

## 🧩 System Architecture

![alt text](<Screenshot 2025-11-23 154526.png>)

## 🧪 Lab Report

## Modules, methods and examples

Earlier presented and illustrated outputs and behaviours are produced by the files in analysis/ and orchestrated in 
`main.py`.

### **Hashing (hashing.py)**

Integrated into the system with the purpose of computing **MD5, SHA1, and SHA256 .**[1] The code behind it loads the file and computes each digest. The process of reading whole files for smaller files doesn’t induce additional errors; however, many could be observed when working with large files and applications. Therefore, a built-in drop optimisation computes hashes in a single pass without reading the whole file. Allowing us to reduce peak memory, hence preserving the code's robustness for large binaries.

```python
h_dict = {algo: hashlib.new(algo) for algo in algorithms} [3]
with open(file_path, 'rb') as f:
    for block in iter(lambda: f.read(8192), b''):
        for h in h_dict.values():
            h.update(block)
hashes = {a: h.hexdigest() for a,h in h_dict.items()}
```

**main.py output:**
```python
 MD5: 8e88ea01fc1fece5ab611e3a42181bbd
 SHA1: ed6ceed3ee85acb90e54e15211…
 SHA256: 6b2e2eabe78c2c0ac78397f4b…
```
**Why this matters:** *hashes are canonical IOCs used for sharing and quick reputation checks [2].*

---

### **String extraction (strings.py)**

**What it does:** finds printable ASCII sequences using:

```python
pattern = rb"[ -~]{%d,}" % min_length [4]
raw_strings = re.findall(pattern, data)
return [s.decode(errors='ignore') for s in raw_strings] [6]
```

This precisely mirrors strings utilities (ASCII range 0x20–0x7E) [4].

**Top strings from the run:**

",}@Z"
".rdata"
".pdata"
"@.fptable"
"@.reloc"

**Trade-offs:**

The purpose of `errors='ignore' is to prevent crashes; however, it may result in potential bottlenecks by hiding malformed encodings. My approach was to keep `min_length` tunable (default 4) and to optionally produce byte offsets for forensic traceability.

---

### **PE inspection (pe_analysis.py)**

**What it does:** uses `pefile` to report entry point, image base, and imports. Key lines:

```python
entry_point = hex(pe.OPTIONAL_HEADER.AddressOfEntryPoint) [5]
image_base  = hex(pe.OPTIONAL_HEADER.ImageBase)
for entry in pe.DIRECTORY_ENTRY_IMPORT:
    dll_name = entry.dll.decode()
    func_names = [imp.name.decode() if imp.name else "None" for imp in entry.imports]
```

**Example output (actual run):**

* Entry Point: `0xcf30`
* Image Base: `0x140000000`
* USER32.dll: `['TranslateMessage','ShutdownBlockReasonCreate', 'GetWindowThreadProcessId', 'SetWindowLongPtrW', 'GetWindowLongPtrW']`
* KERNEL32.dll:`['GetTimeZoneInformation', 'GetProcessHeap','FreeEnvironmentStringsW', 'GetEnvironmentStringsW', 'GetPInfo']`
* ADVAPI32.dll:`['ConvertSidToStringSidW', 'GetTokenInformation', 'OpenProcessToken', 'ConvertStringSecurityDescriptorToSecurityDescriptorW']`

**Analysis:**

Malware triage facilitates the preview of suspicious imports (e.g.,**VirtualAllocEx**,**CreateRemoteThread**, **GetProcAddress**), some of which could be considered as indicators of code injection or dynamic resolution. `ShutdownBlockReasonCreate` and various ADVAPI functions were observed during experimentation, **not necessarily associated with malicious software**, which highlights that the correlation between suspicious scripts and malware doesn’t always apply.

To further account for various files `Pefile.PE()` can raise `pefile.PEFormatError` for corrupt/non-PE files [5].

---

### **IOC extraction (ioc.py)**

**What it does:** extracts URLs and IPv4 tokens:

```python
urls = re.findall(r'https?://[^\s"'<>]+', data) [8]
ips  = re.findall(r'\b\d{1,3}(?:\.\d{1,3}){3}\b', data)
```

The URL regex is pragmatic for triage; the IP regex is to be compatible with real-world applications that would require post-filtering (0–255 checks), hence avoiding the conflict of working with non-existing addresses. By accounting for the module returns a dict with URLs and IPs for quick IOC submission to a SIEM or TI platform.

**Example extraction from the actual run:**

* URLs found: `['http://schemas.microsoft.com/SMI/2016/WindowsSettings']`
* IPs found: `['6.0.0.0']`

`6.0.0.0` not an insightful IPv4 host in most contexts, implying that it would be filtered out by an industry-configured IP validation system. Therefore, opt for a permissive regex with the improved pattern below to reduce impossible addresses. However, for the purpose of my application, we would stick with the simple version.

**Real-world script:**

```python
ips = re.findall(r'\b(?:25[0-5]|2[0-4]\d|1?\d{1,2})(?:\.(?:25[0-5]|2[0-4]\d|1?\d{1,2})){3}\b', data)
```

---

### **YARA matching (yara_analysis.py)**

**What it does:** compiles a YARA rule and matches it on disc:

```python
rules = yara.compile(source=rule_source) [7]
return rules.match(file_path)
```

**main.py uses a minimal rule:**

```text
rule ContainsHTTP {
  strings: $s = "http"
  condition: $s
}
```

In this run the minimal rule matched (the report shows `ContainsHTTP`), the root of which was found to be the presence of the URL found by the IOC extraction.

---

## Challenges & Errors

### **Intermittent pefile.PEFormatError in batch runs**

**Before:**

pefile.PE() calls inside multithreaded workflows triggered sporadic crashes when encountering malformed or non-PE files.

**Fix:**

Use a try/except wrapper so invalid files are skipped cleanly:

```python
try:
    pe = pefile.PE(file_path) [5]
except pefile.PEFormatError:
    return None 
```

**Effect:**

Batch processing continues without interruption; “invalid PE” inputs are safely reported for review.

---

### **Overly permissive IP regex → false positives**

The latest run extracted the IP `6.0.0.0`, which is not a meaningful IOC and demonstrates the weakness of the original regex.

**Before:**

```python
r'\d{1,3}(\.\d{1,3}){3}'
```

**After (improved, range-validated):**

```python
ips = re.findall(
    r'\b(?:25[0-5]|2[0-4]\d|1?\d{1,2})'
    r'(?:\.(?:25[0-5]|2[0-4]\d|1?\d{1,2})){3}\b',
    data
)
```

**Effect:**

Eliminates impossible IPv4 addresses (e.g., `999.999.999.999`) and removes noisy tokens like `6.0.0.0`, improving IOC quality for SIEM/TI ingestion.

---

### **Concurrency: pefile not thread-safe**

**Problem:**

Initial attempts to parallelise PE inspection using threads caused race conditions and unpredictable failures, particularly when processing large batches of samples.

**Fix:**

Switch from threads to process-based parallelism:

* `concurrent.futures.ProcessPoolExecutor`, or
* dedicated subprocesses for PE inspection. [9]

Processes isolate `pefile`’s internal state.

**Effect:**

Deterministic behaviour across large workloads, improved throughput on multi-core systems, and full stability during parallel analysis operations.

## References

[1] National Institute of Standards and Technology (2015) *FIPS 180-4: Secure Hash Standard (SHS)*. Available at: https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf

[2] VirusTotal (2024) *VirusTotal Intelligence — searching by file hash and metadata*. Available at: https://docs.virustotal.com/docs/virustotal-intelligence-introduction

[3] Python Software Foundation *hashlib — Secure hashes and message digests*. Available at: https://docs.python.org/3/library/hashlib.html

[4] Linux manual pages  *strings(1) — print printable character sequences in files*. Available at: https://man7.org/linux/man-pages/man1/strings.1.html

[5] Ero Carrera (pefile project) *pefile — Portable Executable (PE) reader for Python*. Available at: https://pefile.readthedocs.io/en/latest/modules/pefile.html

[6] Python Software Foundation *codecs — Codec registry and base classes*. Available at: https://docs.python.org/3/library/codecs.html

[7] Victor Alvarez et al. (YARA project) *YARA documentation — Using YARA from Python (yara-python)*. Available at: https://yara.readthedocs.io/en/stable/yarapython.html

[8] Jan Goyvaerts *How to find or validate an IP address* — Regular-Expressions.info. Available at: https://www.regular-expressions.info/ip.html

[9] Python Software Foundation *concurrent.futures — Launching parallel tasks (ProcessPoolExecutor)*. Available at: https://docs.python.org/3/library/concurrent.futures.html

