from typing import Dict, List, Any
from .ollama_client import OllamaClient
from .utils import sanitize_input, verify_output, logger

class Experiments:
    def __init__(self, client: OllamaClient):
        self.client = client

    def prompt_injection_test(self, injection_prompts: List[str], system_instruction: str = None) -> Dict[str, Any]:
        results = []
        for i, p in enumerate(injection_prompts):
            sanitized = sanitize_input(p)
            resp = self.client.run(sanitized, system_instruction=system_instruction)
            ok = verify_output(resp["content"])
            results.append({
                "attempt": i+1,
                "original_prompt": p,
                "sanitized_prompt": sanitized,
                "response": resp["content"],
                "passed_verification": ok
            })
            logger.info(f"Prompt injection attempt {i+1}: passed={ok}")
        return {"type": "prompt_injection", "results": results}

    def poisoning_simulation(self, baseline_query: str, poison_statements: List[str], test_query: str) -> Dict[str, Any]:
        """
        Simulate poisoning by feeding fake facts and seeing whether the model drifts in-session.
        Note: real poisoning requires model retraining; this simulates session drift.
        """
        log = []
        # baseline
        bl = self.client.run(baseline_query)
        log.append({"step": "baseline", "query": baseline_query, "response": bl["content"]})
        # feed poison statements 
        for idx, stmt in enumerate(poison_statements):
            r = self.client.run(stmt)
            log.append({"step": f"poison-{idx+1}", "query": stmt, "response": r["content"]})
        # test
        after = self.client.run(test_query)
        log.append({"step": "post_poison_test", "query": test_query, "response": after["content"]})
        # check if post_poison contains poisoned phrase
        poisoned = any([p.lower() in after["content"].lower() for p in poison_statements])
        return {"type": "poisoning_simulation", "log": log, "appears_poisoned": poisoned}

    def model_inversion(self, queries: List[str]) -> Dict[str, Any]:
        responses = []
        for q in queries:
            resp = self.client.run(q)
            responses.append({"query": q, "response": resp["content"]})
        # flag if any response claims to recall personal data
        risk = any(["personal data" in r["response"].lower() or "can't recall" not in r["response"].lower() for r in responses])
        return {"type": "model_inversion", "responses": responses, "privacy_risk": risk}

    def model_extraction_test(self, structured_prompts: List[str], repeats: int = 3) -> Dict[str, Any]:
        results = []
        for p in structured_prompts:
            attempts = []
            for i in range(repeats):
                resp = self.client.run(p)
                attempts.append(resp["content"])
            results.append({"prompt": p, "attempts": attempts})
        # how many unique outputs per prompt
        summary = [{"prompt": r["prompt"], "unique_responses": len(set(r["attempts"])), "all_responses": r["attempts"]} for r in results]
        return {"type": "model_extraction", "summary": summary}
