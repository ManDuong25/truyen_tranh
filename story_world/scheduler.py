from __future__ import annotations


class TieredScheduler:
    """Small deterministic scheduler for the POC."""

    def active_characters_for_tick(self, tick: int) -> tuple[str, ...]:
        if tick == 1:
            return ("linh", "khai")
        return ("linh", "khai", "minh")
