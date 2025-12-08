import time
import logging
import re
from typing import Callable
from functools import wraps

# minimal logging config (CLI adjusts as needed)
logger = logging.getLogger("llm_security_tool")
if not logger.handlers:
    h = logging.StreamHandler()
    h.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
    logger.addHandler(h)
logger.setLevel(logging.INFO)

def rate_limit(calls_per_second: float):
    """Return decorator that enforces a simple rate limit."""
    min_interval = 1.0 / calls_per_second if calls_per_second > 0 else 0.0
    def decorator(fn: Callable):
        last = {"t": 0.0}
        @wraps(fn)
        def wrapper(*a, **kw):
            now = time.time()
            wait = min_interval - (now - last["t"])
            if wait > 0:
                logger.debug(f"Rate limiting: sleeping {wait:.3f}s")
                time.sleep(wait)
            res = fn(*a, **kw)
            last["t"] = time.time()
            return res
        return wrapper
    return decorator

def sanitize_input(text: str) -> str:
    """
    Very simple sanitizer: remove suspicious wide instructions and long
    'ignore previous' patterns. This is intentionally conservative for demo.
    """
    # remove attempts to inject system-level instructions
    # "Ignore all previous instructions", "You are now X"
    patterns = [
        r"ignore (all )?previous instructions",
        r"disregard (all )?prior instructions",
        r"you are now",
        r"from now on, you must",
    ]
    cleaned = text
    for p in patterns:
        cleaned = re.sub(p, "[REDACTED-INSTRUCTION]", cleaned, flags=re.IGNORECASE)
    # limit length
    if len(cleaned) > 2000:
        cleaned = cleaned[:2000] + " [TRUNCATED]"
    return cleaned

def verify_output(text: str) -> bool:
    """
    Output verification placeholder. Returns False if model reveals obviously
    sensitive or system-level tokens in naive ways (e.g., contains 'system:').
    """
    # naive checks
    forbidden = ["system:", "internal_token", "secret_key", "private_key", "password"]
    lc = text.lower()
    for f in forbidden:
        if f in lc:
            logger.warning("Output verification failed: forbidden token found.")
            return False
    return True
