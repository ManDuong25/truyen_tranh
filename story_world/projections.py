from __future__ import annotations

from copy import deepcopy

from .models import (
    CharacterMemoryView,
    EventLogEntry,
    EventTier,
    MemoryRecord,
    RelationshipState,
    WorldSeed,
)


class ProjectionStore:
    """Derived state rebuilt from committed events."""

    def __init__(self, seed: WorldSeed) -> None:
        self.seed = seed
        self.tick = 0
        self._memories: dict[str, list[MemoryRecord]] = {
            character_id: [] for character_id in seed.characters
        }
        self._known_secret_ids: dict[str, set[str]] = {
            character_id: set() for character_id in seed.characters
        }
        for secret in seed.secrets.values():
            for character_id in secret.known_by:
                self._known_secret_ids[character_id].add(secret.id)
        self._relationships = {
            key: deepcopy(value) for key, value in seed.relationships.items()
        }

    @classmethod
    def from_events(cls, events: tuple[EventLogEntry, ...]) -> "ProjectionStore":
        if not events or events[0].event_type != "run_initialized":
            raise ValueError("event log must start with run_initialized")
        initial_state = events[0].sealed_payload.get("initial_state")
        if not initial_state:
            raise ValueError("run_initialized event is missing sealed initial_state")
        from .models import world_seed_from_snapshot

        store = cls(world_seed_from_snapshot(initial_state))
        for event in events:
            store.apply(event)
        return store

    def apply(self, event: EventLogEntry) -> None:
        self.tick = max(self.tick, event.tick)
        if event.tier in {EventTier.CANON, EventTier.SUPPORTING_OBSERVATION}:
            self._apply_memory(event)
        if event.tier == EventTier.CANON:
            self._apply_relationship_effects(event)
            self._apply_secret_visibility(event)

    def memory_view_for(self, character_id: str, public_scene: str) -> CharacterMemoryView:
        character = self.seed.characters[character_id]
        known_secret_ids = tuple(sorted(self._known_secret_ids[character_id]))
        known_truths = tuple(
            self.seed.secrets[secret_id].truth for secret_id in known_secret_ids
        )
        relationship_state: dict[str, dict[str, int | str | list[str]]] = {}
        for (from_id, to_id), state in self._relationships.items():
            if from_id == character_id:
                relationship_state[to_id] = {
                    "trust": state.trust,
                    "tension": state.tension,
                    "reason": state.reason,
                    "source_event_ids": list(state.source_event_ids),
                }
        return CharacterMemoryView(
            run_id=self.seed.run_id,
            tick=self.tick,
            character_id=character_id,
            character_name=character.name,
            role=character.role,
            public_description=character.public_description,
            personality_traits=character.personality_traits,
            short_term_goal=character.short_term_goal,
            long_term_goal=character.long_term_goal,
            location=self.seed.location,
            public_scene=public_scene,
            visible_recent_events=tuple(self._memories[character_id][-6:]),
            known_secret_ids=known_secret_ids,
            known_secret_truths=known_truths,
            relationship_state=relationship_state,
        )

    def relationship(self, from_id: str, to_id: str) -> RelationshipState:
        return self._relationships[(from_id, to_id)]

    def known_secret_ids(self, character_id: str) -> set[str]:
        return set(self._known_secret_ids[character_id])

    def _apply_memory(self, event: EventLogEntry) -> None:
        for character_id in event.visible_to:
            if character_id not in self._memories:
                continue
            self._memories[character_id].append(
                MemoryRecord(
                    event_id=event.event_id,
                    tick=event.tick,
                    summary=event.summary,
                    salience=int(event.payload.get("salience", 5)),
                )
            )

    def _apply_relationship_effects(self, event: EventLogEntry) -> None:
        for effect in event.payload.get("relationship_deltas", []):
            key = (effect["from"], effect["to"])
            state = self._relationships[key]
            state.trust += int(effect.get("trust", 0))
            state.tension += int(effect.get("tension", 0))
            state.reason = effect.get("reason", state.reason)
            state.source_event_ids.append(event.event_id)

    def _apply_secret_visibility(self, event: EventLogEntry) -> None:
        for reveal in event.payload.get("secret_reveals", []):
            secret_id = reveal["secret_id"]
            for character_id in reveal["to"]:
                self._known_secret_ids[character_id].add(secret_id)
