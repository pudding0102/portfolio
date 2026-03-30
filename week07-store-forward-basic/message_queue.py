from collections import deque
import time

class MessageQueue:
    def __init__(self):
        self.queue = deque()

    def add_message(self, message, peer_port):
        self.queue.append({
            "message": message,
            "peer": peer_port,
            "timestamp": time.time()
        })

    def get_messages(self):
        return list(self.queue)

    def remove_message(self, msg):
        self.queue.remove(msg)