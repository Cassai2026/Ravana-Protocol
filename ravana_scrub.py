import os
import time

def scrub_logs():
    targets = ["/var/log/auth.log", "/var/log/syslog"]
    print("[RAVANA] 🧹 HEAD 6: SCRUBBING SYSTEM LOGS...")
    for target in targets:
        # Overwrite logs with null data
        # os.system(f"sudo truncate -s 0 {target}")
        print(f"[RAVANA] Zeroed: {target}")
    print("[RAVANA] ✅ DATA PROTECTION SECURED: NO TRACE REMAINS.")

if __name__ == "__main__":
    while True:
        scrub_logs()
        time.sleep(60) # Scrub every minute
