import socket
import requests
from core.validators import validate_host
from config.settings import USER_AGENT


def lookup_domain(domain: str):
    try:
        ip = socket.gethostbyname(domain)
        validate_host(ip)
    except Exception as e:
        return {"error": f"Resolution failed: {e}"}

    headers = {"User-Agent": USER_AGENT}
    url = f"https://ipapi.co/{ip}/json/"

    try:
        response = requests.get(url, headers=headers, timeout=3)
        data = response.json() if response.ok else {}
    except Exception:
        data = {}

    return {
        "domain": domain,
        "ip": ip,
        "organisation": data.get("org", "Unknown"),
        "region": data.get("region", "Unknown"),
        "country": data.get("country_name", "Unknown"),
    }
