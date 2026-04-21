class MirageGenerator:
    def __init__(self):
        self.virtual_nodes = []

    def generate_ghost_signals(self):
        """Simulate multiple ghost devices to mask the real Lily-Pi node."""
        for i in range(5):
            ghost_mac = "00:1A:2B:3C:4D:" + str(i)
            self.virtual_nodes.append(ghost_mac)
            print(f"[RAVANA] 🏺 HEAD 14: Ghost node {i} deployed at {ghost_mac}")


if __name__ == "__main__":
    mirage = MirageGenerator()
    mirage.generate_ghost_signals()
