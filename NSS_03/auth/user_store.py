import json
import os

DB_FILE = "users.json"

class UserStore:
    def __init__(self):
        self.users = self.load()

    # Load users from JSON
    def load(self):
        if os.path.exists(DB_FILE):
            with open(DB_FILE, "r") as f:
                return json.load(f)
        return {}

    # Save users to JSON
    def save(self):
        with open(DB_FILE, "w") as f:
            json.dump(self.users, f)

    # Add a new user record
    def add(self, username, record):
        self.users[username] = {
            "username": record.username,
            "pwd_hash": record.pwd_hash,
            "totp_secret": record.totp_secret
        }
        self.save()

    # Retrieve user by username
    def get(self, username):
        return self.users.get(username)

    # Check if user exists
    def exists(self, username):
        return username in self.users


