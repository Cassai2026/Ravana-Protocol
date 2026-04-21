"""
ravana_biometric.py — HEAD 10 support
Reads heart rate from a configurable source:
  "file"   — reads an integer from HR_INPUT_FILE
  "gpio"   — reads a pulse-count GPIO pin (Raspberry Pi only)
  "manual" — returns HR_MANUAL_DEFAULT (for testing / simulation)
"""
import config


def read_heart_rate() -> int:
    """Return current heart rate in bpm from the configured source."""
    source = config.HR_INPUT_SOURCE

    if source == "file":
        return _read_from_file()
    if source == "gpio":
        return _read_from_gpio()
    # Default: manual / simulation
    return config.HR_MANUAL_DEFAULT


def _read_from_file() -> int:
    """Read a single integer from HR_INPUT_FILE, falling back to the manual default."""
    try:
        with open(config.HR_INPUT_FILE, "r") as fh:
            return int(fh.read().strip())
    except (OSError, ValueError):
        print(
            f"[RAVANA] ⚠️  Could not read HR from {config.HR_INPUT_FILE}. "
            f"Using manual default ({config.HR_MANUAL_DEFAULT} bpm)."
        )
        return config.HR_MANUAL_DEFAULT


def _read_from_gpio() -> int:
    """
    Read heart rate from a GPIO pulse-count pin on Raspberry Pi.
    Requires RPi.GPIO and a hardware pulse sensor on GPIO pin 17.
    Falls back to manual default if GPIO is unavailable.
    """
    try:
        import RPi.GPIO as GPIO  # noqa: N813  (Pi-only import)
        import time

        PIN = 17
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        pulse_count = 0
        start = time.time()
        while time.time() - start < config.HR_SAMPLE_WINDOW_SECONDS:
            if GPIO.input(PIN) == GPIO.LOW:
                pulse_count += 1
                time.sleep(0.01)

        GPIO.cleanup()
        bpm = pulse_count * (60 // config.HR_SAMPLE_WINDOW_SECONDS)
        return bpm
    except ImportError:
        print("[RAVANA] ⚠️  RPi.GPIO not available. Using manual default.")
        return config.HR_MANUAL_DEFAULT
    except Exception as exc:
        print(f"[RAVANA] ⚠️  GPIO read error: {exc}. Using manual default.")
        return config.HR_MANUAL_DEFAULT


if __name__ == "__main__":
    hr = read_heart_rate()
    print("[RAVANA] ❤️  Heart rate reading acquired.")
