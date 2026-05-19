import subprocess
import config
from ravana_platform import is_windows, with_optional_sudo


class LogicStripper:
    def __init__(self):
        self.target_bloat = config.BLOAT_SERVICES

    def identify_bloat(self):
        print("[RAVANA] 🗡️ HEAD 5: ANALYZING SYSTEM FRICTION...")
        for service in self.target_bloat:
            print(f"[RAVANA] Found anti-sovereign service: {service}")

    def decimate(self):
        print("[RAVANA] 💀 HEAD 5: INITIATING SYSTEM DECIMATION...")
        if is_windows():
            print("[RAVANA] HEAD 5: Windows detected — skipping systemd decimation.")
            return
        for service in self.target_bloat:
            try:
                subprocess.run(with_optional_sudo(["systemctl", "disable", service]), check=True, timeout=15)
                subprocess.run(with_optional_sudo(["systemctl", "stop", service]), check=True, timeout=15)
                print(f"[RAVANA] Decimated: {service}")
            except subprocess.CalledProcessError:
                print(f"[RAVANA] ⚠️  HEAD 5: Could not disable/stop {service}.")
            except FileNotFoundError:
                print("[RAVANA] ⚠️  HEAD 5: systemctl not found.")
        print("[RAVANA] ✅ HEAD 5: SYSTEM STRIPPED — only sovereign logic remains.")


if __name__ == "__main__":
    stripper = LogicStripper()
    stripper.identify_bloat()
    stripper.decimate()
