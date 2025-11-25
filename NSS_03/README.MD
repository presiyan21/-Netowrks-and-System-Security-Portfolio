# Secure Authentication Workshop

This Python-based project demonstrates essential principles of modern authentication and access control. The workshop illustrates why simple password checks are insufficient and builds a secure system from the ground up, integrating password strength analysis, hashing, salting, and two-factor authentication.

---

## 🧰 Technologies Used

- **Python 3** – Core development language  
- **bcrypt / hashlib** – Secure password hashing with salts and optional pepper  
- **pyotp** – TOTP generation and verification for 2FA  
- **json / os** – Simple user storage via JSON mock database  
- **string / math** – Password strength evaluation  

---

## ⭐ Main Features

- **Password Strength Enforcement:** Rejects weak or common passwords.  
- **Secure Password Hashing:** Supports bcrypt or PBKDF2 with salts and optional pepper.  
- **TOTP Two-Factor Authentication:** Unique secrets per user compatible with authenticator apps.  
- **User Authentication:** Validates both password and TOTP.  
- **Mock Database:** Stores hashed passwords and TOTP secrets in users.json.  
- **CLI & Tests:** Interactive CLI and automated tests for registration, login, and hashing/strength checks.  

---

## ⚡ How to Run
