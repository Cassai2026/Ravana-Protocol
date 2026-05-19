import os
import shutil


def is_windows() -> bool:
    """Return True when running on Windows (os.name == 'nt')."""
    return os.name == "nt"


def with_optional_sudo(command: list[str]) -> list[str]:
    """Prepend sudo on non-Windows when available and current user is not root."""
    if not is_windows() and hasattr(os, "geteuid") and os.geteuid() != 0 and shutil.which("sudo"):
        return ["sudo", *command]
    return command
