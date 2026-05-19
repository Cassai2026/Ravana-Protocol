# 🏺 RAVANA PROTOCOL — THE 16-HEADED SHIELD

**SDG 18-22 Compliance | Cognitive Liberty Protection | Sovereign Edge Node**

---

## What Is This?

Ravana Protocol is a modular Python privacy and security framework designed to run on a Raspberry Pi 5 ("Lily-Pi" node). Inspired by the 16 heads of the demon-king Ravana, each module represents one defensive capability. Together they form a multi-layered shield protecting cognitive liberty, data sovereignty, and signal integrity.

The project is structured so that every "head" is an independent module that can be tested, extended, or replaced without touching the others. The single entry point is `ravana_supreme.py`.

---

## Canonical 16-Head Map

| Head | Name | Module |
|------|------|--------|
| 1  | Cognitive Liberty Monitor      | `ravana_core.py`         |
| 2  | Neural Path Encryption         | `ravana_core.py`         |
| 3  | Honeypot Bait Deployment       | `ravana_bait.py`         |
| 4  | Log Data Scrubbing             | `ravana_scrub.py`        |
| 5  | System Bloat Decimation        | `ravana_stripper.py`     |
| 6  | Signal Sanitization            | `ravana_sanitizer.py`    |
| 7  | Perceptual Ghost Traffic       | `ravana_ghost.py`        |
| 8  | Visual Privacy Sentinel        | `ravana_sentinel.py`     |
| 9  | Visual Buffer Purge            | `ravana_visual_purge.py` |
| 10 | Somatic Feedback Sync          | `ravana_ultimate.py`     |
| 11 | Neural Path Cloaking           | `ravana_ultimate.py`     |
| 12 | Auto Purge Trigger             | `ravana_ultimate.py`     |
| 13 | DPI Packet Obfuscation         | `ravana_obfuscator.py`   |
| 14 | Ghost Node Mirage              | `ravana_mirage.py`       |
| 15 | Biometric Coercion Detector    | `ravana_bio_sentry.py`   |
| 16 | Decoy Mode                     | `ravana_bait_switch.py`  |

---

## Repository Layout

```
Ravana-Protocol/
├── config.py               # Central constants — edit here to tune the shield
├── ravana_supreme.py       # ← SINGLE ENTRY POINT — run this
├── ravana_core.py          # Heads 1-7 orchestrator
├── ravana_ultimate.py      # Heads 10-12 (somatic, cloaking, purge)
├── ravana_iron_clad.py     # Full iron-clad activation sequence
├── ravana_biometric.py     # Heart-rate reader (file / GPIO / manual)
├── ravana_bait.py          # HEAD 3 — honeypot
├── ravana_scrub.py         # HEAD 4 — log scrubbing
├── ravana_stripper.py      # HEAD 5 — bloat removal
├── ravana_sanitizer.py     # HEAD 6 — WiFi signal scan
├── ravana_ghost.py         # HEAD 7 — perceptual noise
├── ravana_sentinel.py      # HEAD 8 — privacy camera
├── ravana_visual_purge.py  # HEAD 9 — CCTV buffer purge
├── ravana_obfuscator.py    # HEAD 13 — DPI obfuscation
├── ravana_mirage.py        # HEAD 14 — ghost node generator
├── ravana_bio_sentry.py    # HEAD 15 — biometric coercion detection
├── ravana_bait_switch.py   # HEAD 16 — decoy mode
├── ravana_ignite.py        # Boot-sequence alias
├── ravana_tunnel.py        # WireGuard tunnel rotator (helper)
├── requirements.txt
└── tests/
    └── test_ravana.py      # Basic unit tests
```

---

## Requirements

- Raspberry Pi 5 (or any Linux/Windows host for development/simulation)
- Python 3.10+
- WireGuard installed and configured for tunnel rotation
- `iw` and `nmcli` for signal sanitization (Linux hosts)

Install Python dependencies:

```bash
pip install -r requirements.txt
```

> `RPi.GPIO` is only installed automatically on `aarch64` (Raspberry Pi) hardware.

---

## Running the Shield

