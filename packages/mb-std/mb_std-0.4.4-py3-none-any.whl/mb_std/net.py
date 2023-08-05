import socket
import time


def check_port(ip: str, port: int, attempts=3, sleep_seconds=1, timeout=1) -> bool:
    for _ in range(attempts):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        res = sock.connect_ex((ip, port)) == 0
        if res:
            return True
        time.sleep(sleep_seconds)
    return False
