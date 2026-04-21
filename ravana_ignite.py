"""
ravana_ignite.py — Boot-sequence alias.
Calls ravana_supreme.py's master watch loop.
Prefer running ravana_supreme.py directly.
"""
from ravana_supreme import ravana_master_watch

if __name__ == "__main__":
    ravana_master_watch()
