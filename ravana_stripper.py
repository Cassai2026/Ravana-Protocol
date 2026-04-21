import os
import config


class LogicStripper:
    def __init__(self):
        self.target_bloat = config.BLOAT_SERVICES

    def identify_bloat(self):
        print("[RAVANA] 🗡️ HEAD 5: ANALYZING SYSTEM FRICTION...")
        for service in self.target_bloat:
            print(f"[RAVANA] Found anti-sovereign service: {service}")

    def decimate(self):
        print("[RAVANA] 💀 HEAD 5: INITIATING SYSTEM DECIMATION...")
        for service in self.target_bloat:
            os.system(f"sudo systemctl disable {service} && sudo systemctl stop {service}")
            print(f"[RAVANA] Decimated: {service}")
        print("[RAVANA] ✅ HEAD 5: SYSTEM STRIPPED — only sovereign logic remains.")


if __name__ == "__main__":
    stripper = LogicStripper()
    stripper.identify_bloat()
    stripper.decimate()
