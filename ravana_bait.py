import os
import config


def deploy_bait():
    if not os.path.exists(config.BAIT_VAULT_PATH):
        os.makedirs(config.BAIT_VAULT_PATH)
        bait_file = os.path.join(config.BAIT_VAULT_PATH, config.BAIT_FILE_NAME)
        with open(bait_file, "w") as f:
            f.write(config.BAIT_CONTENT)
    print("[RAVANA] 🍯 HEAD 3: BAIT DEPLOYED — monitoring honey-pot for access.")


if __name__ == "__main__":
    deploy_bait()
