import os

def purge_buffer():
    # Only keep the last 60 seconds of 'Problem' footage, delete everything else.
    print("[RAVANA] 🧼 HEAD 8: PURGING NON-CRITICAL VISUAL BUFFER...")
    # os.system("rm -rf /tmp/cctv_buffer/*")

if __name__ == "__main__":
    purge_buffer()
