# Validation

## Proof Strategy

Unit tests prove the adapter fails closed and parses OpenCode JSON event output.
The live smoke proves local OpenCode can at least execute the configured free
model and produce a parseable `CharacterIntent`.

If local/provider state blocks the live smoke, the story may remain partial with
explicit `unavailable` evidence rather than claiming a real LLM run succeeded.

## Test Plan

| Layer | Cases |
| --- | --- |
| Unit | Parse direct intent JSON, parse intent embedded in OpenCode text event, classify OpenCode error event, construct `opencode run --format json`, classify missing command. |
| Integration | `python -m story_world.opencode_smoke --out runs/us002-opencode-smoke-deepseek-free` using `opencode/deepseek-v4-flash-free`. |
| E2E | Not applicable; no UI. |
| Platform | Windows PATH/PATHEXT command resolution for `opencode`. |
| Performance | Smoke should finish within bounded command timeout. |
| Logs/Audit | Harness trace and smoke report. |

## Fixtures

- Scenario: `build_bridge_scenario()`.
- Character: `linh`.
- Model: `opencode/deepseek-v4-flash-free`.
- Agent: `.opencode/agents/story-character-intent.md`.

## Commands

```powershell
python -m unittest discover -s tests
python -m story_world.opencode_smoke --out runs/us002-opencode-smoke-deepseek-free
.\scripts\bin\harness-cli.exe story verify US-002
```

## Acceptance Evidence

- `python -m unittest discover -s tests`
  - Result: pass, 21 tests.
- `python -m story_world.opencode_smoke --out runs/us002-opencode-smoke-deepseek-free`
  - Result: pass.
  - Model: `opencode/deepseek-v4-flash-free`.
  - Agent: `story-character-intent`.
  - Report: `runs/us002-opencode-smoke-deepseek-free/opencode_smoke_report.json`.
- OpenCode-backed one-tick runtime smoke:
  - Result: pass.
  - Generated 2 events in `runs/us002-opencode-runtime-tick/events.jsonl`.
  - Generated 8/8 passing evals in `runs/us002-opencode-runtime-tick/eval_report.json`.
- Oracle review:
  - First pass found two blockers: timeout escaping the smoke report and
    malformed `metadata` escaping typed parse failure.
  - Both were fixed with regression tests.
  - Follow-up returned `APPROVE`.
- Known limitation:
  - DeepSeek free generated valid but generic `explore/observe` intents in the
    runtime tick while the current resolver still emitted `dialogue_conflict`.
  - Recorded Harness backlog `#1` for intent quality and resolver alignment.
