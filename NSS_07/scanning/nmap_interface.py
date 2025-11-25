import nmap
from core.validators import validate_host

def nmap_service_scan(host, port_range="1-100"):
    validate_host(host)
    scanner = nmap.PortScanner()

    try:
        scanner.scan(host, port_range, arguments="-sV")
    except Exception as e:
        return {"error": str(e)}

    findings = []
    for h in scanner.all_hosts():
        for proto in scanner[h].all_protocols():
            for port, data in scanner[h][proto].items():
                findings.append(
                    f"{h}:{port} {data['state']} → {data.get('name','?')} "
                    f"{data.get('version','')}"
                )
    return findings
