from core.auth_system import AuthSystem

def run_tests():
    auth = AuthSystem(require_totp=True)

    # Register a test user 
    print("\n--- Register User ---")
    ok, msg = auth.register("alice", "StrongPass123!")
    print(ok, msg)
    if not ok:
        return

    # Show TOTP URI 
    print("\n--- Get TOTP URI ---")
    uri = auth.get_totp_uri("alice")
    print(uri)
    print("Scan this in Google Authenticator / Authy")

    # Wrong password 
    print("\n--- Authenticate (wrong password) ---")
    print(auth.authenticate("alice", "wrongpass"))

    # Correct password, missing TOTP 
    print("\n--- Authenticate (correct password, no TOTP) ---")
    print(auth.authenticate("alice", "StrongPass123!"))

    # Correct password + TOTP 
    print("\n--- Authenticate with TOTP ---")
    code = input("Enter TOTP code from authenticator app: ")
    print(auth.authenticate("alice", "StrongPass123!", code))

if __name__ == "__main__":
    run_tests()

