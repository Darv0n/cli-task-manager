"""Task domain model. Imports from contracts, not the other way around."""

from __future__ import annotations

from datetime import date
from typing import Any

from pydantic import BaseModel, Field, field_validator

from task_manager.contracts import Priority, Status
from task_manager.utils.ids import generate_id
from task_manager.utils.time import utcnow_iso


class Task(BaseModel):
    model_config = {"str_strip_whitespace": True}

    id: str = Field(default_factory=generate_id)
    title: str = Field(min_length=1, max_length=500)
    description: str = Field(default="")
    status: Status = Status.OPEN
    priority: Priority = Priority.MEDIUM
    tags: list[str] = Field(default_factory=list)
    project: str | None = None
    context: str | None = None
    due_date: date | None = None
    created_at: str = Field(default_factory=utcnow_iso)
    updated_at: str = Field(default_factory=utcnow_iso)

    @field_validator("tags", mode="before")
    @classmethod
    def normalize_tags(cls, v: Any) -> list[str]:
        if isinstance(v, str):
            v = [t.strip() for t in v.split(",") if t.strip()]
        return [tag.lower().strip() for tag in v]

    @field_validator("project", "context", mode="before")
    @classmethod
    def strip_prefix_sigils(cls, v: Any) -> str | None:
        """Allow '+myproject' or '@home' as input, store without sigil."""
        if isinstance(v, str):
            return v.lstrip("+@").strip() or None
        return v

    def mark_updated(self) -> None:
        self.updated_at = utcnow_iso()

    def to_storage(self) -> dict[str, Any]:
        """Serialize for storage. due_date as ISO string, enums as values."""
        data = self.model_dump()
        if data["due_date"] is not None:
            data["due_date"] = data["due_date"].isoformat()
        data["status"] = self.status.value
        data["priority"] = self.priority.value
        return data

    @classmethod
    def from_storage(cls, data: dict[str, Any]) -> Task:
        """Deserialize from storage dict."""
        return cls.model_validate(data)
