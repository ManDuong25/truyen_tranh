from __future__ import annotations

from .models import EvalResult, EventLogEntry, StoryOutput, WorldSeed
from .projections import ProjectionStore


def evaluate_run(
    *,
    seed: WorldSeed,
    events: tuple[EventLogEntry, ...],
    projections: ProjectionStore,
    story: StoryOutput,
) -> tuple[EvalResult, ...]:
    results = [
        _secret_visibility(seed, projections),
        _visible_event_payloads_do_not_leak_unrevealed_secrets(seed, events),
        _relationship_deltas_have_source_events(projections),
        _supporting_observations_do_not_mutate_canon(events),
        _story_grounded(story, events),
        _story_does_not_render_unrevealed_secret(seed, story),
        _event_log_has_run_initialized(events),
        _canon_events_have_visibility(events),
    ]
    return tuple(results)


def _secret_visibility(seed: WorldSeed, projections: ProjectionStore) -> EvalResult:
    secret = seed.secrets["s_khai_black_lotus"]
    leaked_to = []
    for character_id in seed.characters:
        view = projections.memory_view_for(character_id, public_scene="")
        if character_id not in secret.known_by and secret.truth in view.known_secret_truths:
            leaked_to.append(character_id)
        joined_memories = "\n".join(record.summary for record in view.visible_recent_events)
        if character_id not in secret.known_by and secret.truth in joined_memories:
            leaked_to.append(character_id)
    return EvalResult(
        name="character_cannot_retrieve_unrevealed_secret",
        passed=not leaked_to,
        details=(
            "No unrevealed secret appeared in unauthorized memory views."
            if not leaked_to
            else f"Secret leaked to: {sorted(set(leaked_to))}"
        ),
    )


def _relationship_deltas_have_source_events(projections: ProjectionStore) -> EvalResult:
    missing = []
    for pair in [("linh", "khai"), ("khai", "linh")]:
        state = projections.relationship(*pair)
        if not state.source_event_ids:
            missing.append(f"{pair[0]}->{pair[1]}")
    return EvalResult(
        name="relationship_delta_requires_source_event",
        passed=not missing,
        details=(
            "Relationship projections cite source event ids."
            if not missing
            else f"Missing source events for {missing}"
        ),
    )


def _visible_event_payloads_do_not_leak_unrevealed_secrets(
    seed: WorldSeed, events: tuple[EventLogEntry, ...]
) -> EvalResult:
    leaks = []
    for event in events:
        public_text = f"{event.summary}\n{event.payload}"
        for secret in seed.secrets.values():
            unauthorized_viewers = set(event.visible_to).difference(secret.known_by)
            if unauthorized_viewers and (
                secret.id in public_text or secret.truth in public_text
            ):
                leaks.append(f"{event.event_id}:{secret.id}")
    return EvalResult(
        name="visible_event_payloads_do_not_leak_unrevealed_secrets",
        passed=not leaks,
        details=(
            "Visible summaries/payloads do not expose private secret ids or truths."
            if not leaks
            else f"Visible leaks: {leaks}"
        ),
    )


def _supporting_observations_do_not_mutate_canon(
    events: tuple[EventLogEntry, ...]
) -> EvalResult:
    offenders = [
        event.event_id
        for event in events
        if event.tier.value == "supporting_observation"
        and (
            "relationship_deltas" in event.payload
            or "secret_reveals" in event.payload
        )
    ]
    return EvalResult(
        name="supporting_observation_cannot_update_projection",
        passed=not offenders,
        details=(
            "Supporting observations do not contain canon mutation payloads."
            if not offenders
            else f"Supporting observations attempted mutation: {offenders}"
        ),
    )


def _story_grounded(story: StoryOutput, events: tuple[EventLogEntry, ...]) -> EvalResult:
    event_ids = {event.event_id for event in events}
    missing = [
        paragraph.support_event_ids
        for paragraph in story.paragraphs
        if not paragraph.support_event_ids
        or any(event_id not in event_ids for event_id in paragraph.support_event_ids)
    ]
    return EvalResult(
        name="narrator_output_has_support_event_ids",
        passed=not missing,
        details=(
            "Every paragraph has at least one valid support event id."
            if not missing
            else f"Ungrounded paragraphs: {missing}"
        ),
    )


def _story_does_not_render_unrevealed_secret(
    seed: WorldSeed, story: StoryOutput
) -> EvalResult:
    story_text = "\n".join(paragraph.text for paragraph in story.paragraphs)
    leaks = [
        secret.id
        for secret in seed.secrets.values()
        if secret.id in story_text or secret.truth in story_text
    ]
    return EvalResult(
        name="narrator_cannot_render_secret_without_supporting_event",
        passed=not leaks,
        details=(
            "Story text does not render unrevealed private secrets."
            if not leaks
            else f"Story leaked secrets: {leaks}"
        ),
    )


def _event_log_has_run_initialized(events: tuple[EventLogEntry, ...]) -> EvalResult:
    passed = bool(events) and events[0].event_type == "run_initialized"
    return EvalResult(
        name="eventlog_starts_with_run_initialized",
        passed=passed,
        details="First event initializes the run." if passed else "Missing run_initialized.",
    )


def _canon_events_have_visibility(events: tuple[EventLogEntry, ...]) -> EvalResult:
    missing = [
        event.event_id
        for event in events
        if event.tier.value == "canon_event" and not event.visible_to
    ]
    return EvalResult(
        name="canon_events_have_visibility_scope",
        passed=not missing,
        details=(
            "Canon events define visibility scope."
            if not missing
            else f"Missing visibility on {missing}"
        ),
    )
