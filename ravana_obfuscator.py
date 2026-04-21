import random
import config


class DPIObfuscator:
    def __init__(self):
        self.chaff_size = config.CHAFF_SIZE

    def fragment_and_pad(self, data_stream: str) -> str:
        """Add random padding to data to make it resemble normal HTTPS traffic."""
        padded_data = data_stream + str(random.getrandbits(self.chaff_size))
        print("[RAVANA] 👻 HEAD 13: Packet obfuscated — signature masked.")
        return padded_data


if __name__ == "__main__":
    obfuscator = DPIObfuscator()
    obfuscator.fragment_and_pad("Sovereign_Data_Pulse")
