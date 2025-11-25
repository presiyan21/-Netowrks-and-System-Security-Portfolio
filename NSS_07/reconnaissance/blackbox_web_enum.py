from reconnaissance.passive_recon import fetch_headers

def blackbox_enum(url):
    result = fetch_headers(url)
    report = [f"{k}: {v}" for k, v in result.items()]
    return report
