import config
from ravana_audit import log_event


class BioSentry:
    def __init__(self, baseline_hr: int = None):
        self.baseline = baseline_hr if baseline_hr is not None else config.BASELINE_HR
        self.coercion_limit = config.COERCION_LIMIT

    def evaluate_threat(self, current_hr: int) -> bool:
        """
        Return True if coercion is detected (HR >= coercion_limit),
        triggering the ghost purge sequence.
        """
        if current_hr >= self.coercion_limit:
            print("[RAVANA] 🚨 HEAD 15: COERCION DETECTED — biometric spike out of safety bounds.")
            log_event("COERCION_DETECTED", f"hr={current_hr} limit={self.coercion_limit}")
            self.trigger_ghost_purge()
            return True
        return False

    def trigger_ghost_purge(self):
        """Wire the coercion response to actual purge and decoy modules."""
        print("[RAVANA] 💀 HEAD 15: GHOST PROTOCOL ENGAGED — purging RAM-vault for cognitive liberty.")

        # Activate decoy mode to hide the real node
        try:
            from ravana_bait_switch import BaitSwitch
            BaitSwitch().engage_decoy()
        except Exception as exc:
            print(f"[RAVANA] ⚠️  Decoy activation failed: {exc}")

        # Purge the visual buffer
        try:
            from ravana_visual_purge import purge_buffer
            purge_buffer()
        except Exception as exc:
            print(f"[RAVANA] ⚠️  Visual purge failed: {exc}")

        # Deploy honeypot bait to catch the intruder
        try:
            from ravana_bait import deploy_bait
            deploy_bait()
        except Exception as exc:
            print(f"[RAVANA] ⚠️  Bait deployment failed: {exc}")

        print("[RAVANA] 🏺 HEAD 15: Node going dark. OUSH.")


if __name__ == "__main__":
    sentry = BioSentry()
    sentry.evaluate_threat(150)  # Simulate a coercion event
