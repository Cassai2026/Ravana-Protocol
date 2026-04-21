import config
from ravana_bait import deploy_bait
from ravana_scrub import scrub_logs
from ravana_stripper import LogicStripper
from ravana_sanitizer import SignalSanitizer
from ravana_ghost import PerceptualGhost


class RavanaCore:
    def __init__(self):
        self.heads_active = len(config.HEAD_MAP)
        self.status = "SOVEREIGN"

    def engage_shield(self):
        print("--- 🏺 RAVANA PROTOCOL: SHIELD IGNITION ---")

        print(f"[HEAD  1] {config.HEAD_MAP[1]}: monitoring cognitive liberty (SDG 18)...")

        print(f"[HEAD  2] {config.HEAD_MAP[2]}: encrypting neural paths...")

        print(f"[HEAD  3] {config.HEAD_MAP[3]}: deploying honeypot...")
        deploy_bait()

        print(f"[HEAD  4] {config.HEAD_MAP[4]}: scrubbing logs...")
        scrub_logs()

        print(f"[HEAD  5] {config.HEAD_MAP[5]}: identifying system bloat...")
        stripper = LogicStripper()
        stripper.identify_bloat()
        # stripper.decimate()  # Uncomment to actively remove services on the Pi

        print(f"[HEAD  6] {config.HEAD_MAP[6]}: scanning airwaves...")
        SignalSanitizer().scan_for_static()

        print(f"[HEAD  7] {config.HEAD_MAP[7]}: initiating ghost broadcast...")
        # Run one noise broadcast (the infinite loop is available via PerceptualGhost.active_deception_loop)
        PerceptualGhost().broadcast_noise()

        return True


if __name__ == "__main__":
    guard = RavanaCore()
    guard.engage_shield()
