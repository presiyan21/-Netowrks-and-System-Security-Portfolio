import requests
from config.settings import USER_AGENT


def fetch_headers(url: str):
    try:
        res = requests.head(url, timeout=3, headers={"User-Agent": USER_AGENT})
        return {
            "server": res.headers.get("Server", "Hidden/Unknown"),
            "content_type": res.headers.get("Content-Type", "Unknown"),
        }
    except Exception as e:
        return {"error": str(e)}
