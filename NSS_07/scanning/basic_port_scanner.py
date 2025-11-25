import socket
from core.validators import validate_host
from core.utils import safe_socket


def scan_port(host, port):
    validate_host(host)
    with safe_socket() as sock:
        result = sock.connect_ex((host, port))
        return result == 0


def scan_multiple(host, ports):
    validate_host(host)
    open_ports = []
    for p in ports:
        if scan_port(host, p):
            open_ports.append(p)
    return open_ports
