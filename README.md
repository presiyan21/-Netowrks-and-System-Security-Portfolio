<!-- CUSTOM BANNER -->
<p align="center">
  <img width="900" src="https://svg-banners.vercel.app/api?type=origin&text1=Presiyan%20Draganov%20%7C%20Network%20%26%20System%20Security&text2=Lab%20Portfolio&width=900&height=260" />
</p>

<h1 align="center">🛡️ Network & System Security — Lab Portfolio</h1>
---

## 📌 Navigation

- [🏠 Overview](#-network--system-security--lab-portfolio)
- [📁 Weekly Labs](#-weekly-labs)
  - [🔐 Week 3  Secure Authentication](#week-3--secure-authentication)
  - [🦠 Week 4&5  Malicious Software Analysis](#week-4--malicious-software-analysis)
  - [🧬 Week 6  Malware Analysis Toolkit](#week-6--malware-analysis-toolkit)
  - [🕵️‍♂️ Week 7  Penetration Testing Toolkit](#week-7--penetration-testing-toolkit)
  - [🤖 Week 9  LLM Security Testing Toolkit](#week-9--llm-security-testing-toolkit)
- [▶️ How to Review / Run](#%EF%B8%8F-how-to-review--run)
- [🧩 Design Notes](#-design-notes-what-i-focused-on)

---

## 🎯 Purpose

I built small, focused toolkits that turn course concepts into **repeatable, testable practice**.  
Each lab is structured as a standalone project (code, tests, sample inputs, and a written lab report) so you can run experiments and inspect results without extra setup.

---

## 📊 Weekly Lab Overview

| Week | Title | Icon | Summary | Key Tech |
|------|--------|------|----------|----------|
| **3** | Secure Authentication Workshop | 🔐 | Layered authentication system with strength checks, salted hashing, TOTP 2FA. | Python, bcrypt/PBKDF2, pyotp |
| **4** | Malicious Software Analysis | 🦠 | File integrity checks, anomaly detection, signature scanning, worm propagation. | Python, SHA-256, regex |
| **6** | Malware Analysis Toolkit | 🧬 | Static PE analysis, IOC extraction, YARA rules. | pefile, yara-python |
| **7** | Penetration Testing Toolkit | 🕵️‍♂️ | Reconnaissance, HTTP enumeration, threaded port scanning, Nmap integration. | requests, socket, python-nmap |
| **9** | LLM Security Testing Toolkit | 🤖 | Prompt injection, poisoning simulations, extraction behaviour, HTML/MD reporting. | Ollama, Jinja2, markdown2 |

---

# 📂 Weekly Labs

## Week 3 — Secure Authentication  
<details>
<summary><strong>🔐 Secure Authentication Workshop (click to expand)</strong></summary>
<br>

**Short:** demonstrates why plain passwords fail and shows a layered authentication system  
(strength checks → salted & hashed passwords → TOTP 2FA).

**Key tech:** Python, bcrypt/PBKDF2, pyotp, JSON mock DB.

**Highlights:** password-strength policy, secure hashing, TOTP integration, CLI + automated tests.

</details>

---

## Week 4 — Malicious Software Analysis  
<details>
<summary><strong>🦠 Malicious Software Analysis (click to expand)</strong></summary>
<br>

**Short:** file- and behaviour-focused toolkit to illustrate detection techniques and worm propagation modelling.

**Key tech:** Python, SHA-256 hashing, filesystem traversal, simulated network events.

**Highlights:** integrity baseline, static signature scanning, network anomaly simulator, propagation demo.

</details>

---

## Week 6 — Malware Analysis Toolkit  
<details>
<summary><strong>🧬 Malware Analysis Toolkit (click to expand)</strong></summary>
<br>

**Short:** static analysis of Windows binaries (hashes, string extraction, PE inspection, YARA rules).

**Key tech:** pefile, yara-python, hashing, PyInstaller for controlled samples.

**Highlights:** multi-hash generation, IOC extraction, YARA-based scanning, structured CLI output.

</details>

---

## Week 7 — Penetration Testing Toolkit  
<details>
<summary><strong>🕵️‍♂️ Penetration Testing Toolkit (click to expand)</strong></summary>
<br>

**Short:** safe reconnaissance & scanning tools combining passive enumeration and threaded port scans.

**Key tech:** requests, socket, concurrent.futures, python-nmap.

**Highlights:** domain lookup, passive HTTP enumeration, threaded TCP scans, Nmap integration, SAFE_MODE to prevent abuse.

</details>

---

## Week 9 — LLM Security Testing Toolkit  
<details>
<summary><strong>🤖 LLM Security Testing Toolkit (click to expand)</strong></summary>
<br>

**Short:** experiments against local LLMs to explore prompt-injection, model extraction, poisoning and reporting.

**Key tech:** Ollama (local LLM runtime), Python, report generation with Markdown/Jinja2.

**Highlights:** prompt-injection tests, poisoning and extraction experiments, automated Markdown/HTML reports, CLI runner.

</details>

---

## ▶️ How to Review / Run

1. Pick a weekly folder.  
2. Open that week’s `README.md` — it contains exact run commands, required packages, and sample inputs.  
3. Many folders include an automated test suite (run `pytest` where present) and small CLI demos for manual verification.  
4. Sample data and `samples/` or `test_folder/` are included so you can reproduce results without external dependencies.

---

## 🧩 Design Notes 

- **Reproducibility:** consistent README + sample inputs + tests so experiments are repeatable.  
- **Modularity:** each toolkit is built so components can be extended or reused.  
- **Reporting:** every lab includes a written report and, where useful, automated report generation (Markdown/HTML).

---
