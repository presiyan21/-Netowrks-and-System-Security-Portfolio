# 🛡️ Malicious Software Analysis

This Python-based toolkit simulates and detects malicious software behaviours using file integrity checks, network activity monitoring, static code signature scanning, and worm propagation modelling.  
The `test_folder` directory includes normal files (e.g. `lecture_notes.txt`, `linear_regression.py`) alongside intentionally malicious scripts (e.g. `test_malware.py`, `encoded_test.py`) used to demonstrate each module.

---

## 🧰 Technologies Used

- **Python 3** – primary development language (standard library only)  
- **hashlib & pathlib** – SHA-256 hashing and filesystem traversal  
- **csv & time** – structured CSV export and timestamp logging  
- **random & datetime** – simulated network events with time tracking  
- **re (Regular Expressions)** – pattern matching for static code analysis  

---

## ⭐ Main Features

### 🔐 File Integrity Checker — `file_integrity_checker.py`
Computes SHA-256 hashes for all files in `test_folder` and stores them in `file_baseline.csv` with timestamps, forming a baseline for detecting unauthorized modifications.

### 🌐 Network Traffic Monitor — `network_monitor.py`
Simulates outbound connection attempts for 50 hosts. Any host exceeding `ANOMALY_THRESHOLD` is flagged and logged to `network_alerts.csv`, demonstrating anomaly-based detection.

### 🧬 Static Signature Scanner — `signature_scan.py`
Searches each file for suspicious code patterns such as:
- `eval()`
- `base64.b64decode`
- `socket.connect`
- `exec()`
- `import os`  
Results highlight files containing potentially malicious signatures.

### 🪱 Worm Propagation Simulator — `worm_simulation.py`
Models a self-replicating worm spreading between hosts. Each infected host attempts random infections at each step, printing the total infections per round to visualise rapid malware propagation.

---

## ⚡ How to Run

### 1️⃣ Generate File Baseline
```bash
python file_integrity_checker.py
```
Creates file_baseline.csv with SHA-256 hashes and timestamps.

### 2️⃣ Monitor Network Traffic
```bash
python network_monitor.py
```
Simulates connections and logs anomalies to network_alerts.csv.

### 3️⃣ Scan for Malicious Signatures
```bash
python signature_scan.py
```
###4️⃣ Simulate Worm Infection
```bash
python worm_simulation.py
```
