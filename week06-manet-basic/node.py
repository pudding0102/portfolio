import socket
import threading
import random
from config import HOST, BASE_PORT, BUFFER_SIZE, NEIGHBORS, FORWARD_PROBABILITY, TTL

neighbor_table = set(NEIGHBORS)

def handle_incoming(conn, addr):
    data = conn.recv(BUFFER_SIZE).decode()
    msg, ttl = data.split('|')
    ttl = int(ttl)

    print(f"[NODE {BASE_PORT}] Received: {msg} (TTL={ttl})")

    conn.close()

    # ✅ ต้องอยู่ตรงนี้!
    if ttl > 0 and random.random() < FORWARD_PROBABILITY:
        forward_message(msg, ttl - 1, exclude=addr[1])


def forward_message(message, ttl, exclude=None):
    for peer_port in neighbor_table:
        if peer_port == exclude:
            continue

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, peer_port))
            s.sendall(f"{message}|{ttl}".encode())
            s.close()
        except:
            print(f"[NODE {BASE_PORT}] Peer {peer_port} unreachable")


def start_server(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, port))
    server.listen()

    print(f"[NODE {port}] Listening...")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_incoming, args=(conn, addr)).start()


# 🚀 main
if __name__ == "__main__":
    threading.Thread(target=start_server, args=(BASE_PORT,), daemon=True).start()

    forward_message("Hello", TTL)