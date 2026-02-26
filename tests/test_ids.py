"""Tests for ULID generation."""

from task_manager.utils.ids import generate_id


def test_ulid_length():
    ulid = generate_id()
    assert len(ulid) == 26


def test_ulid_uniqueness():
    ids = {generate_id() for _ in range(100)}
    assert len(ids) == 100


def test_ulid_sortable():
    """ULIDs generated in sequence should sort in creation order."""
    import time

    id1 = generate_id()
    time.sleep(0.002)
    id2 = generate_id()
    assert id1 < id2


def test_ulid_characters():
    """ULID should only contain Crockford base32 chars."""
    valid = set("0123456789ABCDEFGHJKMNPQRSTVWXYZ")
    ulid = generate_id()
    assert all(c in valid for c in ulid)
