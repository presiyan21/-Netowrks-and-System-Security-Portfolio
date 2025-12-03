# 🔍 Penetration Testing Toolkit

A Python-based application designed to perform reconnaissance and scanning for penetration testing exercises.  
The toolkit demonstrates how domain lookup, passive web enumeration, multi-threaded port scanning, and Nmap-based service enumeration can be combined to simulate early-stage penetration tests in a safe and controlled environment.

---

## 🧰 Technologies Used

- **Python 3** – Core development language throughout the project  
- **requests** – Sends HTTP requests for passive reconnaissance  
- **socket** – Implements TCP port scanning  
- **concurrent.futures** – Enables multi-threaded port scanning  
- **python-nmap** – Integrates Nmap functionality for service enumeration  
- **os / pathlib** – Supports structured file handling and reporting  

---

## ⭐ Main Features

- Performs **domain lookup** and resolves IP addresses  
- Conducts **passive web enumeration** to collect HTTP headers  
- Executes **threaded TCP port scans** for faster discovery  
- Integrates **Nmap service detection** for detailed port and service info  
- Writes **timestamped structured reports** suitable for academic or professional review  
- Implements **SAFE_MODE** to prevent unauthorized scanning of external hosts  
- Supports **configurable target domains and ports** for flexible testing  
- Modular design allows easy extension for additional reconnaissance or scanning features  

## ⚡ How to Run Locally


1. 1️⃣ **Install required packages**  
```bash
pip install -r requirements.txt
```


2. 2️⃣ **Run the main application**  
```bash
python main.py
```

3. 3️⃣ **View the output**  
Results are written to `report.txt` and include:  
- Domain IP resolution and metadata  
- Passive web header enumeration  
- Open ports detected by threaded scanner  
- Service and version information from Nmap

![alt text](image.png)

---

## 🧩 System Architecture

![alt text](<Screenshot 2025-11-23 154526.png>)