import socket
import threading
import time

from config import HOST, BASE_PORT, PEER_PORTS, BUFFER_SIZE, UPDATE_INTERVAL
from token import Token

token_queue = []

# 📤 ส่ง token
def send_token(peer_port, token):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)

        s.connect((HOST, peer_port))
        s.sendall(token.message.encode())
        s.close()

        print(f"[NODE {BASE_PORT}] Sent token -> {peer_port}")
        return True

    except (ConnectionRefusedError, socket.timeout):
        print(f"[NODE {BASE_PORT}] Failed to send to {peer_port}")
        return False


# 🔁 forward token
def forward_loop():
    while True:
        for token in token_queue[:]:
            for peer in PEER_PORTS:
                if send_token(peer, token):
                    token_queue.remove(token)
                    break

        time.sleep(UPDATE_INTERVAL)


# 📥 รับ token
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, BASE_PORT))
    server.listen()

    print(f"[NODE {BASE_PORT}] Listening...")

    while True:
        conn, addr = server.accept()
        data = conn.recv(BUFFER_SIZE).decode()

        # สร้าง token ใหม่จาก message
        token = Token(data)

        message = token.read_token()

        if message:
            print(f"[NODE {BASE_PORT}] Received token: {message}")

            # forward ต่อได้ (ยังไม่หมดอายุ)
            token_queue.append(token)
        else:
            print(f"[NODE {BASE_PORT}] Token invalid/used from {addr}")

        conn.close()


# 🚀 main
if __name__ == "__main__":
    threading.Thread(target=start_server, daemon=True).start()
    threading.Thread(target=forward_loop, daemon=True).start()

    # สร้าง token เริ่มต้น
    initial_token = Token(f"Quantum token from {BASE_PORT}")
    token_queue.append(initial_token)

    while True:
        time.sleep(1)