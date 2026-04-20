import os

def deploy_bait():
    bait_path = "./vault_bait"
    if not os.path.exists(bait_path):
        os.makedirs(bait_path)
        with open(f"{bait_path}/passwords.txt", "w") as f:
            f.write("TRAP_ACTIVE: RAVANA_PROTOCOL_BREACH_DETECTED")
    print("[RAVANA] 🍯 BAIT DEPLOYED: Monitoring honey-pot for access.")

if __name__ == "__main__":
    deploy_bait()
