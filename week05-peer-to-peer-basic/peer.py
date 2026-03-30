import socket
import threading
import sys
from config import HOST, BASE_PORT, BUFFER_SIZE

peer_id = int(sys.argv[1])
PORT = BASE_PORT + peer_id

# 🔊 Listener (รับ)
def listen():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(5)

    print(f"[PEER {peer_id}] Listening on {PORT}")

    while True:
        conn, addr = sock.accept()
        data = conn.recv(BUFFER_SIZE)
        print(f"[PEER {peer_id}] From {addr}: {data.decode()}")
        conn.close()

# 📤 Sender (ส่ง)
def send_message(target_peer_id, message):
    target_port = BASE_PORT + target_peer_id

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, target_port))
    sock.sendall(message.encode())
    sock.close()

# 🚀 เริ่ม listener แบบ thread
threading.Thread(target=listen, daemon=True).start()

# 🔁 loop ส่งข้อความ
while True:
    target = int(input("Send to peer ID: "))
    msg = input("Message: ")
    send_message(target, msg)