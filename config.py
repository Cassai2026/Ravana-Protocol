"""
config.py — Ravana Protocol Central Configuration
All constants used across modules are defined here.
Edit this file to tune the shield for your environment.
"""
from pathlib import Path
import tempfile

TEMP_DIR = Path(tempfile.gettempdir())

# ── Biometric ─────────────────────────────────────────────────────────────────
BASELINE_HR = 70                    # Resting heart rate (bpm)
COERCION_LIMIT = 145                # Stress threshold that triggers ghost purge
HR_INPUT_SOURCE = "file"            # "file" | "gpio" | "manual"
HR_INPUT_FILE = str(TEMP_DIR / "ravana_hr.txt")  # Written by sensor integration
HR_SAMPLE_WINDOW_SECONDS = 10       # GPIO sampling window length
HR_MANUAL_DEFAULT = 72              # Used when source = "manual"
# MAX30102 pulse sensor: connect INT pin to BCM GPIO 17 (physical pin 11)
GPIO_HR_PIN = 17

# ── Service Control ───────────────────────────────────────────────────────────
# Set True on Raspberry Pi 5 to actively disable bloat services at boot
ENABLE_SERVICE_DECIMATION = False

# ── Network / Tunnel ──────────────────────────────────────────────────────────
# Replace these with your real WireGuard peer config names (wg-quick profile names).
# Each string must match a profile under /etc/wireguard/<name>.conf on the Pi.
WIREGUARD_ENDPOINTS = [
    "wg-uk-lon-01",     # UK sovereign relay — London
    "wg-se-sto-01",     # Sweden relay — Stockholm
    "wg-ch-zur-01",     # Switzerland relay — Zurich
]
MONITORED_INTERFACES = ["wlan0", "eth0"]
AUTHORIZED_MACS = ["NODE_29_OAKLEY", "TRAFFORD_MESH_PRIMARY"]

# ── DPI Obfuscation ───────────────────────────────────────────────────────────
CHAFF_SIZE = 1024                   # Random-padding size in bits

# ── Ghost Traffic ─────────────────────────────────────────────────────────────
GHOST_NOISE_TARGETS = [
    "https://www.bbc.com/weather",
    "https://www.wikipedia.org/wiki/Main_Page",
    "https://www.standard.co.uk",
]
GHOST_INTERVAL_MIN = 30             # Seconds between noise broadcasts (min)
GHOST_INTERVAL_MAX = 120            # Seconds between noise broadcasts (max)

# ── Log Scrubbing ─────────────────────────────────────────────────────────────
LOG_SCRUB_TARGETS = ["/var/log/auth.log", "/var/log/syslog"]
LOG_SCRUB_INTERVAL = 60             # Seconds between scrub cycles

# ── Visual Buffer ─────────────────────────────────────────────────────────────
CCTV_BUFFER_PATH = str(TEMP_DIR / "cctv_buffer")
CCTV_RETENTION_SECONDS = 60

# ── Bloat Services ────────────────────────────────────────────────────────────
BLOAT_SERVICES = [
    "avahi-daemon",       # Local discovery — leakage risk
    "bluetooth",          # Keep off for signal purity unless needed
    "cups",               # Printing — irrelevant for edge node
    "packagekit",         # Auto-updates — unauthorised system changes
    "whoopsie",           # Ubuntu error reporting — telemetry
    "snapd",              # Snap daemon — telemetry + unnecessary on Pi 5
    "ModemManager",       # Modem management — irrelevant for edge node
    "triggerhappy",       # Key daemon — unnecessary on Pi 5
    "hciuart",            # Bluetooth UART — matches bluetooth above
]

# ── Honeypot ──────────────────────────────────────────────────────────────────
BAIT_VAULT_PATH = "./vault_bait"
BAIT_FILE_NAME = "passwords.txt"
BAIT_CONTENT = "TRAP_ACTIVE: RAVANA_PROTOCOL_BREACH_DETECTED"

# ── Decoy Mode ────────────────────────────────────────────────────────────────
DECOY_PORT = 8080                   # Port for the HEAD 16 fake HTTP responder

# ── Audit Log ─────────────────────────────────────────────────────────────────
AUDIT_LOG_FILE = str(TEMP_DIR / "ravana_audit.log")    # Encrypted append-only event log
AUDIT_KEY_FILE = str(TEMP_DIR / "ravana_audit.key")    # Fernet key (auto-generated on first run)

# ── Canonical Head Map ────────────────────────────────────────────────────────
HEAD_MAP = {
    1:  "Cognitive Liberty Monitor",
    2:  "Neural Path Encryption",
    3:  "Honeypot Bait Deployment",
    4:  "Log Data Scrubbing",
    5:  "System Bloat Decimation",
    6:  "Signal Sanitization",
    7:  "Perceptual Ghost Traffic",
    8:  "Visual Privacy Sentinel",
    9:  "Visual Buffer Purge",
    10: "Somatic Feedback Sync",
    11: "Neural Path Cloaking",
    12: "Auto Purge Trigger",
    13: "DPI Packet Obfuscation",
    14: "Ghost Node Mirage",
    15: "Biometric Coercion Detector",
    16: "Decoy Mode",
}
