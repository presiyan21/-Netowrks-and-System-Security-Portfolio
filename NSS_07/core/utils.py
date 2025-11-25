import socket
import time
from contextlib import closing

def safe_socket(timeout=1.0):
    """Create a TCP socket with context management."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    return sock

def timestamp():
    return time.strftime("%Y-%m-%d %H:%M:%S")
