from config.settings import SAFE_MODE, ALLOWED_HOSTS

def validate_host(host):
    if not SAFE_MODE:
        return True

    if host in ALLOWED_HOSTS:
        return True

    raise PermissionError(
        f"Scanning '{host}' blocked: SAFE_MODE enabled.\n"
        f"Allowed hosts: {ALLOWED_HOSTS}"
    )
