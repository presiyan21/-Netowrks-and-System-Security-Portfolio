# 🛡️ Malicious Software Analysis

This Python-based toolkit simulates and detects malicious software behaviours using file integrity checks, network activity monitoring, static code signature scanning, and worm propagation modelling.  
The `test_folder` directory includes normal files (e.g. `lecture_notes.txt`, `linear_regression.py`) alongside intentionally malicious scripts (e.g. `test_malware.py`, `encoded_test.py`) used to demonstrate each module.

---

## 🧰 Technologies Used

- **Python ** – primary development language
- **hashlib & pathlib** – SHA-256 hashing and filesystem traversal  
- **csv & time** – structured CSV export and timestamp logging  
- **random & datetime** – simulated network events with time tracking  
- **re (Regular Expressions)** – pattern matching for static code analysis  

---

## ⭐ Main Features

### 🔐 File Integrity Checker — `file_integrity_checker.py`

Generates SHA-256 hashes for all files in `test_folder` and saves them to `file_baseline.csv`, creating a baseline for detecting unauthorised file changes.

### 🌐 Network Traffic Monitor — `network_monitor.py`

Simulates outbound requests from hosts and flags any that exceed the defined `ANOMALY_THRESHOLD`. Alerts are recorded in `network_alerts.csv` to demonstrate anomaly detection.

### 🧬 Static Signature Scanner — `signature_scan.py`

Scans files for suspicious patterns such as `eval()`, `exec()`, `socket.connect`, and `base64.b64decode`, reporting any files that contain potential malicious signatures.

### 🪱 Worm Propagation Simulator — `worm_simulation.py`

Models a self-replicating worm spreading across hosts, showing how infection counts grow each round to illustrate rapid malware propagation.

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
Outputs any files in test_folder containing defined suspicious patterns.

### 4️⃣ Simulate Worm Infection
```bash
python worm_simulation.py
```
Displays infection counts per step to illustrate worm spread dynamics.
