from concurrent.futures import ThreadPoolExecutor
from scanning.basic_port_scanner import scan_port
from core.validators import validate_host

def threaded_scan(host, ports, workers=20):
    validate_host(host)
    results = []

    def task(port):
        return port if scan_port(host, port) else None

    with ThreadPoolExecutor(max_workers=workers) as exe:
        for r in exe.map(task, ports):
            if r:
                results.append(r)

    return sorted(results)
