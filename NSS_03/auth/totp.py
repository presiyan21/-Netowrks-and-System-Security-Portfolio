import base64, secrets
import pyotp

# Generate random TOTP secret
def generate_secret():
    return base64.b32encode(secrets.token_bytes(16)).decode().rstrip("=")

# Generate URI for QR code
def provisioning_uri(secret, user, issuer="SecureSys"):
    return pyotp.TOTP(secret).provisioning_uri(user, issuer)

# Verify user-provided TOTP code
def verify(secret, code):
    return pyotp.TOTP(secret).verify(code, valid_window=1)

