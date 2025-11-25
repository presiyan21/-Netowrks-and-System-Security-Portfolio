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
