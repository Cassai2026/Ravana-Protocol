import random
import time
import requests
import config


class PerceptualGhost:
    def __init__(self):
        self.noise_targets = config.GHOST_NOISE_TARGETS

    def broadcast_noise(self):
        print("[RAVANA] 👻 HEAD 7: BROADCASTING PERCEPTUAL NOISE...")
        target = random.choice(self.noise_targets)
        try:
            requests.get(target, timeout=5)
            print(f"[RAVANA] HEAD 7: Ghost traffic directed to: {target}")
        except Exception:
            print(f"[RAVANA] HEAD 7: Ghost ping failed for {target} — noise pattern maintained.")

    def active_deception_loop(self):
        while True:
            self.broadcast_noise()
            interval = random.randint(
                config.GHOST_INTERVAL_MIN, config.GHOST_INTERVAL_MAX
            )
            time.sleep(interval)


if __name__ == "__main__":
    ghost = PerceptualGhost()
    ghost.active_deception_loop()
