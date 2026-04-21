import os
import stat
import config


def deploy_bait():
    if not os.path.exists(config.BAIT_VAULT_PATH):
        os.makedirs(config.BAIT_VAULT_PATH)
    bait_file = os.path.join(config.BAIT_VAULT_PATH, config.BAIT_FILE_NAME)
    if not os.path.exists(bait_file):
        with open(bait_file, "w") as f:
            f.write(config.BAIT_CONTENT)
    # World-readable so adversaries are attracted; only owner (root) can write.
    try:
        os.chmod(config.BAIT_VAULT_PATH, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
        os.chmod(bait_file, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
    except OSError:
        pass  # Non-fatal — permissions may already be correct or running as non-root
    print("[RAVANA] 🍯 HEAD 3: BAIT DEPLOYED — monitoring honey-pot for access.")


if __name__ == "__main__":
    deploy_bait()

