import socket
from config import PORT, BUFFER_SIZE

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# ฟังทุก IP ในเครื่อง
sock.bind(("", PORT))

print(f"[LISTENER] Listening on port {PORT}")

while True:
    data, addr = sock.recvfrom(BUFFER_SIZE)
    print(f"[LISTENER] From {addr}: {data.decode()}")