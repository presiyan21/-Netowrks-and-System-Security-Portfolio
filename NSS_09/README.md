# LLM Security Testing Toolkit

This project aims to explore how large-language-model systems can be implemented to asses security risks. Upon diving, we would explore attacks based on vectors prompt injection, model extraction, poisoning simulations, and plenty of others while running controlled experiments against local LLMs through Ollama. The toolkit has further developed reports tool, therefore making it interactive further implying developers can quickly understand model behaviour and potential weaknesses.

---

## 🧰 Technologies Used
- **Python 3** – Core development language  
- **Ollama** – Local LLM runtime for model execution  
- **Subprocess / HTTP** – Supports both CLI and API interaction with models  
- **markdown2 / Jinja2** – Used for Markdown + HTML report generation  
- **JSON / OS utilities** – Handles config data and mock simulation inputs  
- **Pytest** – Automated tests for experiment and client logic  

---

## ⭐ Main Features
- **Prompt Injection Tests:** Checks whether a model can be coerced into ignoring instructions.  
- **Poisoning Simulations:** Helps us divie into how models react to intentionally misleading input.  
- **Model Inversion Queries:** Explores whether a model recalls or fabricates sensitive patterns.  
- **Model Extraction Behaviour:** Evaluates output consistency across repeated prompts.  
- **Multiple Model Support:** Run experiments on several Ollama models for comparison.  
- **Safety Layer:** Input sanitisation, output checks, and basic rate-limiting.  
- **Automated Reporting:** Generates Markdown and HTML summaries of experiment results.  
- **CLI Interface:** Simple command-line runner for launching experiments end-to-end.  

---

## ⚡ How to Run

### 1️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 2️⃣ Run the CLI
```bash
python -m src.cli
```

### Run Tests
```bash
pytest tests/
```
## 🧩 System Architecture

<img width="637" height="1092" alt="Screenshot 2025-12-08 173358" src="https://github.com/user-attachments/assets/10ec024f-5003-4bbb-b221-ca3bc14a6801" />
