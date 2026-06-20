# US-001 Environment-Mediated Multi-Agent Runtime POC

## Status

implemented

## Lane

normal

## Product Contract

Build the smallest executable story-world runtime that proves character agents
interact through a central environment instead of direct peer-to-peer chat.

The runtime must preserve private knowledge boundaries, commit all important
state changes as structured events, and produce a grounded story projection from
the event log.

## Relevant Product Docs

- `docs/product/story-world-runtime.md`
- `PROJECT_NOTES.md`

## Acceptance Criteria

- A deterministic demo run simulates 3 characters for 10 ticks.
- Character workers return structured `CharacterIntent` objects only.
- The GM/Resolver is the only code path that appends canonical runtime events.
- The event log is written as JSONL.
- The run can rebuild projections from the persisted event log.
- Linh and Minh cannot retrieve Khai's unrevealed secret.
- Public event summaries/payloads do not expose unrevealed secret ids or truths.
- GMResolver sanitizes adversarial worker attempts to smuggle secrets in intent
  fields.
- Relationship deltas are tied to source event ids.
- Story output is generated from committed events and contains support event ids.
- The OpenCode integration point exists as a worker adapter but is not required
  for deterministic tests.

## Design Notes

- Commands: `python -m story_world --ticks 10 --out runs/us001-demo`
- Queries: none yet.
- API: none yet.
- Tables: none yet.
- Domain rules:
  - `RunInitialized` is a `system_event`.
  - `RunInitialized.sealed_payload.initial_state` carries replayable initial
    state.
  - `visible_to` applies to public event `summary` and `payload`, not sealed
    system payload.
  - `canon_event` changes world/memory/relationship projections.
  - `supporting_observation` can enter scoped memory but cannot change global
    canon by itself.
  - `texture_note` is not used in this POC.
  - Secret visibility is enforced by `CharacterMemoryView`.
- UI surfaces: none yet.

## Validation

When updating durable proof status, use numeric booleans:
`scripts/bin/harness-cli story update --id US-001 --unit 1 --integration 1 --e2e 0 --platform 0`.

| Layer | Expected proof |
| --- | --- |
| Unit | `python -m unittest discover -s tests` |
| Integration | `python -m story_world --ticks 10 --out runs/us001-demo` |
| E2E | Not applicable; no UI yet. |
| Platform | Not applicable; no deployment/runtime shell yet. |
| Release | Not applicable. |

## Harness Delta

This is the first product story packet for the repo. It establishes a concrete
runtime verification command in the Harness durable matrix.

## Evidence

- `python -m unittest discover -s tests`
  - Result: pass, 12 tests.
- `python -m story_world --ticks 10 --out runs/us001-demo`
  - Result: pass.
  - Generated 20 events in `runs/us001-demo/events.jsonl`.
  - Generated grounded chapter in `runs/us001-demo/chapter_1.txt`.
  - Generated eval report in `runs/us001-demo/eval_report.json`.
  - Eval report passed:
    - `character_cannot_retrieve_unrevealed_secret`;
    - `visible_event_payloads_do_not_leak_unrevealed_secrets`;
    - `relationship_delta_requires_source_event`;
    - `supporting_observation_cannot_update_projection`;
    - `narrator_output_has_support_event_ids`;
    - `narrator_cannot_render_secret_without_supporting_event`;
    - `eventlog_starts_with_run_initialized`;
    - `canon_events_have_visibility_scope`.
- Oracle review:
  - First pass found 3 blockers around replay source-of-truth, public secret id
    leakage, and raw intent smuggling.
  - Follow-up found one remaining sanitizer gap for `intent_type`/`target_id`.
  - Final focused follow-up returned `APPROVE` after all public intent string
    fields were redacted and worker identity mismatch was rejected.
