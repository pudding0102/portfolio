import socket
import threading
import time

from config import HOST, BASE_PORT, PEER_PORTS, BUFFER_SIZE, \
                   FORWARD_THRESHOLD, UPDATE_INTERVAL, REINFORCEMENT, INITIAL_PHEROMONE

from pheromone_table import PheromoneTable

pheromone_table = PheromoneTable()
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

        # ✅ reinforce เมื่อสำเร็จ
        pheromone_table.reinforce(peer_port, REINFORCEMENT)

        return True

    except (ConnectionRefusedError, socket.timeout):
        print(f"[NODE {BASE_PORT}] Failed to send to {peer_port}")
        return False


# 🔁 forward + decay
def forward_loop():
    while True:
        # ลด pheromone ทุก cycle
        pheromone_table.decay()

        candidates = pheromone_table.get_best_candidates(FORWARD_THRESHOLD)

        print(f"[NODE {BASE_PORT}] Candidates: {candidates}")
        pheromone_table.debug_print()

        for msg in message_queue[:]:
            for peer in candidates:
                if send_message(peer, msg):
                    message_queue.remove(msg)
                    break

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

        # เก็บไว้ forward ต่อ
        message_queue.append(data)

        conn.close()


# 🚀 main
if __name__ == "__main__":
    # start server
    threading.Thread(target=start_server, daemon=True).start()

    # start forward loop
    threading.Thread(target=forward_loop, daemon=True).start()

    # 🔥 initialize pheromone
    for peer in PEER_PORTS:
        pheromone_table.reinforce(peer, INITIAL_PHEROMONE)

    # ส่งครั้งแรก
    for peer in PEER_PORTS:
        msg = f"Hello from node {BASE_PORT}"

        if not send_message(peer, msg):
            print(f"[NODE {BASE_PORT}] Store message")
            message_queue.append(msg)

    while True:
        time.sleep(1)