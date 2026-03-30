from config import DECAY_FACTOR

class PheromoneTable:
    def __init__(self):
        self.table = {}  # {peer_port: pheromone}

    def reinforce(self, peer, value):
        self.table[peer] = self.table.get(peer, 0) + value

    def decay(self):
        for peer in list(self.table.keys()):
            self.table[peer] *= DECAY_FACTOR

    def get_best_candidates(self, threshold):
        return [p for p, val in self.table.items() if val >= threshold]

    def debug_print(self):
        print("[PHEROMONE TABLE]", self.table)