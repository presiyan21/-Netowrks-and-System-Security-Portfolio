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
