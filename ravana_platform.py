import os
import shutil


def is_windows() -> bool:
    return os.name == "nt"


def with_optional_sudo(command: list[str]) -> list[str]:
    if not is_windows() and hasattr(os, "geteuid") and os.geteuid() != 0 and shutil.which("sudo"):
        return ["sudo", *command]
    return command
