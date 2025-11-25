# core/auth_system.py
from dataclasses import dataclass
from auth.hashing import hash_password, verify_password
from auth.strength import strength
from auth.totp import generate_secret, provisioning_uri, verify
from auth.user_store import UserStore

@dataclass
class UserRecord:
    username: str
    pwd_hash: str
    totp_secret: str

class AuthSystem:
    def __init__(self, require_totp=True):
        self.store = UserStore()
        self.require_totp = require_totp

    def register(self, username, password):
        # Block duplicate usernames
        if self.store.exists(username):
            return False, "User exists"

        # Check password strength
        score, issues = strength(password)
        if score < 2:
            return False, f"Weak password: {issues}"

        secret = generate_secret()
        record = UserRecord(username, hash_password(password), secret)
        self.store.add(username, record)
        return True, "Registered"

    def authenticate(self, username, password, code=None):
        user = self.store.get(username)
        if not user:
            return False, "User not found"

        if not verify_password(password, user["pwd_hash"]):
            return False, "Invalid password"

        if self.require_totp:
            if not code or not verify(user["totp_secret"], code):
                return False, "Invalid TOTP"

        return True, "Authenticated"

    def get_totp_uri(self, username):
        # Build URI for authenticator apps
        user = self.store.get(username)
        if not user:
            raise KeyError("No user")
        
        return provisioning_uri(user["totp_secret"], username)



