import os
import shutil
import config


def purge_buffer():
    """Keep only the last CCTV_RETENTION_SECONDS of footage; delete everything else."""
    print("[RAVANA] 🧼 HEAD 9: PURGING NON-CRITICAL VISUAL BUFFER...")
    buffer_path = config.CCTV_BUFFER_PATH
    if os.path.isdir(buffer_path):
        for entry in os.scandir(buffer_path):
            if entry.is_dir(follow_symlinks=False):
                shutil.rmtree(entry.path)
            elif entry.is_file(follow_symlinks=False):
                os.remove(entry.path)
        print(f"[RAVANA] ✅ HEAD 9: Buffer cleared at {buffer_path}")
    else:
        print(f"[RAVANA] HEAD 9: Buffer path not found — nothing to purge ({buffer_path})")


if __name__ == "__main__":
    purge_buffer()
