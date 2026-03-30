import socket
import threading
import time
from config import HOST, BASE_PORT, PEER_PORTS, BUFFER_SIZE, FORWARD_THRESHOLD, UPDATE_INTERVAL
from delivery_table import DeliveryTable

delivery_table = DeliveryTable()
message_queue = []

# 📤 ส่ง message
def send_message(peer_port, message):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)

        s.connect((HOST, peer_port))
        s.sendall(message.encode())
        s.close()

        print(f"[NODE {BASE_PORT}] Sent: {message} -> {peer_port}")
        return True
    except (ConnectionRefusedError, socket.timeout):
        print(f"[NODE {BASE_PORT}] Failed to send to {peer_port}")
        return False


# 🔁 Opportunistic forwarding
def forward_loop():
    while True:
        candidates = delivery_table.get_best_candidates(FORWARD_THRESHOLD)

        if candidates:
            print(f"[NODE {BASE_PORT}] Candidates: {candidates}")

        for msg in message_queue[:]:
            for peer in candidates:
                if send_message(peer, msg):
                    message_queue.remove(msg)
                    break  # ส่งสำเร็จแล้วหยุด

        time.sleep(UPDATE_INTERVAL)


# 📥 รับ message
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, BASE_PORT))
    server.listen()

    print(f"[NODE {BASE_PORT}] Listening...")

    while True:
        conn, addr = server.accept()
        data = conn.recv(BUFFER_SIZE).decode()

        print(f"[NODE {BASE_PORT}] Received: {data} from {addr}")

        # เก็บเข้า queue เพื่อ forward ต่อ
        message_queue.append(data)

        conn.close()


# 🚀 main
if __name__ == "__main__":
    # start server
    threading.Thread(target=start_server, daemon=True).start()

    # start forwarding loop
    threading.Thread(target=forward_loop, daemon=True).start()

    # ตั้งค่า probability (ลองปรับเล่นได้)
    for peer in PEER_PORTS:
        delivery_table.update_probability(peer, 0.6)

    # ส่ง message ครั้งแรก
    for peer in PEER_PORTS:
        msg = f"Hello from node {BASE_PORT}"

        if not send_message(peer, msg):
            print(f"[NODE {BASE_PORT}] Store message for {peer}")
            message_queue.append(msg)

    # loop กันโปรแกรมปิด
    while True:
        time.sleep(1)