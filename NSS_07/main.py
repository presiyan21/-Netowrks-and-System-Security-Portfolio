from reconnaissance.domain_lookup import lookup_domain
from reconnaissance.blackbox_web_enum import blackbox_enum
from scanning.threaded_port_scanner import threaded_scan
from scanning.nmap_interface import nmap_service_scan
from core.report_writer import write_report
from config.settings import TARGET_DOMAINS


def run():
    for domain in TARGET_DOMAINS:
        info = lookup_domain(domain)
        write_report("Domain Lookup", [str(info)])

        bb = blackbox_enum(f"http://{domain}")
        write_report("Black-Box Web Enumeration", bb)

    open_ports = threaded_scan("127.0.0.1", range(1, 200))
    write_report("Threaded Port Scan", [f"Open Ports: {open_ports}"])

    nmap_info = nmap_service_scan("127.0.0.1", "1-50")
    write_report("Nmap Scan", nmap_info)


if __name__ == "__main__":
    run()
