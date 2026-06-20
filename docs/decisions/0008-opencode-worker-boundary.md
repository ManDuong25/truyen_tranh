# 0008 OpenCode Worker Boundary

Date: 2026-06-19

## Status

Accepted

## Context

The user wants OpenCode to run model-backed sub-agents/character agents for the
story-world engine. OpenCode can execute models and custom agents, but it must
not become the authority for world state, canon, memory, relationship updates,
or secret visibility.

## Decision

Use OpenCode as a `CharacterWorker` implementation behind the world runtime
boundary.

OpenCode character workers:

- receive scoped `CharacterMemoryView`;
- return structured `CharacterIntent`;
- run through project-local `story-character-intent` agent by default;
- use `opencode/deepseek-v4-flash-free` for the free smoke path;
- cannot commit events or mutate world state.

`WorldRuntime` and `GMResolver` remain authoritative. The resolver sanitizes all
public intent fields before committing events.

## Alternatives Considered

1. Let OpenCode agents talk to each other directly.
   - Rejected because it weakens secret visibility, replay, and traceability.
2. Use the built-in `build` agent for story characters.
   - Rejected as the default because it loads broad development context and can
     be slow or noisy for a narrow character-intent task.
3. Use provider-specific OpenAI/ProxyPal models first.
   - Rejected for the default smoke because local credentials/server state may
     block them; the free OpenCode DeepSeek model is the requested path.

## Consequences

Positive:

- The runtime can test OpenCode integration without surrendering world authority.
- Free-model smoke can run without adding project secrets.
- Provider failures become explicit `unavailable` reports.

Tradeoffs:

- Free model latency/quality is variable.
- Live smoke depends on OpenCode service availability.
- Later production use still needs stronger schema-constrained output and model
  quality evals.

## Follow-Up

- Add a full LLM-backed 1-2 tick run after this smoke passes reliably.
- Add structured-output retry/repair before trusting live model output in
  long-running simulations.
