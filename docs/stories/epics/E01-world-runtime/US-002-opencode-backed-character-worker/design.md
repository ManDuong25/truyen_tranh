# Design

## Domain Model

`OpenCodeCharacterWorker` remains behind the `CharacterWorker` protocol. It
receives a `CharacterMemoryView` and returns a `CharacterIntent`.

New supporting behavior:

- `OpenCodeExecutionError` classifies provider/auth/connectivity failures.
- OpenCode JSON event streams are parsed explicitly.
- OpenCode `type=error` events are treated as failures even when the process
  exits with status `0`.
- Project-local OpenCode agent `story-character-intent` returns one intent JSON
  object and denies tools.

## Application Flow

```text
ProjectionStore -> CharacterMemoryView
OpenCodeCharacterWorker.decide(view)
  -> opencode run --format json --agent story-character-intent --model opencode/deepseek-v4-flash-free
  -> parse JSON event stream
  -> return CharacterIntent or typed failure
GMResolver
  -> sanitizes public intent fields before commit
```

## Interface Contract

Smoke command:

```powershell
python -m story_world.opencode_smoke --out runs/us002-opencode-smoke-deepseek-free
```

Report:

```json
{
  "status": "passed | unavailable | failed",
  "agent": "story-character-intent",
  "model": "opencode/deepseek-v4-flash-free",
  "character_id": "linh"
}
```

`unavailable` means OpenCode ran but the provider/model was not available or
timed out. It is a fail-closed operational state, not a successful LLM run.

## Data Model

No database changes.

## UI / Platform Impact

Adds project-local OpenCode agent config under `.opencode/agents/`.

## Observability

Smoke reports are written under `runs/us002-*`, which is ignored as local run
artifact. Harness story evidence records whether live OpenCode passed or was
blocked.

## Alternatives Considered

1. Use the built-in `build` agent.
   - Rejected as default because it loads very large development context and
     can hang on a tiny story intent prompt.
2. Use ProxyPal/OpenAI provider models.
   - Rejected for this smoke because local ProxyPal was not listening and
     OpenAI API credentials were not configured.
