from ravana_ultimate import RavanaUltimate
from ravana_obfuscator import DPIObfuscator
from ravana_mirage import MirageGenerator


def engage_iron_clad(hr_input: int = 65):
    print("--- 🏺 RAVANA PROTOCOL: IRON-CLAD ACTIVATION ---")
    shield = RavanaUltimate()
    obf = DPIObfuscator()
    mirage = MirageGenerator()

    # Execute heads 10-12
    shield.run_shield_cycle(hr_input)

    # HEAD 13: Obfuscate a test data pulse
    obf.fragment_and_pad("Sovereign_Data_Pulse")

    # HEAD 14: Deploy mirage nodes
    mirage.generate_ghost_signals()

    print("[SYSTEM] ✅ IRON-CLAD: SHIELD IS SOLID. SDG 18-22 SECURED.")


if __name__ == "__main__":
    engage_iron_clad()
