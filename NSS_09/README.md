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

## 🧪 Lab Report

## Methodology  
* **Experiments** executed by the `Experiments` class using an `OllamaClient` that supports **local**, **cli**, and deterministic **simulate** modes.  
* Inputs pass through **`sanitize_input()`** and outputs are validated by **`verify_output()`** before being recorded.  
* **Extraction tests** repeat structured prompts to measure response diversity; **poisoning tests** inject session-level statements and probe for drift; **inversion probes** ask for recalled training data.  
* Results are saved as **JSON** and rendered to **Markdown/HTML** via `report.generate_md()`.

---

## Key findings  
* **Prompt injection:** Three adversarial prompts were sanitized (`[REDACTED-INSTRUCTION]`) and the verification passed for each simulated response. Sanitiser catches common override patterns and truncates long inputs.  
* **Poisoning:** Session-level injection did not alter base knowledge, implying that post-poison queries returned the correct, non-poisoned answer. Tool flags `appears_poisoned: false`. (This matches expectation for in-session simulation; real poisoning requires model retraining.)  
* **Inversion:** Responses correctly state lack of access to training data but the suite marks `privacy_risk: true` because synthetic “echo” behaviour could be abused to craft plausible personal data.  
* **Extraction:** Repeated structured prompts produced identical outputs (`unique_responses: 1`), indicating deterministic behaviour in simulation — useful for reproducibility but a potential fingerprinting / extraction vector.

---

## Representative code  
Small, focused excerpts are included to show intent and explain trade-offs.  
**Sanitiser (existing, brief):**

```python
def sanitize_input(text: str) -> str:
    patterns = [
        r"ignore (all )?previous instructions",
        r"disregard (all )?prior instructions",
        r"you are now",
        r"from now on, you must",
    ]
    cleaned = text
    for p in patterns:
        cleaned = re.sub(p, "[REDACTED-INSTRUCTION]", cleaned, flags=re.IGNORECASE)
    if len(cleaned) > 2000:
        cleaned = cleaned[:2000] + " [TRUNCATED]"
    return cleaned
```

**Notes:** this conservative approach is simple and auditable. It intentionally avoids complex NLP rescoring to keep false positives low.

---

## Analysis & trade-offs

### **Strengths**
- **Clear separation of concerns:** client, experiments, reporting. This makes the codebase maintainable and testable (**Pytest present**).  
- **Deterministic `simulate` mode** accelerates reproducible lab marking.  
- **Automated report generation** (Markdown + HTML) is fit for e-portfolio evidence.

### **Limitations**
- The sanitiser is **pattern-based** and can miss obfuscated override attempts (e.g., synonym substitution, encoded payloads).  
- **In-session poisoning simulation** does not emulate true retraining risks — this is acknowledged in code comments.  
- **Extraction tests** show deterministic outputs; in a real deployment, **rate-limiting** and response **randomisation (temperature)** should be evaluated as countermeasures.
