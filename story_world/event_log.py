from __future__ import annotations

import json
from pathlib import Path

from .models import EventLogEntry


class EventLog:
    """Append-only in-memory log with optional JSONL persistence."""

    def __init__(self, path: Path | None = None) -> None:
        self._events: list[EventLogEntry] = []
        self._path = path
        if self._path is not None:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            self._path.write_text("", encoding="utf-8")

    @property
    def events(self) -> tuple[EventLogEntry, ...]:
        return tuple(self._events)

    def append(self, event: EventLogEntry) -> EventLogEntry:
        expected_sequence = len(self._events) + 1
        if event.sequence != expected_sequence:
            raise ValueError(
                f"event {event.event_id} sequence {event.sequence} does not match "
                f"expected {expected_sequence}"
            )
        self._events.append(event)
        if self._path is not None:
            with self._path.open("a", encoding="utf-8") as fp:
                fp.write(json.dumps(event.to_json_dict(), ensure_ascii=False) + "\n")
        return event

    def next_sequence(self) -> int:
        return len(self._events) + 1