```bash
python ravana_supreme.py
```

This boots all 16 heads in sequence and leaves the Bio-Sentry watching for coercion events.

### Windows note

On Windows, Linux-only operations are skipped automatically:
- systemd service decimation (`systemctl`)
- Linux log truncation (`truncate` in `/var/log`)
- Linux wireless controls (`iw` / `nmcli`)
- WireGuard tunnel rotation via `wg-quick`

Core module flow, biometric file / manual input, audit logging, mirage/obfuscation, and tests still run.

### Biometric Input (Heart Rate)

The shield reads heart-rate from one of three configurable sources (set `HR_INPUT_SOURCE` in `config.py`):

| Source | Description |
|--------|-------------|
| `"file"` | Reads from the OS temp directory (default file: `ravana_hr.txt`) — write a number (e.g. `72`) to this file from any sensor script |
| `"gpio"` | Reads a pulse-count pin via `RPi.GPIO` (requires hardware) |
| `"manual"` | Uses the `HR_MANUAL_DEFAULT` constant — good for testing |

---

## Configuration

All tunable constants live in `config.py`. Key values:

| Constant | Default | Description |
|----------|---------|-------------|
| `BASELINE_HR` | 70 | Resting heart rate (bpm) |
| `COERCION_LIMIT` | 145 | HR spike that triggers ghost purge |
| `CHAFF_SIZE` | 1024 | DPI padding size in bits |
| `LOG_SCRUB_INTERVAL` | 60 | Seconds between log wipes |
| `WIREGUARD_ENDPOINTS` | 3 nodes | Sovereign mesh tunnel points |

---

## Goals (SDG 18-22)

- **SDG 18** — Cognitive Liberty: no entity may observe, intercept, or coerce mental/digital sovereignty
- **SDG 19** — Signal Integrity: communications remain clean and unmonitored
- **SDG 20** — Data Autonomy: logs purged, no residue left for adversaries
- **SDG 21** — Somatic Safety: biometric stress detection prevents coerced access
- **SDG 22** — Deception Resilience: mirage nodes and decoy modes frustrate surveillance

---

## OUSH.

---

## Quick Start — Raspberry Pi 5

### 1. Install system dependencies

```bash
sudo apt update && sudo apt install -y wireguard iw network-manager python3-pip
```

### 2. Deploy the protocol

```bash
sudo mkdir -p /opt/ravana-protocol
sudo cp -r . /opt/ravana-protocol
cd /opt/ravana-protocol
sudo pip3 install -r requirements.txt
```

### 3. Configure WireGuard tunnels

Place your peer configuration files in `/etc/wireguard/`:

```
/etc/wireguard/wg-uk-lon-01.conf
/etc/wireguard/wg-se-sto-01.conf
/etc/wireguard/wg-ch-zur-01.conf
```

Then update `WIREGUARD_ENDPOINTS` in `config.py` to match those filenames (without `.conf`).

### 4. Wire the MAX30102 heart-rate sensor

Connect the MAX30102 module to the Pi 5 40-pin header:

| MAX30102 pin | Pi 5 header pin | BCM GPIO |
|---|---|---|
| VIN | Pin 1 (3.3 V) | — |
| GND | Pin 6 (GND) | — |
| SDA | Pin 3 | GPIO 2 |
| SCL | Pin 5 | GPIO 3 |
| INT | **Pin 11** | **GPIO 17** ← pulse input |

Set `HR_INPUT_SOURCE = "gpio"` in `config.py`. The `GPIO_HR_PIN` constant (default `17`) controls which BCM pin is polled.

> **Note:** `RPi.GPIO` is only installed automatically on `aarch64` (Raspberry Pi) hardware; it is skipped on x86 dev machines.

### 5. Enable service decimation (optional)

Set `ENABLE_SERVICE_DECIMATION = True` in `config.py` to disable the bloat services listed in `BLOAT_SERVICES` at each boot.

### 6. Install the systemd service

```bash
sudo cp ravana.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable ravana.service
sudo systemctl start ravana.service
```

Check status:

```bash
sudo systemctl status ravana.service
journalctl -u ravana.service -f
```
