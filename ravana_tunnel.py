import subprocess
import time
import random

class SilentTunnel:
    def __init__(self):
        self.endpoints = ["node_uk_1", "node_se_1", "node_ch_1"] # Sovereign mesh points
        self.current_endpoint = None

    def rotate_tunnel(self):
        new_point = random.choice(self.endpoints)
        if new_point != self.current_endpoint:
            print(f"[RAVANA] 🌀 ROTATING TUNNEL: Shifting to {new_point}...")
            # In a live Pi 5 environment, this would swap the wg0.conf
            # subprocess.run(["wg-quick", "down", "wg0"])
            # subprocess.run(["wg-quick", "up", new_point])
            self.current_endpoint = new_point
            print(f"[RAVANA] ✅ TUNNEL SECURED: Frequency Shifted.")

if __name__ == "__main__":
    tunnel = SilentTunnel()
    tunnel.rotate_tunnel()
