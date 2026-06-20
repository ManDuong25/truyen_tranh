# Test Matrix

This file maps product behavior to proof.

No product behavior has been defined or implemented yet. Do not mark a row
implemented until tests or validation evidence exist.

## Status Values

| Status | Meaning |
| --- | --- |
| planned | Accepted as intended behavior, not implemented |
| in_progress | Actively being built |
| implemented | Implemented and proof exists |
| changed | Contract changed after earlier implementation |
| retired | No longer part of the product contract |

## Matrix

| Story | Contract | Unit | Integration | E2E | Platform | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| US-001 | Environment-mediated multi-agent runtime POC | yes | yes | n/a | n/a | implemented | `python -m unittest discover -s tests` passed 12 tests; `python -m story_world --ticks 10 --out runs/us001-demo` passed; Oracle final follow-up approved sanitizer fix |
| US-002 | OpenCode-backed character worker smoke | yes | yes | n/a | yes | implemented | `python -m unittest discover -s tests` passed 21 tests; `python -m story_world.opencode_smoke --out runs/us002-opencode-smoke-deepseek-free` passed with `opencode/deepseek-v4-flash-free`; one-tick OpenCode runtime smoke passed 8 evals; Oracle follow-up approved |

## Evidence Rules

- Unit proof covers pure domain and application rules.
- Integration proof covers backend enforcement, data integrity, provider
  behavior, jobs, or service contracts.
- E2E proof covers user-visible browser flows.
- Platform proof covers only shell, deployment, mobile, desktop, or runtime
  behavior that cannot be proven in lower layers.
- A story can be implemented without every proof column if the story packet
  explains why.
