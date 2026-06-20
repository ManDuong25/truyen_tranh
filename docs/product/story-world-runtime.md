# Story World Runtime

This product contract defines the first executable slice of the story-world
engine. It is intentionally smaller than the final product vision: its purpose
is to prove that multiple character agents interact through a shared world
environment without directly mutating canon or leaking private knowledge.

## Product Shape

The runtime is an environment-mediated simulation:

```text
WorldRuntime
  -> Scheduler
  -> PerceptionFilter
  -> CharacterWorker
  -> CharacterIntent
  -> GMResolver
  -> EventLog
  -> Projections
  -> StorySynthesizer
  -> EvalReport
```

OpenCode or any other model runner is a worker implementation behind the
`CharacterWorker` boundary. The world runtime remains the authority.

## Non-Negotiable Rules

- Character workers receive scoped character context, not global truth.
- Character workers return structured `CharacterIntent` data.
- Character workers cannot write events, update relationships, or mutate world
  state directly.
- `GMResolver` is the only component that can commit resolved runtime events.
- `EventLog` is the source of truth after a run starts.
- Replay-critical system truth may live in `sealed_payload`; `visible_to`
  applies to public event `summary` and `payload`, not sealed system data.
- Memory, relationship state, and story prose are projections from events.
- Private secrets must not appear in a character's memory view until a committed
  event makes them visible to that character.
- Private secret ids/truths must not appear in public event summaries or public
  payloads visible to unauthorized characters.
- Narration must be grounded in committed events and must expose support event
  ids for its claims.

## US-001 Scope

US-001 proves the runtime contract with a deterministic no-LLM scenario:

- one world and one location;
- three characters: Linh, Khai, and Minh;
- one private secret known only by Khai;
- ten simulation ticks;
- structured intents;
- GM-resolved events;
- JSONL event log;
- sealed initial-state snapshot for replay;
- per-character memory projection;
- relationship projection;
- adversarial intent sanitization;
- grounded chapter output;
- eval report.

The implementation includes an OpenCode-ready worker adapter, but US-001 tests
use a deterministic scripted worker so replay and leakage checks are stable.

## US-002 Scope

US-002 connects the OpenCode adapter to a real local OpenCode invocation:

- project-local `story-character-intent` OpenCode agent;
- free default model `opencode/deepseek-v4-flash-free`;
- explicit parsing of `opencode run --format json` event streams;
- fail-closed handling of OpenCode error events, missing command, provider
  unavailability, and malformed output;
- smoke command that writes a local report under `runs/`.

## Deferred

- Full LLM/OpenCode multi-tick simulation in the main test path.
- Graphiti/Zep memory backend.
- FastAPI backend.
- React inspection UI.
- Continuous background mode.
- Auto Story Composer.

These remain product goals, but US-001 only establishes the runtime boundary
that those layers must obey.
