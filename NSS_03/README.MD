# Secure Authentication Workshop

This Python-based project demonstrates essential principles of modern authentication and access control. The workshop illustrates why simple password checks are insufficient and builds a secure system from the ground up, integrating password strength analysis, hashing, salting, and two-factor authentication.

---

## 🧰 Technologies Used

- **Python 3** – Development language
- **bcrypt / hashlib** – Provide secure password hashing with salts while enabling optional pepper  
- **pyotp** – Core authentication TOTP generation and verification for 2FA  
- **json / os** – User storage via JSON mock database  
- **string / math** – Enables matrices for password strength evaluation  

---

## ⭐ Main Features

- **Password Strength Enforcement:** Rejects users from entering weak or common passwords.  
- **Secure Password Hashing:** Supports bcrypt or PBKDF2 with salts and optional pepper.  
- **TOTP Two-Factor Authentication:** Requires users to enter a code generated on authenticator apps.  
- **User Authentication:** Validates both password and TOTP.  
- **Mock Database:** Acts as a storage to provide a database of hashed passwords and TOTP secrets in users.json.  
- **CLI & Tests:** Interactive CLI and automated tests which enable easy and quick system feature validation for registration, login, and hashing/strength checks.  

---

## ⚡ How to Run

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run the CLI
```bash
python -m app.cli
```
Follow prompts to register users or log in using TOTP.

### Run Tests
#### Full authentication flow
```bash
python -m app.tests
```
#### Password strength and hashing modules
```bash
python -m app.tests_unit
```

## ✅ Expected Outcomes

- **Successful Registration:**  
  Users are provided with a TOTP URI compatible with authenticator apps.

  ![alt text](<Screenshot 2025-11-25 141747.png>)

- **Login Verification:**  
  Both the password and TOTP code are verified for authentication.

- **Unit Tests:**  
  Ensure correct functionality, including:
  - Password hashing and verification
  - Password strength scoring
  - TOTP generation and validation

![alt text](<Screenshot 2025-11-25 142121.png>)

## System Architecture

![alt text](<Screenshot 2025-11-20 232559.png>)

## Lab Report

## 🔒 Password Strength Analysis

One of the first tools built to ensure user credentials are sufficiently strong. Constituent metrics consist of:

* Minimum length: ≥ 8 characters
* Strong length: ≥ 12 characters
* Character variety: lowercase, uppercase, digits, symbols

To strengthen the toolkit, a blacklist of commonly compromised passwords is included, prompting users to choose a different one. For example:

```python
>> strength("password")
(0, ['This password appears in breach lists.',
     'Use both upper and lowercase letters.',
     'Add numbers.',
     'Add symbols for extra entropy.'])

>> strength("StrongPass123!")
(6, [])
```

This output indicates the user-chosen `"password"` scores 0 and triggers feedback prompts like "add uppercase, digits, and symbols". In contrast, `"StrongPass123!"` scores 6 with no errors shown.

Entropy, a concept used in science (e.g., physics, chemistry) to measure disorder, can also be estimated for passwords using the formula:

```
E = L * log2(pool)
```

Where `pool` is the number of possible characters (e.g., 52 letters, 10 digits, symbols, etc.). Using this formula:

* `"password"` uses only 26 lowercase letters → low entropy
* `"StrongPass123!"` uses all character classes → higher entropy

**Takeaways:** Minimum length (8/12 chars), mixed character types, avoid common passwords.

Sample code:

```python
score, feedback = strength("Pass1234")
# score = 3
# feedback = ['Add symbols for extra entropy.']
```

---

## 🔐 Secure Password Hashing (Salt and Pepper)

To strengthen the system, passwords are hashed using **bcrypt** (preferred) or **PBKDF2** (fallback). Key points:

* **One-way hashing**: Cannot be decrypted, ensuring password security
* **Avoid fast hashes** like SHA-256 for password storage (vulnerable to brute-force/rainbow attacks)
* **bcrypt advantages**: Slow, adaptive, auto-salts each password, work factor tunable (default cost=12)

Example with bcrypt:

```python
>>> bcrypt.hashpw(b"secret", bcrypt.gensalt())
b"$2b$12$...A1..."
>>> bcrypt.hashpw(b"secret", bcrypt.gensalt())
b"$2b$12$...Z9..."
```

Randomness is expected and desirable; output differs each time due to unique salts.

Fallback with PBKDF2:

```python
salt = os.urandom(16)
dk = hashlib.pbkdf2_hmac('sha256', password, salt, 200000)
hash = f"pbkdf2$200000${salt.hex()}${dk.hex()}"
```

* Salt stored alongside hash → defeats rainbow tables
* **Pepper**: A secret global key (e.g., `AUTH_PEPPER` in env variables), added to password before hashing:

```python
hash_password(password + PEPPER)
```

* If the database is stolen, an attacker cannot validate guesses without the pepper
* Changing the pepper invalidates all existing hashes (limitation)

---

### Adding Salt and Pepper (Anti-Rainbow Defenses)

* Without salt → identical passwords yield identical hashes
* With salt → same password produces different hashes each time
* Adding a pepper → even with hash & salt, attacker needs pepper to crack

**Security Discussion:**

* Attacker with only DB:

  * Unsalted SHA-256 → immediate rainbow table lookup
  * Salted hash → must brute-force each password individually
  * Salt + pepper → cannot start without pepper, stalling attack

* Pepper handling: pre-hash concatenation (as implemented) or post-hash HMAC-style (OWASP suggestion)

* Changing pepper → forces password resets

**Example Verification:**

```python
# Hashing "test123" yields bcrypt hash
# Verification returns True
```

