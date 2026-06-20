# Exec Plan

## Goal

Run a real OpenCode-backed character worker smoke using the free
`opencode/deepseek-v4-flash-free` model, while preserving the US-001 runtime
boundary and fail-closed behavior.

## Scope

In scope:

- Register/check OpenCode as Harness `agent-runtime`.
- Add project-local OpenCode agent `story-character-intent`.
- Improve OpenCode worker parsing and error classification.
- Add smoke CLI/report.
- Add unit tests for parser, command construction, error event handling, and
  missing command behavior.
- Run a real OpenCode smoke with DeepSeek free and record evidence.

Out of scope:

- Continuous LLM simulation loop.
- Provider credential setup.
- Full quality evaluation of DeepSeek prose/intent reasoning.
- UI or backend API.

## Risk Classification

Risk flags:

- External systems: OpenCode/provider runtime.
- Weak proof: live model availability depends on local/provider state.
- Public contracts: `opencode_smoke` command/report shape.

Hard gates:

- External provider behavior.

Lane:

```text
high-risk
```

## Work Phases

1. Discover local OpenCode model/provider state.
2. Add OpenCode-specific agent and smoke contract.
3. Implement parsing/error handling improvements.
4. Run unit tests.
5. Run live OpenCode smoke using `opencode/deepseek-v4-flash-free`.
6. Run Oracle review.
7. Update Harness matrix/story/trace.

## Stop Conditions

Pause for human confirmation if:

- The requested free model is not visible in `opencode models`.
- A provider setup would require credentials or secrets.
- The only way forward requires weakening US-001 secret/authority rules.
