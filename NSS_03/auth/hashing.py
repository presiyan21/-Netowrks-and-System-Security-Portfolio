import os, hmac, hashlib
try:
    import bcrypt
    HAVE_BCRYPT = True
except:
    HAVE_BCRYPT = False

PEPPER = os.getenv("AUTH_PEPPER", "")  

# PBKDF2 hash fallback if bcrypt not available
def pbkdf2_hash(pwd, iters=200_000):
    salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac("sha256", pwd, salt, iters)
    return f"pbkdf2${iters}${salt.hex()}${dk.hex()}"

def pbkdf2_verify(pwd, stored):
    try:
        _, iters, salt, dk_hex = stored.split("$")
        dk = hashlib.pbkdf2_hmac("sha256", pwd, bytes.fromhex(salt), int(iters))
        return hmac.compare_digest(dk.hex(), dk_hex)
    except:
        return False

# Hash password with bcrypt if available, otherwise PBKDF2
def hash_password(password):
    pwd = (password + PEPPER).encode()
    if HAVE_BCRYPT:
        return bcrypt.hashpw(pwd, bcrypt.gensalt()).decode()
    return pbkdf2_hash(pwd)

# Verify password against stored hash
def verify_password(password, stored):
    pwd = (password + PEPPER).encode()
    if HAVE_BCRYPT and stored.startswith("$2"):
        return bcrypt.checkpw(pwd, stored.encode())
    return pbkdf2_verify(pwd, stored)

