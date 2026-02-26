"""Input validators for CLI arguments.

Pure functions that parse CLI string inputs into domain types.
Raise typer.BadParameter on failure.
"""

from __future__ import annotations

from datetime import date, timedelta

import typer

_NATURAL_DATES: dict[str, object] = {
    "today": lambda: date.today(),
    "tomorrow": lambda: date.today() + timedelta(days=1),
    "yesterday": lambda: date.today() - timedelta(days=1),
    "next week": lambda: date.today() + timedelta(weeks=1),
}

_DATE_FORMATS = ["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y"]


def parse_due_date(value: str) -> date:
    """Parse a due date from natural language or ISO format.

    Accepts: 'today', 'tomorrow', 'next week', 'YYYY-MM-DD', 'DD/MM/YYYY'
    """
    normalized = value.lower().strip()

    if normalized in _NATURAL_DATES:
        return _NATURAL_DATES[normalized]()

    # Try ISO format first
    try:
        return date.fromisoformat(value)
    except ValueError:
        pass

    # Try other formats
    from datetime import datetime

    for fmt in _DATE_FORMATS[1:]:
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            continue

    raise typer.BadParameter(
        f"Cannot parse date: {value!r}. "
        f"Use YYYY-MM-DD, DD/MM/YYYY, or natural language (today, tomorrow, 'next week')."
    )
