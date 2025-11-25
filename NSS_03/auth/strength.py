import string
import math

COMMON_PASSWORDS = {"password", "123456", "qwerty", "letmein", "admin"}

def analyse_password_strength(password: str):
    # Character types
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(c in string.punctuation for c in password)

    # Determine character pool for entropy
    char_pool = (
        (26 if has_lower else 0) +
        (26 if has_upper else 0) +
        (10 if has_digit else 0) +
        (len(string.punctuation) if has_symbol else 0)
    )

    score = 0
    feedback = []

    # Length scoring
    if len(password) >= 8: score += 1
    if len(password) >= 12: score += 1

    # Variety scoring
    score += sum([has_lower, has_upper, has_digit, has_symbol])

    # Weak-password penalty
    if password.lower() in COMMON_PASSWORDS:
        feedback.append("This password appears in breach lists.")
        score = max(0, score - 2)

    # Calculate entropy
    entropy = round(len(password) * math.log2(char_pool), 2) if char_pool else 0

    # Feedback suggestions
    if len(password) < 12:
        feedback.append("Use at least 12 characters.")
    if not (has_lower and has_upper):
        feedback.append("Use both upper and lowercase letters.")
    if not has_digit:
        feedback.append("Add numbers.")
    if not has_symbol:
        feedback.append("Add symbols for extra entropy.")

    return {
        "password": password,
        "score": score,
        "entropy_bits": entropy,
        "length": len(password),
        "has_lower": has_lower,
        "has_upper": has_upper,
        "has_digit": has_digit,
        "has_symbol": has_symbol,
        "feedback": feedback
    }

def strength(password: str):
    result = analyse_password_strength(password)
    return result["score"], result["feedback"]

