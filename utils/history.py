"""
CipherVault – Operation History
Stores recent operations in session state (no plaintext/keys logged).
"""

import datetime


def add_history_entry(history: list, algorithm: str, operation: str, detail: str = "") -> list:
    """
    Append an entry to the history list.
    Does NOT store plaintext or keys for security.
    """
    entry = {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "algorithm": algorithm,
        "operation": operation,
        "detail": detail,
    }
    history.insert(0, entry)  # Most recent first
    # Keep only last 50 entries
    return history[:50]


def clear_history(history: list) -> list:
    """Clear all history entries."""
    return []
