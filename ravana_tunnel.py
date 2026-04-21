import subprocess
import random
import config


class SilentTunnel:
    def __init__(self):
        self.endpoints = config.WIREGUARD_ENDPOINTS
        self.current_endpoint = None

    def rotate_tunnel(self):
        # Validate against the whitelist before any subprocess call
        available = [ep for ep in self.endpoints if ep != self.current_endpoint]
        if not available:
            print("[RAVANA] 🌀 TUNNEL: Only one endpoint configured — no rotation possible.")
            return
        new_point = random.choice(available)

        # Ensure new_point is strictly in the allowed list (defence-in-depth)
        if new_point not in config.WIREGUARD_ENDPOINTS:
            print(f"[RAVANA] ⚠️  TUNNEL: Endpoint '{new_point}' not in whitelist — aborting.")
            return

        print(f"[RAVANA] 🌀 TUNNEL: Rotating to {new_point}...")
        try:
            subprocess.run(["sudo", "wg-quick", "down", "wg0"], check=True, timeout=15)
            subprocess.run(["sudo", "wg-quick", "up", new_point], check=True, timeout=15)
            self.current_endpoint = new_point
            print(f"[RAVANA] ✅ TUNNEL: Secured via {new_point} — frequency shifted.")
        except subprocess.CalledProcessError as exc:
            print(f"[RAVANA] ⚠️  TUNNEL: Rotation failed — command error.")
        except FileNotFoundError:
            print("[RAVANA] ⚠️  TUNNEL: wg-quick not found — WireGuard not installed.")


if __name__ == "__main__":
    tunnel = SilentTunnel()
    tunnel.rotate_tunnel()
