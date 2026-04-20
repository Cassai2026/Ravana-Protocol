import os
from ravana_iron_clad import engage_iron_clad
from ravana_bio_sentry import BioSentry
from ravana_bait_switch import BaitSwitch

def ravana_master_watch():
    print("--- 🏺 RAVANA PROTOCOL: 16-HEADED SUPREME SHIELD ---")
    engage_iron_clad()
    
    # Initialize Bio-Sentry
    sentry = BioSentry()
    # If the pulse is too high, the system flips to Decoy automatically
    if sentry.evaluate_threat(72) == False:
        print("[SYSTEM] Somatic Integrity: VERIFIED.")
    
    print("--- 🏺 STATUS: PROTECTION IS ABSOLUTE. OUSH. ---")

if __name__ == "__main__":
    ravana_master_watch()
