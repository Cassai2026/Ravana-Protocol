"""
ravana_audit.py — Encrypted Append-Only Audit Log
Records every shield event (boot, HR reading, phase completions, coercion
triggers) to a Fernet-encrypted log file.  A symmetric key is auto-generated
on first run and stored at AUDIT_KEY_FILE.
"""
import datetime
import json
import os

import config


def _load_or_create_key() -> bytes:
    """Return the Fernet key, generating and saving a new one if absent."""
    from cryptography.fernet import Fernet

    key_path = config.AUDIT_KEY_FILE
    if os.path.exists(key_path):
        with open(key_path, "rb") as fh:
            return fh.read()
    key = Fernet.generate_key()
    with open(key_path, "wb") as fh:
        fh.write(key)
    # Restrict key file to owner-only read/write
    try:
        os.chmod(key_path, 0o600)
    except OSError:
        pass
    return key


def log_event(event_type: str, detail: str = "") -> None:
    """
    Append an encrypted JSON record to the audit log.

    Each record has the shape:
        {"ts": "<ISO-8601>", "event": "<event_type>", "detail": "<detail>"}

    Parameters
    ----------
    event_type : str
        Short label, e.g. "SHIELD_BOOT", "HR_READING", "COERCION_DETECTED".
    detail : str
        Optional extra context appended to the record.
    """
    try:
        from cryptography.fernet import Fernet

        key = _load_or_create_key()
        fernet = Fernet(key)
        record = json.dumps({
            "ts": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
            "event": event_type,
            "detail": detail,
        })
        token = fernet.encrypt(record.encode())
        with open(config.AUDIT_LOG_FILE, "ab") as fh:
            fh.write(token + b"\n")
    except Exception as exc:
        print(f"[RAVANA] ⚠️  AUDIT: could not write log entry: {exc}")


def read_audit_log() -> list[dict]:
    """
    Decrypt and return all audit log entries as a list of dicts.
    Entries that cannot be decrypted are skipped with a warning.
    """
    from cryptography.fernet import Fernet, InvalidToken

    key = _load_or_create_key()
    fernet = Fernet(key)
    entries = []
    try:
        with open(config.AUDIT_LOG_FILE, "rb") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    entries.append(json.loads(fernet.decrypt(line).decode()))
                except (InvalidToken, json.JSONDecodeError) as exc:
                    print(f"[RAVANA] ⚠️  AUDIT: skipping unreadable entry: {exc}")
    except FileNotFoundError:
        pass
    return entries


if __name__ == "__main__":
    log_event("AUDIT_SELF_TEST", "ravana_audit.py executed directly")
    print("[RAVANA] 📋 AUDIT: Self-test entry written.")
    for entry in read_audit_log():
        print(entry)
