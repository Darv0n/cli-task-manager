"""ULID generation — pure Python, zero dependencies.

ULID = 48-bit timestamp (ms precision) + 80-bit randomness, base32-encoded.
Total: 26 characters. Monotonically sortable. URL-safe.
"""

from __future__ import annotations

import os
import time

_ENCODING = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"


def _encode(value: int, length: int) -> str:
    chars = []
    for _ in range(length):
        chars.append(_ENCODING[value & 0x1F])
        value >>= 5
    return "".join(reversed(chars))


def generate_id() -> str:
    """Generate a new ULID string (26 chars, base32, time-sortable)."""
    timestamp_ms = int(time.time() * 1000)
    randomness = int.from_bytes(os.urandom(10), byteorder="big")
    return _encode(timestamp_ms, 10) + _encode(randomness, 16)
