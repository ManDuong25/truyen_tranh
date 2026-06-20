from __future__ import annotations

from .event_log import EventLog
from .models import CharacterIntent, EventLogEntry, EventTier, WorldSeed, world_seed_to_snapshot


class GMResolver:
    """Single authority that converts intents into committed events."""

    def __init__(self, seed: WorldSeed, event_log: EventLog) -> None:
        self.seed = seed
        self.event_log = event_log

    def initialize_run(self) -> EventLogEntry:
        if self.event_log.events:
            raise ValueError("run already initialized")
        return self._append(
            tick=0,
            tier=EventTier.SYSTEM,
            event_type="run_initialized",
            actor_ids=(),
            observer_ids=(),
            visible_to=tuple(self.seed.characters),
            summary=(
                f"Run {self.seed.run_id} begins at {self.seed.location} in "
                f"{self.seed.world_name}."
            ),
            payload={
                "world_name": self.seed.world_name,
                "location": self.seed.location,
                "character_ids": sorted(self.seed.characters),
            },
            sealed_payload={
                "initial_state": world_seed_to_snapshot(self.seed),
            },
        )

    def resolve_tick(self, tick: int, intents: list[CharacterIntent]) -> list[EventLogEntry]:
        events: list[EventLogEntry] = []
        intent_by_actor = {intent.character_id: intent for intent in intents}
        if "linh" in intent_by_actor and "khai" in intent_by_actor:
            events.append(self._resolve_linh_khai_conflict(tick, intent_by_actor))
        if "minh" in intent_by_actor:
            events.append(self._resolve_minh_observation(tick, intent_by_actor["minh"]))
        return events

    def _resolve_linh_khai_conflict(
        self, tick: int, intent_by_actor: dict[str, CharacterIntent]
    ) -> EventLogEntry:
        linh_intent = intent_by_actor["linh"]
        khai_intent = intent_by_actor["khai"]
        minh_can_overhear = tick >= 2
        visible_to = ("linh", "khai", "minh") if minh_can_overhear else ("linh", "khai")
        observer_ids = ("minh",) if minh_can_overhear else ()
        summary = (
            "Linh confronts Khai about her father. Khai gives an evasive answer "
            "that increases Linh's suspicion without revealing his oath."
        )
        if tick == 3:
            summary = (
                "Khai admits the night of Linh's father's disappearance was more "
                "dangerous than rumor says, but he still withholds the oath-bound truth."
            )
        return self._append(
            tick=tick,
            tier=EventTier.CANON,
            event_type="dialogue_conflict",
            actor_ids=("linh", "khai"),
            observer_ids=observer_ids,
            visible_to=visible_to,
            summary=summary,
            payload={
                "intents": [
                    self._public_intent(linh_intent),
                    self._public_intent(khai_intent),
                ],
                "spoken_lines": {
                    "linh": self._redact_private_knowledge(linh_intent.spoken_line),
                    "khai": self._redact_private_knowledge(khai_intent.spoken_line),
                },
                "relationship_deltas": [
                    {
                        "from": "linh",
                        "to": "khai",
                        "trust": -2,
                        "tension": 3,
                        "reason": "Khai kept answering around the truth.",
                    },
                    {
                        "from": "khai",
                        "to": "linh",
                        "trust": 0,
                        "tension": 2,
                        "reason": "Khai's guilt increased under Linh's pressure.",
                    },
                ],
                "salience": 8,
            },
        )

    def _resolve_minh_observation(
        self, tick: int, intent: CharacterIntent
    ) -> EventLogEntry:
        return self._append(
            tick=tick,
            tier=EventTier.SUPPORTING_OBSERVATION,
            event_type="private_observation",
            actor_ids=("minh",),
            observer_ids=("minh",),
            visible_to=("minh",),
            summary=(
                "Minh stays hidden and notes the growing distrust between Linh "
                "and Khai, but he does not learn Khai's unrevealed secret."
            ),
            payload={
                "intent": self._public_intent(intent),
                "salience": 6,
            },
        )

    def _append(
        self,
        *,
        tick: int,
        tier: EventTier,
        event_type: str,
        actor_ids: tuple[str, ...],
        observer_ids: tuple[str, ...],
        visible_to: tuple[str, ...],
        summary: str,
        payload: dict,
        sealed_payload: dict | None = None,
    ) -> EventLogEntry:
        sequence = self.event_log.next_sequence()
        event = EventLogEntry(
            event_id=f"evt_{sequence:04d}",
            sequence=sequence,
            run_id=self.seed.run_id,
            tick=tick,
            tier=tier,
            event_type=event_type,
            actor_ids=actor_ids,
            observer_ids=observer_ids,
            visible_to=visible_to,
            summary=summary,
            payload=payload,
            sealed_payload=sealed_payload or {},
        )
        return self.event_log.append(event)

    def _public_intent(self, intent: CharacterIntent) -> dict:
        return {
            "character_id": self._redact_private_knowledge(intent.character_id),
            "intent_type": self._redact_private_knowledge(intent.intent_type),
            "target_id": self._redact_optional_private_knowledge(intent.target_id),
            "surface_action": self._redact_private_knowledge(intent.surface_action),
            "spoken_line": self._redact_private_knowledge(intent.spoken_line),
            "desired_outcome": self._redact_private_knowledge(intent.desired_outcome),
            "raw_inner_motive_stored": False,
            "raw_metadata_stored": False,
        }

    def _redact_private_knowledge(self, value: str) -> str:
        redacted = value
        for secret in self.seed.secrets.values():
            redacted = redacted.replace(secret.id, "[redacted_private_secret_id]")
            redacted = redacted.replace(secret.truth, "[redacted_private_secret]")
        return redacted

    def _redact_optional_private_knowledge(self, value: str | None) -> str | None:
        if value is None:
            return None
        return self._redact_private_knowledge(value)
