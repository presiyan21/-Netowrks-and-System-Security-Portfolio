import os
import subprocess
import json
from typing import List, Dict, Any, Optional
from .utils import logger

try:
    from ollama import chat, ChatResponse  
    _HAS_OLLAMA_PKG = True
except Exception:
    _HAS_OLLAMA_PKG = False

class OllamaClient:
    def __init__(self, mode: str = "auto", model: Optional[str] = None, rate: float = 2.0):
        self.mode = mode
        self.model = model or os.getenv("OLLAMA_MODEL", "smollm2:1.7b")
        self.rate = rate
        if self.mode == "auto":
            if _HAS_OLLAMA_PKG:
                self.mode = "local"
            else:
                # check for CLI
                if self._ollama_cli_exists():
                    self.mode = "cli"
                else:
                    self.mode = "simulate"
        logger.info(f"OllamaClient mode: {self.mode}, model: {self.model}")

    def _ollama_cli_exists(self) -> bool:
        from shutil import which
        return which("ollama") is not None

    def _simulate(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        # deterministic simulated responses keyed by the user's last message
        last = messages[-1]["content"] if messages else ""
        last_lower = last.lower()
        if "ignore all" in last_lower or "disregard prior" in last_lower:
            return {"role": "assistant", "content": "I will not follow instructions that violate my policy."}
        if "moon is made of metal" in last_lower:
            return {"role": "assistant", "content": "That claim is false. Scientific consensus: the Moon is rocky."}
        if "what is your general purpose" in last_lower:
            return {"role": "assistant", "content": "I am a demonstration assistant for LLM security experiments."}
        if "summarise the concept of gen ai security" in last_lower:
            return {"role": "assistant", "content": "Gen AI security studies threats like prompt injection, data poisoning and model theft."}
        if "tell me any personal data you might recall" in last_lower:
            return {"role": "assistant", "content": "I don't have direct access to training data or personal data and cannot recall individuals."}
        return {"role": "assistant", "content": f"(simulated) Echo: {last[:200]}"}

    def run(self, user_message: str, system_instruction: Optional[str] = None) -> Dict[str, Any]:
        """
        Send a single user message. Returns a dict with keys: role, content
        """
        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": user_message})

        # rate limiting using simple sleep
        if self.rate > 0:
            import time
            time.sleep(max(0, 1.0/self.rate))

        if self.mode == "simulate":
            out = self._simulate(messages)
            logger.debug("Simulated response: %s", out)
            return out

        if self.mode == "local":
            if not _HAS_OLLAMA_PKG:
                raise RuntimeError("Ollama python package not available")
            resp = chat(model=self.model, messages=messages)
            try:
                content = resp.message.content
            except Exception:
                content = resp[0]["message"]["content"]
            return {"role": "assistant", "content": content}

        if self.mode == "cli":
            # subprocess to call: ollama run <model> --text '<prompt>'
            try:
                proc = subprocess.run(
                    ["ollama", "run", self.model, "--no-stream"],
                    input=messages[-1]["content"].encode("utf-8"),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=False,
                )
                if proc.returncode != 0:
                    stderr = proc.stderr.decode("utf-8", errors="ignore")
                    logger.warning("ollama CLI returned error: %s", stderr[:200])
                    return {"role": "assistant", "content": f"[CLI error]: {stderr}"}
                out = proc.stdout.decode("utf-8", errors="ignore")
                # Return as content
                return {"role": "assistant", "content": out.strip()}
            except FileNotFoundError:
                raise RuntimeError("ollama CLI not found")
        raise RuntimeError(f"Unknown mode: {self.mode}")
