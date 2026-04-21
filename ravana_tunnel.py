import subprocess
import random
import config


class SilentTunnel:
    def __init__(self):
        self.endpoints = config.WIREGUARD_ENDPOINTS
        self.current_endpoint = None

    def rotate_tunnel(self):
        new_point = random.choice(self.endpoints)
        if new_point == self.current_endpoint:
            print(f"[RAVANA] 🌀 TUNNEL: Already connected to {new_point} — no rotation needed.")
            return
        print(f"[RAVANA] 🌀 TUNNEL: Rotating to {new_point}...")
        try:
            subprocess.run(["sudo", "wg-quick", "down", "wg0"], check=True, timeout=15)
            subprocess.run(["sudo", "wg-quick", "up", new_point], check=True, timeout=15)
            self.current_endpoint = new_point
            print(f"[RAVANA] ✅ TUNNEL: Secured via {new_point} — frequency shifted.")
        except subprocess.CalledProcessError as exc:
            print(f"[RAVANA] ⚠️  TUNNEL: Rotation failed: {exc}")
        except FileNotFoundError:
            print("[RAVANA] ⚠️  TUNNEL: wg-quick not found — WireGuard not installed.")


if __name__ == "__main__":
    tunnel = SilentTunnel()
    tunnel.rotate_tunnel()
