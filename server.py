import socket
import json

# IP Pool 
IP_POOL = [
    "192.168.1.1", "192.168.1.2", "192.168.1.3", "192.168.1.4", "192.168.1.5",
    "192.168.1.6", "192.168.1.7", "192.168.1.8", "192.168.1.9", "192.168.1.10",
    "192.168.1.11", "192.168.1.12", "192.168.1.13", "192.168.1.14", "192.168.1.15"
]

SERVER_HOST = "127.0.0.1"   # Local host
SERVER_PORT = 9999         


def resolve_ip(custom_header: str) -> str:
    """Applying timestamp("HHMMSSID") rules to choose an IP from the pool"""
    hour = int(custom_header[:2])   # HH first two chars
    seq_id = int(custom_header[-2:])  # ID last two chars

    # Time based Selection
    if 4 <= hour <= 11:       # Morning 
        start = 0
    elif 12 <= hour <= 19:    # Afternoon 
        start = 5
    else:                     # Night 
        start = 10

    ip_id = start + (seq_id % 5)
    return IP_POOL[ip_id]


def server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((SERVER_HOST, SERVER_PORT))
    print(f"[SERVER] Listening on {SERVER_HOST}:{SERVER_PORT}...")

    while True:
        data, addr = sock.recvfrom(4096)
        try:
            # Decode the plain text message from client
            msg = data.decode()
            if "|" not in msg:
                print(f"[SERVER] Invalid message: {msg}")
                continue

            header, domain = msg.split("|", 1)
            ip = resolve_ip(header)

            # Response format
            response = f"{header}|{domain}|{ip}"
            sock.sendto(response.encode(), addr)

            print(f"[SERVER] {domain} -> {ip} (Header={header})")
        except Exception as e:
            print("[SERVER] Error:", e)


if __name__ == "__main__":
    server()
