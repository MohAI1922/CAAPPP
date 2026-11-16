"""
VeriMath Server Runner
Runs the VeriMath FastAPI backend on port 8000 and 8001 with socket reuse.
"""
import socket
import uvicorn
from backend.main import app

def main():
    sockets = []
    
    # 1. Try IPv6 localhost on port 8000 (Chrome / Edge default for http://localhost:8000)
    try:
        sock_ipv6 = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        sock_ipv6.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock_ipv6.bind(('::1', 8000))
        sock_ipv6.setblocking(False)
        sockets.append(sock_ipv6)
    except Exception as e:
        print(f"Note: Could not bind IPv6 port 8000: {e}")

    # 2. Try IPv4 127.0.0.1 on port 8000
    try:
        sock_8000 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_8000.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock_8000.bind(('127.0.0.1', 8000))
        sock_8000.setblocking(False)
        sockets.append(sock_8000)
    except Exception as e:
        print(f"Note: Could not bind IPv4 port 8000: {e}")

    # 3. Always bind port 8001 as a guaranteed secondary port
    try:
        sock_8001 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_8001.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock_8001.bind(('0.0.0.0', 8001))
        sock_8001.setblocking(False)
        sockets.append(sock_8001)
    except Exception as e:
        print(f"Note: Could not bind port 8001: {e}")

    if not sockets:
        print("ERROR: Could not bind to any port.")
        return

    config = uvicorn.Config(app=app, log_level="info")
    server = uvicorn.Server(config)
    print("==================================================================")
    print(" VeriMath Server Ready!")
    print(" - UI (IPv6 Localhost): http://localhost:8000/app/")
    print(" - UI (IPv4 Port 8001): http://127.0.0.1:8001/app/")
    print("==================================================================")
    server.run(sockets=sockets)

if __name__ == "__main__":
    main()
