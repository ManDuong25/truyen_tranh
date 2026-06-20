from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import StrEnum
from typing import Any


class EventTier(StrEnum):
    SYSTEM = "system_event"
    CANON = "canon_event"
    SUPPORTING_OBSERVATION = "supporting_observation"
    TEXTURE = "texture_note"


@dataclass(frozen=True)
class Secret:
    id: str
    truth: str
    known_by: tuple[str, ...]
    reveal_conditions: tuple[str, ...] = ()


@dataclass(frozen=True)
class Character:
    id: str
    name: str
    role: str
    public_description: str
    personality_traits: tuple[str, ...]
    short_term_goal: str
    long_term_goal: str
    starting_location: str
    private_secret_ids: tuple[str, ...] = ()


@dataclass
class RelationshipState:
    from_id: str
    to_id: str
    trust: int
    tension: int
    reason: str
    source_event_ids: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class WorldSeed:
    run_id: str
    world_name: str
    location: str
    premise: str
    characters: dict[str, Character]
    secrets: dict[str, Secret]
    relationships: dict[tuple[str, str], RelationshipState]


@dataclass(frozen=True)
class MemoryRecord:
    event_id: str
    tick: int
    summary: str
    salience: int


@dataclass(frozen=True)
class CharacterMemoryView:
    run_id: str
    tick: int
    character_id: str
    character_name: str
    role: str
    public_description: str
    personality_traits: tuple[str, ...]
    short_term_goal: str
    long_term_goal: str
    location: str
    public_scene: str
    visible_recent_events: tuple[MemoryRecord, ...]
    known_secret_ids: tuple[str, ...]
    known_secret_truths: tuple[str, ...]
    relationship_state: dict[str, dict[str, Any]]


@dataclass(frozen=True)
class CharacterIntent:
    character_id: str
    intent_type: str
    target_id: str | None
    surface_action: str
    spoken_line: str
    inner_motive: str
    desired_outcome: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class EventLogEntry:
    event_id: str
    sequence: int
    run_id: str
    tick: int
    tier: EventTier
    event_type: str
    actor_ids: tuple[str, ...]
    observer_ids: tuple[str, ...]
    visible_to: tuple[str, ...]
    summary: str
    payload: dict[str, Any] = field(default_factory=dict)
    sealed_payload: dict[str, Any] = field(default_factory=dict)

    def to_json_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["tier"] = self.tier.value
        return data

    @classmethod
    def from_json_dict(cls, data: dict[str, Any]) -> "EventLogEntry":
        return cls(
            event_id=data["event_id"],
            sequence=int(data["sequence"]),
            run_id=data["run_id"],
            tick=int(data["tick"]),
            tier=EventTier(data["tier"]),
            event_type=data["event_type"],
            actor_ids=tuple(data.get("actor_ids", ())),
            observer_ids=tuple(data.get("observer_ids", ())),
            visible_to=tuple(data.get("visible_to", ())),
            summary=data["summary"],
            payload=dict(data.get("payload", {})),
            sealed_payload=dict(data.get("sealed_payload", {})),
        )


@dataclass(frozen=True)
class StoryParagraph:
    text: str
    support_event_ids: tuple[str, ...]


@dataclass(frozen=True)
class StoryOutput:
    title: str
    paragraphs: tuple[StoryParagraph, ...]

    def to_json_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class EvalResult:
    name: str
    passed: bool
    details: str

    def to_json_dict(self) -> dict[str, Any]:
        return asdict(self)


def world_seed_to_snapshot(seed: WorldSeed) -> dict[str, Any]:
    return {
        "run_id": seed.run_id,
        "world_name": seed.world_name,
        "location": seed.location,
        "premise": seed.premise,
        "characters": {
            character_id: asdict(character)
            for character_id, character in seed.characters.items()
        },
        "secrets": {
            secret_id: asdict(secret) for secret_id, secret in seed.secrets.items()
        },
        "relationships": [
            asdict(relationship) for relationship in seed.relationships.values()
        ],
    }


def world_seed_from_snapshot(snapshot: dict[str, Any]) -> WorldSeed:
    characters = {
        character_id: Character(
            **{
                **data,
                "personality_traits": tuple(data.get("personality_traits", ())),
                "private_secret_ids": tuple(data.get("private_secret_ids", ())),
            }
        )
        for character_id, data in snapshot["characters"].items()
    }
    secrets = {
        secret_id: Secret(
            **{
                **data,
                "known_by": tuple(data.get("known_by", ())),
                "reveal_conditions": tuple(data.get("reveal_conditions", ())),
            }
        )
        for secret_id, data in snapshot["secrets"].items()
    }
    relationships = {}
    for data in snapshot["relationships"]:
        state = RelationshipState(
            from_id=data["from_id"],
            to_id=data["to_id"],
            trust=int(data["trust"]),
            tension=int(data["tension"]),
            reason=data["reason"],
            source_event_ids=list(data.get("source_event_ids", [])),
        )
        relationships[(state.from_id, state.to_id)] = state
    return WorldSeed(
        run_id=snapshot["run_id"],
        world_name=snapshot["world_name"],
        location=snapshot["location"],
        premise=snapshot["premise"],
        characters=characters,
        secrets=secrets,
        relationships=relationships,
    )
