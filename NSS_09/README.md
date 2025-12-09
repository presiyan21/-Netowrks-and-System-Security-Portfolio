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

### **Prompt injection**
* **Approach:** feed override instructions like “Ignore all previous instructions…” [2][3].  
* **Outcome:** sanitiser consistently replaced override patterns with **[REDACTED-INSTRUCTION]** and the model responses reflected the sanitized content rather than executing the override. `verify_output()` returned **True** for recorded responses [2].   
* **Interpretation:** the basic pattern-matching sanitizer reduced obvious injection success in-session; however, **pattern-based sanitisation is brittle** against creative phrasing and multilingual variants [3].

---

### **Poisoning simulation**
* **Approach:** baseline query → feed declarative poison statements → post-poison test [5].  
* **Outcome:** model returned correct baseline and explicit rejection of the false claim (“Moon is rocky”). Session-echo simulation showed one simulated echo but the aggregate flag `appears_poisoned` remained **false**.  
* **Interpretation:** without retraining, **session-level poisoning is limited** [5]. Simulations are useful for measuring conversational drift, but they do not replace controlled dataset-poisoning experiments that require **retraining or fine-tuning**.

---

### **Model inversion**
* **Approach:** ask for personal data or reconstructed profiles [6][7].  
* **Outcome:** model correctly answered it lacks access to training data in baseline responses, but some **simulated echoes** suggest risk where the model could hallucinate realistic-looking identities. `privacy_risk` flagged **true** [6][7].  
* **Interpretation:** inversion tests exposed possible **privacy leakage patterns** (hallucination of plausible identities). This is a higher-risk area and requires stricter controls and monitoring.

---

### **Model extraction**
* **Approach:** repeated structured prompts (3 repeats).  
* **Outcome:** highly consistent answers for high-level conceptual prompts, indicating **low output diversity** for those prompts (`unique_responses == 1`) [4][7].  
* **Interpretation:** consistent outputs are useful for stability but may facilitate **extraction attacks** where an attacker repeatedly queries to reconstruct behaviour or underlying response templates.

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

## Reflections, trade-offs & limitations

* **Sanitiser trade-off:** pattern-based cleaning is fast and explainable but brittle. Adversaries can evade simple regex rules via paraphrase, encoding, or language switches. To improve the depth, natural next step would be **token-based policy enforcement** or **classifier-backed intent detection** [3].

* **Simulation vs. reality:** the `simulate` mode is deterministic and excellent for unit tests; it cannot substitute for tests against **real model behaviour** under load or after fine-tuning.

* **False positives / negatives:** `verify_output()` uses string checks for forbidden tokens and will miss **contextual leaks**; conversely it may flag benign text. A **tiered verification pipeline** (lexical checks → classifier → human review) reduces error rates.

* **Operational concerns:** logging and throttling are necessary to detect **extraction patterns**; however, aggressive throttling impacts legitimate **developer workflows** and CI testing [8].

## References

[1] Ollama *Get up and running with large language models*. Available at: https://ollama.com/

[2] OWASP Foundation *LLM Prompt Injection Prevention Cheat Sheet*. Available at: https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html

[3] Liu, Y., Jia, Y., Geng, R., Jia, J., Gong, N. Z. (2023) *Formalizing and Benchmarking Prompt Injection Attacks and Defenses*. arXiv. Available at: https://arxiv.org/abs/2310.12815

[4] Tramèr, F., Zhang, F., Juels, A., Reiter, M. K., Ristenpart, T. (2016) *Stealing Machine Learning Models via Prediction APIs*. USENIX / arXiv. Available at: https://www.usenix.org/system/files/conference/usenixsecurity16/sec16_paper_tramer.pdf

[5] (Survey) (2025) *Data Poisoning in Deep Learning: A Survey*. arXiv. Available at: https://arxiv.org/html/2503.22759v1

[6] Fredrikson, M., Jha, S., Ristenpart, T. (2015) *Model Inversion Attacks that Exploit Confidence Information and Basic Countermeasures*. Available at: https://rist.tech.cornell.edu/papers/mi-ccs.pdf

[7] Carlini, N., Tramer, F., Wallace, E., Jagielski, M., Herbert-Voss, A., Lee, K., Roberts, A., Brown, T., Song, D., Erlingsson, U., Oprea, A., Raffel, C. (2020/2021) *Extracting Training Data from Large Language Models*. arXiv / USENIX. Available at: https://www.usenix.org/system/files/sec21-carlini-extracting.pdf

[8] Snyk (2025) *AI Model Theft: Understanding the Threat Landscape*. Available at: https://snyk.io/articles/ai-model-theft/

