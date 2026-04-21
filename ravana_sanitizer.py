import subprocess
import config


class SignalSanitizer:
    def __init__(self):
        self.monitored_interfaces = config.MONITORED_INTERFACES
        self.authorized_macs = config.AUTHORIZED_MACS

    def scan_for_static(self) -> bool:
        """
        Scan each monitored interface for rogue probe requests using 'iw'.
        Falls back to nmcli-based check if iw is unavailable.
        Returns True if a rogue probe was detected, False otherwise.
        """
        print("[RAVANA] 📡 HEAD 6: SCANNING AIRWAVES FOR SIGNAL LEAKAGE...")
        rogue_detected = False

        for iface in self.monitored_interfaces:
            detected = self._iw_scan(iface) or self._nmcli_check(iface)
            if detected:
                rogue_detected = True
                break

        if rogue_detected:
            self.sanitize()
        else:
            print("[RAVANA] ✅ HEAD 6: Airwaves clean — no rogue probes detected.")

        return rogue_detected

    def _iw_scan(self, iface: str) -> bool:
        """Use 'iw dev <iface> scan' to check for unrecognised BSSIDs."""
        try:
            result = subprocess.run(
                ["iw", "dev", iface, "scan"],
                capture_output=True,
                text=True,
                timeout=15,
            )
            output = result.stdout
            detected_macs = []
            for line in output.splitlines():
                stripped = line.strip()
                if stripped.startswith("BSS"):
                    parts = stripped.split("BSS", 1)
                    if len(parts) > 1:
                        tokens = parts[1].strip().split()
                        if tokens:
                            detected_macs.append(tokens[0])
            for mac in detected_macs:
                if mac not in self.authorized_macs:
                    print(f"[RAVANA] 🚨 HEAD 6: Unauthorised BSSID detected via iw: {mac}")
                    return True
        except FileNotFoundError:
            pass  # iw not installed — try nmcli fallback
        except subprocess.TimeoutExpired:
            print("[RAVANA] ⚠️  HEAD 6: iw scan timed out.")
        except Exception as exc:
            print(f"[RAVANA] ⚠️  HEAD 6: iw scan error: {exc}")
        return False

    def _nmcli_check(self, iface: str) -> bool:
        """Use nmcli to list nearby access points and check for unauthorised entries."""
        try:
            result = subprocess.run(
                ["nmcli", "-t", "-f", "BSSID,ACTIVE", "device", "wifi", "list", "ifname", iface],
                capture_output=True,
                text=True,
                timeout=15,
            )
            for line in result.stdout.splitlines():
                parts = line.split(":")
                if len(parts) >= 2:
                    bssid = parts[0].strip()
                    if bssid and bssid not in self.authorized_macs:
                        print(f"[RAVANA] 🚨 HEAD 6: Unauthorised AP detected via nmcli: {bssid}")
                        return True
        except FileNotFoundError:
            pass  # nmcli not installed
        except subprocess.TimeoutExpired:
            print("[RAVANA] ⚠️  HEAD 6: nmcli scan timed out.")
        except Exception as exc:
            print(f"[RAVANA] ⚠️  HEAD 6: nmcli error: {exc}")
        return False

    def sanitize(self):
        print("[RAVANA] 🚨 HEAD 6: SIGNAL BREACH — UNAUTHORISED PROBE DETECTED.")
        print("[RAVANA] 🛡️  HEAD 6: INITIATING FREQUENCY SHIFT...")
        try:
            subprocess.run(["sudo", "nmcli", "networking", "off"], check=True, timeout=10)
            subprocess.run(["sudo", "nmcli", "networking", "on"], check=True, timeout=10)
            print("[RAVANA] ✅ HEAD 6: AIRWAVES SANITIZED — cognitive liberty maintained.")
        except Exception as exc:
            print(f"[RAVANA] ⚠️  HEAD 6: Sanitize failed: {exc}")


if __name__ == "__main__":
    sanitizer = SignalSanitizer()
    sanitizer.scan_for_static()
