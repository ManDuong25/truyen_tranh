# Overview

## Current Behavior

US-001 proved the story-world runtime with a deterministic scripted worker.
OpenCode existed only as an adapter boundary and had not successfully executed a
character intent task.

## Target Behavior

The project can invoke a real OpenCode model-backed character worker through a
scoped prompt, parse the resulting `CharacterIntent`, and fail closed when the
provider is unavailable or malformed output is returned.

The default smoke path uses the free OpenCode model:

```text
opencode/deepseek-v4-flash-free
```

## Status

implemented.

## Affected Users

- Developer/operator validating local agent runtime availability.
- Future story-world engine runtime calling LLM-backed character workers.

## Affected Product Docs

- `docs/product/story-world-runtime.md`

## Non-Goals

- No background multi-agent LLM run yet.
- No provider credential setup.
- No FastAPI/UI integration.
- No commitment that free model output quality is production-grade.
