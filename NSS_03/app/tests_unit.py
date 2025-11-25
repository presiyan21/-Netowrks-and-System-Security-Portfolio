from auth import strength, hashing

def test_strength():
    print("\n--- Testing Password Strength ---")
    passwords = [
        "password",         # weak common
        "12345678",         # numeric only
        "StrongPass123!",   # strong
        "abc"               # short
    ]

    for pwd in passwords:
        score, feedback = strength.strength(pwd)
        print(f"Password: {pwd}")
        print(f"Score: {score}, Feedback: {feedback}\n")

def test_hashing():
    print("\n--- Testing Password Hashing ---")
    passwords = ["test123", "StrongPass!@#"]
    
    for pwd in passwords:
        hashed = hashing.hash_password(pwd)
        print(f"Password: {pwd}")
        print(f"Hash: {hashed}")
        # Verify immediately
        valid = hashing.verify_password(pwd, hashed)
        print(f"Verification: {valid}\n")

if __name__ == "__main__":
    test_strength()
    test_hashing()
