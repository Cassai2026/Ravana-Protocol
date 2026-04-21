"""
ravana_supreme.py — SINGLE ENTRY POINT
Boots the complete 16-headed Ravana Protocol shield.
Run:  python ravana_supreme.py
"""
import config
from ravana_core import RavanaCore
from ravana_iron_clad import engage_iron_clad
from ravana_bio_sentry import BioSentry
from ravana_bait_switch import BaitSwitch
from ravana_biometric import read_heart_rate


def ravana_master_watch():
    print("=" * 60)
    print(" 🏺  RAVANA PROTOCOL — 16-HEADED SUPREME SHIELD BOOT")
    print("=" * 60)
    print(f" SDG 18-22 Compliance: ACTIVE | Heads: {len(config.HEAD_MAP)}")
    print("=" * 60)

    # ── PHASE 1: Heads 1-7 via RavanaCore ────────────────────────────────────
    print("\n[PHASE 1] Engaging Heads 1-7 (Core Shield)...")
    core = RavanaCore()
    core.engage_shield()

    # ── PHASE 2: Heads 10-14 via IronClad ────────────────────────────────────
    print("\n[PHASE 2] Engaging Heads 10-14 (Iron-Clad Activation)...")
    hr = read_heart_rate()
    engage_iron_clad(hr_input=hr)

    # ── PHASE 3: Head 15 — Bio-Sentry coercion check ─────────────────────────
    print("\n[PHASE 3] Engaging HEAD 15 (Biometric Coercion Detector)...")
    sentry = BioSentry()
    if not sentry.evaluate_threat(hr):
        print("[SYSTEM] HEAD 15: Somatic integrity verified — no coercion detected.")

    # ── STATUS ────────────────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print(" 🏺  STATUS: PROTECTION IS ABSOLUTE. OUSH.")
    print("=" * 60)


if __name__ == "__main__":
    ravana_master_watch()
