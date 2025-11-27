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

## Password Strength Analysis

One of the first tools built to ensure user credentials are sufficiently strong. The meter's metrics consist of (≥8 chars, ≥12 chars) and character variety (lowercase, uppercase, digits, symbols). Furthermore, to strengthen the toolkit, another chosen feature was a blacklist consisting of commonly compromised passwords and prompting users to choose a different one. For example, the code returns:

```python
>> strength("password")
(0, ['This password appears in breach lists.', 'Use both upper and lowercase letters.', 'Add numbers.', 'Add symbols for extra entropy.'])

>> strength("StrongPass123!")
(6, [])
```

This output indicates the user-chosen "password" scores 0 and triggers feedback (appears in breach lists) prompts like "add uppercase, digits, and symbols". By doing so in contrast, "StrongPass123!" scores 6 on our scale with no visible errors shown.

Entropy being another concept primarily studied in different aspects of science like chemistry or physics (measuring the amount of disorder), we can estimate it in passwords using the formula `E = L·log₂(pool)`, pool being the number of possible characters (e.g. 52 lower and uppercase in English, 10 digits, etc.). Using our examples from earlier, "password" makes use of just 26 lowercases, in contrast, the other candidate "StrongPass123!" makes use of all classes. Therefore, entropy is sufficiently higher using the equation, proving why it’s stronger.

Takeaways: Minimum length (8/12 chars), mixed char types, no common passwords.

```python
# Sample code:
score, feedback = strength("Pass1234")
# score=3, feedback=['Add symbols for extra entropy.']
```

---

## Secure Password Hashing (Salt and Pepper)

With the goal to further strengthen our system, we hash passwords with bcrypt (if available) when not possible, the alternative fallback is PBKDF2. Highlighted by OWASP, hashing is one-way, so it cannot be “decrypted” back to the password. Making it exceptionally successful for password validation. Taking all the listed factors into consideration is why passwords are never stored in plaintext, while also avoiding reversible encryption.

MD5 and SHA-256 comparisons lead to the conclusion that fast hashes like SHA-256 are too fast for password storage while also being vulnerable to brute-force attacks. Its inherent speed leads to both highly susceptible brute-force and rainbow table attacks. In contrast, the design of bcrypt makes it better suited by offering to be slow and adaptive. My `hash_password()` function uses `bcrypt.hashpw`, generating a string like `"$2b$12$..."` that embeds the salt and cost factor. The result output is extremely long (60+ chars), unlike the short hex of SHA-256. Crucially, bcrypt auto-salts each individual password while allowing the freedom to custom-tune the work factor (my model used cost=12 as default). When verifying, `bcrypt.checkpw` recomputes with the same salt.

Even without bcrypt, our PBKDF2 fallback adds a random salt:

```python
salt = os.urandom(16)
dk = hashlib.pbkdf2_hmac('sha256', password, salt, 200000)
hash = f"pbkdf2$200000${salt.hex()}${dk.hex()}"
```

The salt is stored alongside the hash. Subsequently helps to defeat rainbow tables by requiring unique hashes per password. OWASP puts an emphasis on the fact that each unique salt forces an attacker to crack each hash separately, significantly reducing bulk cracking efficiency. Modern functions (Argon2, bcrypt, PBKDF2) do this automatically.

We also introduced a static pepper (`AUTH_PEPPER` from the environment). A pepper is a secret global key added to every password before hashing. It is not stored in the database. In terms of code, the implementation is:

```python
hash_password(password + PEPPER)
```

Further simplified, if the hash DB is stolen, an attacker not possessing the pepper lacks resources to validate guesses. OWASP suggests pepper must be kept separate from the database (e.g. in an HSM or config). In practice, handling a pepper requires careful management: if the pepper is changed, it results in all existing hashes becoming invalid (a well-known limitation). Also, our pepper was optional (os.getenv default empty), so testing required ensuring a consistent environment.

* Example: The same password hashed twice with bcrypt produces different outputs (due to salt), e.g.:

```python
>>> bcrypt.hashpw(b"secret", bcrypt.gensalt())
b"$2b$12$...A1..."
>>> bcrypt.hashpw(b"secret", bcrypt.gensalt())
b"$2b$12$...Z9..."
```

This randomness is expected and desirable.

* Output verification: Our test script showed successful hashing and verification:

```
Hashing "test123": $2b$12$nwQbzsOy... (bcrypt hash)
Verify check returns True
```

---

## Adding Salt and Pepper (Anti-Rainbow Defenses)

Without salt, identical passwords would hash identically. With bcrypt or our PBKDF2-salt, repeated hashing yields distinct hashes, as above. To prove that, I generated two hashes for the same password and got different output each time, proving rainbow-table resistance. Adding a pepper on top means even if an attacker has the salt and hash, they also must know the secret pepper. According to OWASP, “peppers are secrets not stored along with the password database”, and they stop attackers who steal only the database. In my configured system, the pepper is in the app config (e.g. an environment variable), so it would survive even if the database dump is leaked or compromised.

**Security Discussion:**
If an attacker only gets the DB:

* Unsalted SHA-256: they could look up hashes in a rainbow table immediately.
* Salted hashes: they must brute-force each password individually (much slower).
* Salt + pepper: they cannot even start without the pepper, essentially stalling the attack unless the pepper itself is compromised.

After accounting for this, I came into realisation of a practical issue: my code concatenates pepper before hashing (pre-hash peppering). OWASP also suggests post-hash HMAC-style peppering as an alternative. Managing the pepper is non-trivial, since changing it invalidates all accounts and forces password resets.
