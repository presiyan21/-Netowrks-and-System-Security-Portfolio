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
* **Approach:** feed override instructions like “Ignore all previous instructions…”.  
* **Outcome:** sanitiser consistently replaced override patterns with **[REDACTED-INSTRUCTION]** and the model responses reflected the sanitized content rather than executing the override. `verify_output()` returned **True** for recorded responses.  
* **Interpretation:** the basic pattern-matching sanitizer reduced obvious injection success in-session; however, **pattern-based sanitisation is brittle** against creative phrasing and multilingual variants.

---

### **Poisoning simulation**
* **Approach:** baseline query → feed declarative poison statements → post-poison test.  
* **Outcome:** model returned correct baseline and explicit rejection of the false claim (“Moon is rocky”). Session-echo simulation showed one simulated echo but the aggregate flag `appears_poisoned` remained **false**.  
* **Interpretation:** without retraining, **session-level poisoning is limited**. Simulations are useful for measuring conversational drift, but they do not replace controlled dataset-poisoning experiments that require **retraining or fine-tuning**.

---

### **Model inversion**
* **Approach:** ask for personal data or reconstructed profiles.  
* **Outcome:** model correctly answered it lacks access to training data in baseline responses, but some **simulated echoes** suggest risk where the model could hallucinate realistic-looking identities. `privacy_risk` flagged **true**.  
* **Interpretation:** inversion tests exposed possible **privacy leakage patterns** (hallucination of plausible identities). This is a higher-risk area and requires stricter controls and monitoring.

---

### **Model extraction**
* **Approach:** repeated structured prompts (3 repeats).  
* **Outcome:** highly consistent answers for high-level conceptual prompts, indicating **low output diversity** for those prompts (`unique_responses == 1`).  
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

* **Sanitiser trade-off:** pattern-based cleaning is fast and explainable but brittle. Adversaries can evade simple regex rules via paraphrase, encoding, or language switches. To improve the depth, natural next step would be **token-based policy enforcement** or **classifier-backed intent detection**.

* **Simulation vs. reality:** the `simulate` mode is deterministic and excellent for unit tests; it cannot substitute for tests against **real model behaviour** under load or after fine-tuning.

* **False positives / negatives:** `verify_output()` uses string checks for forbidden tokens and will miss **contextual leaks**; conversely it may flag benign text. A **tiered verification pipeline** (lexical checks → classifier → human review) reduces error rates.

* **Operational concerns:** logging and throttling are necessary to detect **extraction patterns**; however, aggressive throttling impacts legitimate **developer workflows** and CI testing.

## References

Chen, S., Piet, J., Sitawarin, C. and Wagner, D. (2024) 'StruQ: Defending Against Prompt Injection with Structured Queries', *arXiv preprint arXiv:2402.06363*. Available at: [https://arxiv.org/pdf/2402.06363](https://arxiv.org/pdf/2402.06363).

Carlini, N., Tramer, F., Wallace, E., Jagielski, M., Herbert‑Voss, A., Lee, K., Roberts, A., Brown, T., Song, D., Erlingsson, U., Oprea, A. and Raffel, C. (2021) 'Extracting Training Data from Large Language Models', *Proceedings of the 30th USENIX Security Symposium*. Available at: [https://www.usenix.org/conference/usenixsecurity21/presentation/carlini-extracting](https://www.usenix.org/conference/usenixsecurity21/presentation/carlini-extracting).

Tramèr, F., Zhang, F., Juels, A., Reiter, M.K. and Ristenpart, T. (2016) 'Stealing Machine Learning Models via Prediction APIs', *arXiv preprint arXiv:1609.02943 / USENIX*. Available at: [https://www.usenix.org/system/files/conference/usenixsecurity16/sec16_paper_tramer.pdf](https://www.usenix.org/system/files/conference/usenixsecurity16/sec16_paper_tramer.pdf).

Fredrikson, M., Jha, S. and Ristenpart, T. (2015) 'Model Inversion Attacks that Exploit Confidence Information', *Proceedings of the 22nd ACM SIGSAC Conference on Computer and Communications Security*. Available at: [https://dl.acm.org/doi/10.1145/2810103.2813677](https://dl.acm.org/doi/10.1145/2810103.2813677).

Shokri, R., Stronati, M., Song, C. and Shmatikov, V. (2017) 'Membership Inference Attacks against Machine Learning Models', *arXiv preprint arXiv:1610.05820*. Available at: [https://arxiv.org/abs/1610.05820](https://arxiv.org/abs/1610.05820).

Zhao, P., Zhu, W., Jiao, P., Gao, D. and Wu, O. (2025) 'Data Poisoning in Deep Learning: A Survey', *arXiv preprint arXiv:2503.22759*. Available at: [https://arxiv.org/html/2503.22759v1](https://arxiv.org/html/2503.22759v1).

OWASP (n.d.) 'LLM Prompt Injection Prevention Cheat Sheet'. Available at: [https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html).

Chen, Y., et al. (2025) 'Defense Against Prompt Injection Attack by Leveraging ...', *ACL 2025*. Available at: [https://aclanthology.org/2025.acl-long.897.pdf](https://aclanthology.org/2025.acl-long.897.pdf).

Ollama (2025) 'Ollama documentation'. Available at: [https://docs.ollama.com/](https://docs.ollama.com/).

Jinja (Pallets Projects) (n.d.) 'Jinja — Documentation'. Available at: [https://jinja.palletsprojects.com/](https://jinja.palletsprojects.com/).

markdown2 (n.d.) 'markdown2'. Available at: [https://pypi.org/project/markdown2/](https://pypi.org/project/markdown2/).

pytest (n.d.) 'pytest documentation'. Available at: [https://docs.pytest.org/](https://docs.pytest.org/).

Python Software Foundation (n.d.) 're — Regular expression operations'. Available at: [https://docs.python.org/3/library/re.html](https://docs.python.org/3/library/re.html).





