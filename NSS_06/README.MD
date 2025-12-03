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

![alt text](<Screenshot 2025-11-20 160608.png>)

## 🧪 Lab Report