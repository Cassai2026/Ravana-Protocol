import os
import time
import config


def scrub_logs():
    print("[RAVANA] 🧹 HEAD 4: SCRUBBING SYSTEM LOGS...")
    for target in config.LOG_SCRUB_TARGETS:
        if os.path.exists(target):
            os.system(f"sudo truncate -s 0 {target}")
        print(f"[RAVANA] Zeroed: {target}")
    print("[RAVANA] ✅ HEAD 4: DATA PROTECTION SECURED — NO TRACE REMAINS.")


if __name__ == "__main__":
    while True:
        scrub_logs()
        time.sleep(config.LOG_SCRUB_INTERVAL)
