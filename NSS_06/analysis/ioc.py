import re

def extract_iocs(file_path):
    with open(file_path, 'rb') as f:
        data = f.read().decode(errors='ignore')
    urls = re.findall(r'https?://[^\s"\'<>]+', data)
    ips = re.findall(r'\b\d{1,3}(?:\.\d{1,3}){3}\b', data)
    return {
        'urls': urls,
        'ips': ips
    }
