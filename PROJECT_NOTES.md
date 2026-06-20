# Project Notes

Date: 2026-06-16

This file records important discussion outcomes, decisions, and research notes for the `truyen_tranh` project so they do not exist only in chat history.

## Current Workspace Rule

- `C:\Users\mansh\Downloads\truyen_tranh` is the intended project root.
- `arena-library/` is only for cloning, running, and comparing external libraries before integration.
- Do not treat `arena-library/` repos as the actual product implementation.
- Root was reverted after an earlier temporary harness install attempt.
- On 2026-06-16, `repository-harness` was installed again as the actual project scaffold.
- Current expected root-level harness files include `AGENTS.md`, `README.md`, `.gitignore`, `docs/`, `scripts/`, `PROJECT_NOTES.md`, `arena-library/`, and prior research artifacts.

## Harness Direction

Current decision:

- Use `repository-harness` as the main project spine for specs, stories, decisions, validation, traces, and tool registry.
- Do not replace it wholesale with ECC.
- Use ECC selectively as a skill, hook, security, and operator-pattern library.

Reasoning:

- `repository-harness` has a focused repo-local durable layer: intake, stories, decisions, traces, tool registry, audit, and improvement proposals.
- ECC is broader and more powerful for agent skills and operator workflows, but too large and volatile to install wholesale as the core project framework.

## Harness Installation Record

Installed on 2026-06-16 from local checkout:

- Source: `arena-library/repository-harness`
- Target: project root `C:\Users\mansh\Downloads\truyen_tranh`
- Installed CLI: `scripts/bin/harness-cli.exe`
- CLI version: `harness-cli 0.1.10`
- Release source verified by installer: `harness-cli-v0.1.10`

Initial commands run:

```powershell
.\scripts\bin\harness-cli.exe init
.\scripts\bin\harness-cli.exe migrate
.\scripts\bin\harness-cli.exe import brownfield
```

Initial result:

- `harness.db` created.
- Schema applied to version 5.
- Brownfield import found 7 harness decisions.
- First intake recorded as `#1`: install repository-harness as project operating scaffold.

## ECC Findings

Inspected repo:

- GitHub: `https://github.com/affaan-m/ECC`
- Local clone: `arena-library/ECC`
- Latest inspected commit: `e25f2d4` on 2026-06-16
- Package: `ecc-universal@2.0.0`
- License: MIT

Useful ECC surfaces:

- selective installer and profiles
- 271 skills
- 67 agents
- 92 commands
- hook runtime for Claude/OpenCode/Cursor-like surfaces
- Codex metadata and plugin surface
- MCP connector policy
- AgentShield integration
- Hermes/OpenClaw migration guidance
- ECC2 Rust control-plane alpha

Important ECC caveats:

- Do not install the full ECC profile into this project by default.
- Codex plugin mode is documented by ECC as fragile.
- Codex hook parity is instruction-backed, not runtime-enforced.
- ECC2 is alpha and should not be treated as a finished control plane.
- `npm test` did not fully pass on the inspected checkout due stale command registry.
- `node tests/run-all.js` passed 2786/2788 with a Windows path expectation issue in OpenCode format-code tests.
- `npm audit` reported 3 moderate vulnerabilities in dev dependency chain.

Recommended ECC skills to cherry-pick later:

- `product-capability`
- `architecture-decision-records`
- `agent-harness-construction`
- `iterative-retrieval`
- `tdd-workflow`
- `verification-loop`
- `eval-harness`
- `search-first`
- `team-agent-orchestration`
- `recursive-decision-ledger`
- `security-scan`

## Story Engine Design Principle

Important principle from discussion:

```text
Hard core, soft surface.
```

Meaning:

- Hard core: canonical facts, event log, knowledge visibility, secrets, memory provenance, relationship causes, resolver authority, narrator grounding.
- Soft surface: dialogue, hesitation, body language, mood, micro-actions, ambiguity, expressive prose.

ADR candidate:

```text
Only canon-affecting facts become structured events.
Atmosphere, prose texture, hesitation, and minor expressive behavior remain narrator-level soft detail unless they change knowledge, relationship, location, goal, or world state.
```

## Next Build Direction

Completed:

- `repository-harness` is installed in the project root.

Next real step:

```text
Create the durable product contract and ADR set for the Story World Engine.
```

Target formal artifacts:

- `docs/product/story-world-engine.md`
- ADR for hard core / soft surface
- ADR for source-of-truth hierarchy
- ADR for graph memory boundary
- ADR for secret visibility
- ADR for event tier permissions
- ADR for pattern-library quarantine
- MVP-A deterministic contract demo story/spec
- MVP-B Graphiti-backed memory demo story/spec

Keep:

- Register useful external tools/skills through the harness tool registry instead of making every tool mandatory.
- Keep `arena-library/` for reproducible research and dependency comparison.

## Working Process Decision

After harness installation, the first real project step is not coding.

First step:

```text
Turn the research brief and discussion into a durable product contract.
```

This means:

- record a `new_spec` intake for the Multi-Agent Story World Engine;
- create `docs/product/story-world-engine.md` or equivalent product contract;
- capture the core design principle as a project ADR;
- only then split work into epics/stories and implementation tasks.

Reason:

- The project has many moving parts: event log, world state, per-character memory, private knowledge, agent orchestration, narrator grounding, evaluation, and UI inspection.
- Coding before a product contract would make later architecture decisions drift.
- Harness should make future agents inherit the product intent instead of relying on chat history.

Recommended lane for the first product-contract step: `high-risk`, because it defines architecture, source-of-truth hierarchy, memory boundaries, and external-agent behavior.

## Product Direction: Auto Story Composer Powered By Simulation Lab

Decision from user discussion:

The first product should not be a pure Authoring Studio where users must manually enter complete `WorldConfig`, `CharacterConfig`, `SecretConfig`, and `SceneConfig`.

The first product should be:

```text
Short Context -> Auto Story Setup -> Simulation Lab -> Narrated Story
```

External UX:

- User enters a short context prompt.
- User clicks `Generate Story Seed`.
- System expands the prompt into a structured story setup.
- User clicks `Run Simulation`.
- User reads Chapter 1.
- User can use `Inspect Why` to see why the story unfolded that way.

Example input:

```text
Một thiếu niên bị gia tộc ruồng bỏ, vô tình gặp một linh hồn cổ xưa trong chiếc nhẫn. Thế giới tu luyện, có gia tộc, tông môn, luyện đan, đấu kỹ, bí cảnh.
```

The system should auto-expand this into:

- story premise
- minimal world bible
- main characters
- factions
- secrets
- relationship seeds
- first scene setup
- conflict pressure
- simulation run
- readable chapter prose

Internal constraints remain strict:

- Generated Story Bible is only initialization input.
- EventLog remains the source of truth.
- Character agents produce structured intents, not final prose.
- GM/Resolver turns intents into `ResolvedEvent` records.
- Projections update memory, relationship, and secret visibility.
- Narrator writes prose from `ResolvedEvent` records.
- Director/Critic checks pacing, continuity, secret leakage, and narrator hallucination.
- Trace must explain what each character knew, remembered, why they acted, and which events support each prose passage.

Pattern library direction:

- User-provided story corpus is not used to copy prose.
- It is used to derive reusable patterns:
  - scene patterns
  - conflict patterns
  - worldbuilding patterns
  - trope library
  - pacing guide
  - chapter opening/ending patterns
  - cliffhanger patterns
  - character archetype patterns

MVP runtime direction:

- deterministic no-LLM/stub path first;
- LLM agents attached later;
- one scenario generated from short context;
- 3-5 characters;
- 1-2 secrets;
- 10 ticks;
- event log;
- relationship/memory projection;
- grounded narrator;
- eval report.

Core reason:

```text
The user should input little and the system should generate much,
but the generated material must become explicit data models before simulation runs.
```

## Product Direction Update: Persistent Living World Simulation

Decision from user clarification on 2026-06-19:

```text
The product is not only a 10-tick chapter generator.
The product should create a living story world that can keep running,
with story output synthesized later from the world's event history.
```

Meaning:

- The user provides an initial freeform context or premise.
- Auto Story Setup expands that premise into a structured world seed.
- The system initializes a simulated world with agents, locations, factions, goals, secrets, resources, rules, and memory.
- Character agents continue interacting with each other and the world over simulated time.
- The world can be left running for a configured duration, tick budget, event budget, or until stopped.
- The engine records what happens as structured events, observations, projection updates, and traces.
- A dedicated Story Synthesizer / Narrative Compiler agent later reads selected event windows/arcs and turns them into readable prose and optional storyboard beats.

Reframed core product loop:

```text
Freeform context
-> Auto Story Setup
-> Validated GeneratedStorySeed
-> RunInitialized
-> Persistent Living World Simulation
-> Continuous EventLog / projections / memory graph
-> Story Synthesizer selects event arcs
-> Grounded chapter prose + optional storyboard beats
-> Inspect Why / timeline / memory / knowledge / relationship trace
```

Important distinction:

- Simulation creates world truth.
- Story synthesis narrates selected truth.
- Narration is downstream from simulation, not the thing driving every tick.

Impact on prior MVP language:

- The earlier 10-tick scenario remains useful as a deterministic acceptance slice.
- It is not the full product concept.
- MVP-A/MVP-B should prove the runtime contract with bounded ticks, but the architecture must support longer-running persistent worlds.

Living-world requirements:

- world state persists across many simulation cycles;
- agents have ongoing goals, plans, emotions, relationships, beliefs, resources, and private knowledge;
- not all agents run at full LLM depth every cycle;
- scheduler supports active, nearby, background, and dormant agents;
- background world changes can occur through rules, faction movement, environmental pressure, and summarized offscreen simulation;
- story output can be requested for:
  - latest event window;
  - selected character arc;
  - selected location;
  - selected conflict;
  - chapter-sized slice;
  - timeline summary;
  - storyboard beats.

Story Synthesizer / Narrative Compiler role:

- reads committed EventLog windows and projections;
- selects salient events using conflict, emotion, relationship change, secret movement, and pacing signals;
- groups events into scenes/arcs/chapters;
- writes readable prose in the chosen language/style;
- may produce storyboard beats as sibling projection from the same selected event window;
- must link major claims back to event ids;
- must not invent unsupported major facts.

Design consequence:

```text
The engine should be optimized for durable simulation first,
and narrative output second.
```

However, the user-facing UX should remain simple:

```text
User enters a short or long premise
-> system builds and starts a living world
-> user can inspect or wait
-> user asks for story/chapter/summary when desired
```

## Auto Story Setup Expansion Policy

Default expansion mode:

```text
Genre-Rich Controlled Expansion
```

Meaning:

- The system should expand a short user context strongly enough to create genre flavor, conflict, secrets, factions, pressure, and hooks.
- It should not default to minimal expansion, because that would make the story bland.
- It should not default to full Bold Director mode, because that risks drifting away from the user's intended premise.

Core premise preservation rules:

- Preserve the core premise supplied by the user.
- Do not change the protagonist's role if the user stated it clearly.
- Do not change the main genre or tone.
- Do not add twists that reverse the meaning of the prompt.

Allowed generated additions:

- minimal worldbuilding;
- cultivation/power-level system when the genre needs it;
- 3-5 main/supporting characters;
- 1-3 factions;
- 1-2 secrets;
- conflict pressure;
- opening scene hook;
- genre-appropriate archetypes/tropes;
- first chapter direction.

Every generated element should carry provenance:

- `user_provided`
- `inferred_from_prompt`
- `genre_pattern`
- `director_added`

Bold twist rule:

- Major twists should not be committed directly into canon.
- Bold twists should begin as `director_candidate`.
- A bold twist becomes canon only when selected by the user or introduced through a valid GM/Resolver `ResolvedEvent`.

Corpus/pattern-library boundary:

- Story corpora are used only to derive reusable patterns:
  - scene patterns
  - conflict patterns
  - pacing patterns
  - trope patterns
  - worldbuilding patterns
- Do not copy proper names, exact prose, unique plot specifics, or original passages.

Auto Story Setup output should include:

- expanded premise
- minimal story bible
- character sheets
- factions
- secrets
- relationship seeds
- opening scene
- default run config suggestions
- generated assumptions for user inspection

After Auto Story Setup, the runtime must still pass through Simulation Lab:

- EventLog is the source of truth.
- CharacterIntent is structured.
- GM/Resolver creates ResolvedEvent.
- memory, relationship, and secret visibility are projections.
- Narrator writes only from supported events.
- trace/eval must remain inspectable.

Future option:

- Add an advanced toggle: `Allow bold twists`.

## Genre Architecture Decision: Hybrid Core + Default Pattern Pack

Decision from user discussion:

```text
Build a genre-agnostic StoryWorldCore,
but ship MVP with an opinionated cultivation_fantasy pattern pack
as the default product experience.
```

Reasoning:

- A pure cultivation-specific core would make the MVP flavorful quickly but risks locking the engine into one genre.
- A pure genre-agnostic MVP would keep architecture clean but likely be bland and over-abstract before there is a good demo.
- Hybrid keeps the core clean while giving the first product a strong genre identity.

Core schema must not hard-code cultivation fantasy concepts.

Core concepts:

- `World`
- `Location`
- `Character`
- `Faction`
- `Goal`
- `Secret`
- `Relationship`
- `Memory`
- `Rule`
- `Resource`
- `Ability`
- `Intent`
- `ResolvedEvent`
- `EventLog`
- `Projection`
- `StoryOutput`
- `Trace`
- `Eval`

Default MVP pattern pack:

```text
cultivation_fantasy
```

This pattern pack may define:

- cultivation realms / cảnh giới
- sects / tông môn
- clans / gia tộc
- techniques / công pháp / đấu kỹ
- pills / luyện đan
- artifacts / pháp bảo
- secret realms / bí cảnh
- beasts / ma thú
- auctions / đấu giá
- broken engagement / humiliation / lucky encounter / mysterious teacher
- tournament / sect selection / clan conflict
- power progression pressure

Auto Story Setup uses the pattern pack to expand short context.

Example:

```text
Thiếu niên bị gia tộc ruồng bỏ, gặp linh hồn cổ trong nhẫn.
```

The default pack may generate:

- power realm system
- rival clan
- major sect
- secret about the ring
- spirit mentor
- humiliation or broken engagement pressure
- opening scene hook

Pattern pack constraints:

- It must preserve the user's core premise.
- It can add genre-appropriate tropes.
- It must not change the meaning of the prompt.
- It must not bypass the core simulation architecture.

Genre-specific data must live in extension fields or pack metadata, for example:

- `character.extensions.cultivation.realm`
- `faction.extensions.cultivation.sect_rank`
- `ability.extensions.cultivation.technique_grade`
- `item.extensions.cultivation.artifact_grade`

Simulation runtime remains generic:

- `CharacterIntent`
- `GMResolver`
- `ResolvedEvent`
- `EventLog`
- `Projection`
- `Narrator`
- `Validator`

MVP defaults:

- `genre = cultivation_fantasy`
- `expansion_mode = genre_rich_controlled`
- 3-5 characters
- 1-2 factions
- 1-2 secrets
- 10 ticks
- first readable chapter
- Inspect Why / Event Log / Character Knowledge / Relationship panel

## Auto Story Setup Review Gate

Decision:

```text
Use a hybrid review gate.
```

Meaning:

- After `Generate Story Seed`, the system shows the generated structured setup.
- The user can run simulation immediately by default.
- The user is not forced to approve or edit every generated field.
- A visible `Generated Assumptions` panel lets the user inspect, edit, lock, or reject generated elements.
- Major `director_candidate` twists require explicit approval before becoming canon.

Reasoning:

- A required review gate would slow down the product and make it feel like a manual Authoring Studio.
- Fully auto-running without visible assumptions would hide too much and make surprising generation hard to trust.
- Hybrid keeps the product fast while preserving control and traceability.

Default behavior:

- `user_provided` elements are locked by default unless the user edits the original prompt or explicitly unlocks them.
- `inferred_from_prompt`, `genre_pattern`, and `director_added` elements are editable.
- `director_candidate` elements are visible but non-canon until approved or later introduced by a valid GM/Resolver event.

## Generated Story Seed Contract: Layered Seed

Decision from user discussion:

```text
Layered Seed = Required Core for runtime
             + Optional Layers for richness, inspection, and future editing.
```

Generated Story Seed has two layers:

1. `required_core`
   - The minimal contract required for simulation to run.
   - Runtime may depend on this layer.
   - If this layer is invalid or missing required fields, simulation should not start.

2. `optional_layers`
   - Enrichment for UI inspection, narrator/director quality, genre flavor, and future editing.
   - Simulation must not crash if this layer is missing.
   - Optional layers should degrade cleanly.

Reasoning:

- A compact seed is easy for MVP but too shallow for story depth.
- A full mini bible is rich but too heavy and risks MVP bloat.
- A layered seed keeps the MVP runnable while enabling inspectability and later Authoring Studio features.

Desired top-level shape:

```yaml
generated_story_seed:
  meta:
    seed_id:
    source_prompt:
    genre:
    pattern_pack: cultivation_fantasy
    expansion_mode: genre_rich_controlled
    created_at:
    provenance_policy:
      - user_provided
      - inferred_from_prompt
      - genre_pattern
      - director_added

  required_core:
    premise:
      logline:
      central_conflict:
      protagonist_desire:
      opening_hook:

    world:
      world_name:
      current_era:
      starting_location:
      minimal_rules:
        - id:
          rule:
          reason:

    locations:
      - id:
        name:
        type:
        description:
        parent_location_id:
        connected_location_ids:
        visibility:
        constraints:
        starting_present_character_ids:
        provenance:

    characters:
      - id:
        name:
        role:
        archetype:
        starting_location:
        public_description:
        personality_traits:
        short_term_goal:
        long_term_goal:
        seed_fact_refs:
        private_seed_fact_refs:
        starting_emotional_state:

    seed_facts:
      - id:
        category: canonical_fact | character_belief | rumor | secret_truth | narrator_context
        text:
        visibility_scope:
        known_by:
        hidden_from:
        source:
        confidence:
        lock_status:
        source_reason:

    factions:
      - id:
        name:
        role_in_conflict:
        public_goal:
        hidden_agenda:

    abilities:
      - id:
        owner_id:
        name:
        description:
        constraints:
        provenance:

    resources:
      - id:
        owner_id:
        name:
        quantity:
        constraints:
        provenance:

    items:
      - id:
        owner_id:
        name:
        description:
        constraints:
        provenance:

    constraints:
      - id:
        applies_to:
        rule:
        reason:
        provenance:

    secrets:
      - id:
        truth:
        known_by:
        unknown_by:
        reveal_conditions:
        danger_if_revealed:

    relationships:
      - from:
        to:
        trust:
        tension:
        reason:

    opening_scene:
      location:
      active_characters:
      nearby_characters:
      situation:
      pressure:
      expected_first_conflict:

  optional_layers:
    power_system:
      enabled: true
      realms:
      resources:
      abilities:
      artifacts:
      constraints:

    genre_patterns:
      selected_tropes:
      scene_patterns:
      conflict_patterns:
      pacing_patterns:
      forbidden_copy_patterns:

    tone_and_style:
      prose_style:
      dialogue_style:
      atmosphere:
      chapter_pacing:
      cliffhanger_style:

    assumption_ledger:
      - id:
        assumption:
        source:
        confidence:
        editable: true

    validation_expectations:
      secret_visibility:
      narrator_grounding:
      relationship_consistency:
      canon_constraints:
      replay_requirements:

    director_candidates:
      twists:
      future_conflicts:
      possible_reveals:
      escalation_paths:

default_run_config:
  run_mode: deterministic_acceptance | interactive | background | synthesis_only
  tick_budget: 10
  wall_clock_budget:
  event_budget:
  agent_scheduling_policy:
  stop_conditions:
  output_request_policy:
  eval_expectations:
    must_create_events:
      - conflict_escalation
      - private_knowledge_test
      - relationship_delta
    must_not_happen:
      - reveal_secret_without_event
      - narrator_invents_unsupported_fact
```

Runtime rules:

- `required_core` is the required simulation contract.
- `optional_layers` are enrichment only.
- `default_run_config` controls how a run executes; it is not part of world canon.
- A persistent world may run with different `RunConfig` values from the same validated seed.
- Simulation must not depend hard on optional layers.
- Every generated element should have provenance.
- `director_candidates` are not canon.
- A director candidate becomes canon only if selected or committed by a valid GM/Resolver `ResolvedEvent`.
- EventLog remains the source of truth.
- Narrator renders only from supported events.

UI rules:

- MVP UI should show `required_core` first.
- Optional layers can live in an `Inspect Generated Layers` tab.
- User can edit seed before simulation in later versions.
- First MVP may keep seed read-only as long as assumptions are inspectable.

## Seed Validation and Repair Policy

Decision from user discussion:

```text
Use Repair Preview for invalid, incomplete, contradictory, or low-confidence generated seeds.
```

Meaning:

- Before simulation starts, the system validates `generated_story_seed.required_core`.
- If the required core is complete and coherent, the user can run simulation immediately.
- If required data is missing, contradictory, or low-confidence, the system creates a repair preview instead of silently rewriting the seed or hard-blocking with no path forward.
- Safe repairs may be auto-applied when they do not change premise, protagonist role, core conflict, major secrets, or genre/tone.
- Premise-changing repairs require user approval.
- Major changes to secrets, main characters, factions, central conflict, or opening scene pressure require user approval.
- Repair suggestions must explain:
  - the detected issue;
  - the proposed change;
  - affected fields;
  - whether the change is safe auto-repair or approval-required;
  - provenance for any generated replacement.

Reasoning:

- A hard block would make the MVP feel brittle.
- Fully automatic repair could quietly drift away from the user's intent.
- Repair Preview preserves fast generation while keeping the user in control of meaningful story changes.

Runtime rule:

- Simulation may not start from an invalid `required_core`.
- Repair Preview is part of Auto Story Setup, not part of EventLog canon.
- A repair does not become story truth until the repaired seed is used to initialize a simulation run and later events are committed through GM/Resolver.

## Auto Story Setup Composer Policy

Decision from user discussion:

```text
Use Hybrid Parser + Pattern Pack + LLM-Assisted Composer.
```

Meaning:

- The user-facing input remains freeform: a short or long natural-language description.
- The user should not be forced to manually fill `WorldConfig`, `CharacterConfig`, `SecretConfig`, `SceneConfig`, or other setup forms before the first run.
- Internally, the system converts that freeform prompt into a structured `GeneratedStorySeed` before simulation.
- The composer has three cooperating parts:
  - prompt parser: preserves explicit user-provided facts and constraints;
  - pattern pack: adds genre-appropriate material, with `cultivation_fantasy` as the MVP default;
  - LLM-assisted composer: expands the seed creatively while obeying schema, provenance, and validation rules.
- MVP should also keep a deterministic stub composer for tests and reproducible demos.
- Both deterministic composer and LLM-assisted composer must return the same `GeneratedStorySeed` schema.

User experience rule:

- Primary UX is still:

```text
User enters a freeform story idea
-> Generate Story Seed
-> optional inspect/edit
-> Run Simulation
-> Read Chapter
-> Inspect Why
```

- `Generated Assumptions`, `Repair Preview`, and optional generated layers exist to inspect and correct system decisions, not to make the user do manual setup work.
- The system should ask for user approval only when a generated repair or twist changes a major premise, secret, protagonist role, core conflict, faction pressure, or genre/tone.

Reasoning:

- Pure templates are too rigid.
- Pure LLM generation is too opaque and difficult to validate.
- Hybrid composition keeps the product fast for users while preserving explicit data models, provenance, reproducibility, and later simulation traceability.

## Story Output Policy

Decision from user discussion:

```text
Use Hybrid output: default chapter prose plus optional storyboard beats.
```

Meaning:

- MVP primary readable output is a coherent web-novel-style chapter generated from resolved simulation events.
- MVP also produces optional storyboard beats as a structured projection from the same resolved events.
- The storyboard beats are not a separate canon source and must not invent events unsupported by EventLog.
- The default reader experience should not require viewing storyboard data.
- Storyboard beats exist to support later comic/truyen-tranh rendering, panel planning, visual generation, and scene inspection.

Output hierarchy:

```text
selected EventLog window
  -> chapter prose
  -> optional storyboard beats
  -> trace links for both outputs back to supporting events
```

Lineage rule:

- Chapter prose and storyboard beats are sibling projections from the committed EventLog window.
- Storyboard beats must not be generated from prose as their source of truth.
- Prose hallucinations must not leak into storyboard/panel planning.

Chapter prose should include:

- readable scene narration;
- grounded dialogue;
- emotional texture;
- pacing and cliffhanger;
- no unsupported major facts.

Storyboard beats should include:

- beat id;
- supported event ids;
- location;
- characters visible in the beat;
- panel/action summary;
- dialogue/caption candidates;
- emotional focus;
- visual notes;
- continuity constraints.

Reasoning:

- Pure prose proves the event-log-to-narrative pipeline fastest.
- Pure comic storyboard would force visual/panel concerns too early.
- Hybrid preserves the project direction toward `truyen_tranh` while keeping MVP focused on simulation-grounded narrative.

## Language and Voice Policy

Decision from user discussion:

```text
Use Vietnamese-first output with adaptive override.
```

Meaning:

- If the user does not specify an output language, MVP defaults to Vietnamese.
- The default Vietnamese voice should fit web-novel cultivation / huyền huyễn / tiên hiệp expectations without hard-coding the core engine to one language.
- If the user prompt clearly requests another language, or a future UI language selector is set, the system should follow that requested output language.
- Language choice applies to:
  - generated story seed summaries shown to the user;
  - chapter prose;
  - storyboard beats;
  - narrator/director explanations in Inspect Why.
- Internal IDs, schemas, event types, and trace fields should remain stable machine-friendly identifiers, preferably English snake_case, regardless of output language.

Reasoning:

- The current product direction is Vietnamese-first and cultivation-fantasy-heavy.
- The core engine should remain reusable across genres and languages.
- Separating internal schema language from user-facing narrative language keeps validation, tests, and trace queries stable.

## Director and Character Autonomy Policy

Decision from user discussion:

```text
Use Director-bounded character autonomy.
```

Meaning:

- Director does not script exact character actions tick-by-tick.
- Director provides scene pressure, pacing targets, canon constraints, escalation suggestions, and quality feedback.
- Character agents still choose their own structured intents from their goals, memories, relationships, emotions, secrets, and current perception.
- GM/Resolver is the only layer that turns intents into committed `ResolvedEvent` records.
- Director suggestions are not canon until GM/Resolver commits an event.

Responsibility split:

```text
Director:
  sets narrative pressure, pacing, tension, soft goals, constraints

Character agent:
  chooses structured intent based only on visible knowledge and memory

GM/Resolver:
  validates feasibility, resolves conflict, applies consequences, commits events

Narrator:
  renders selected committed event windows into prose/storyboard beats downstream from simulation

Critic/Lore Keeper:
  checks continuity, canon, secret leakage, unsupported narration, repetition
```

Anti-patterns to avoid:

- Director forcing exact dialogue or exact outcomes every tick.
- Character agents seeing global plot plans or secrets they should not know.
- Narrator inventing events because Director wanted a beat.
- Simulation becoming a group chat with no resolver authority.

Reasoning:

- Pure character autonomy risks drifting into random conversation.
- Pure Director-led plot beats make characters feel mechanical.
- Director-bounded autonomy preserves character agency while keeping the story coherent, paced, and inspectable.

## Simulation Tick Policy

Decision from user discussion:

```text
Use phased simulation ticks.
```

Meaning:

- A simulation tick is not a loose chat turn.
- Each tick runs through explicit phases so agent actions can be parallelized while state updates remain deterministic and traceable.
- Character agents may generate intents in parallel, but they all receive perception from the same pre-resolution snapshot for that tick.
- GM/Resolver resolves all submitted intents together, handles conflicts, and commits structured `ResolvedEvent` records.
- Projections update only after events are committed.

Default tick pipeline:

```text
1. Scheduler selects tick type:
   - active_scene_tick
   - background_world_tick
   - faction_pressure_tick
   - dormant_update_tick
   - synthesis_only_run
2. Director pressure / scene objective, only when useful for active scene ticks
3. World snapshot freeze
4. Perception filter per active/nearby character
5. Character memory retrieval per character
6. CharacterIntent generation, parallel where possible
7. GM/Resolver conflict resolution
8. ResolvedEvent append to EventLog
9. Projection updates:
   - character state
   - memories
   - relationships
   - secret visibility / knowledge
   - world state
10. Optional per-tick debug summary / trace note
11. Critic/Lore Keeper validation
12. Trace persistence
```

Story synthesis rule:

- Story Synthesizer runs after a selected EventLog window/arc is chosen.
- It does not run as a mandatory phase of every simulation tick.

MVP rule:

- Use active characters only for full reasoning.
- Nearby characters may observe and receive memory updates if perception rules allow.
- Background/dormant character scheduling can be added later.
- The bounded MVP should make every tick inspectable: inputs, perceptions, retrieved memories, intents, resolver decision, events, projection deltas, debug summaries/synthesis candidates, and validation findings.

Reasoning:

- Pure sequential turns are easier to debug but less natural for scenes where several characters react to the same moment.
- Fully simultaneous intents are natural but can become hard to inspect without phase boundaries.
- Phased ticks allow parallel character agents while preserving deterministic-ish orchestration, conflict resolution, and traceability.

## Living World Scheduler Policy

Decision:

```text
Persistent worlds require tiered agent scheduling.
```

Agent execution tiers:

- active agents:
  - currently in the scene/conflict;
  - receive full perception, memory retrieval, and CharacterIntent generation.
- nearby agents:
  - can observe or react lightly;
  - may receive supporting observations and limited intent opportunities.
- background agents:
  - simulated through rules, goals, faction pressure, summaries, or low-cost model calls;
  - do not receive full reasoning every cycle.
- dormant agents:
  - no execution until reactivated by location, conflict, schedule, or event trigger.

Run modes:

- deterministic acceptance run: bounded tick count for tests.
- interactive run: user starts/stops or advances N ticks.
- background run: world advances under budget/time limits.
- story synthesis run: no new world simulation; only selects and narrates committed event history.

Stop/budget controls:

- tick budget;
- wall-clock budget;
- token/cost budget;
- event count budget;
- story arc completion;
- user stop;
- safety/error stop;
- projection_out_of_sync pause.

Reasoning:

- A living world should feel continuous, but compute must be bounded and inspectable.
- Scheduler tiers keep the system from becoming a runaway all-agent chat loop.

## Memory Architecture Policy

Decision from user discussion:

```text
Use graph-first memory.
```

Clarification:

- Graph-first means memory, beliefs, facts, secrets, relationships, and evolving character knowledge are represented and retrieved through a temporal knowledge graph from the beginning.
- Graph-first does not mean the graph replaces EventLog as canonical truth.
- EventLog remains the source of truth for what happened during simulation.
- The memory graph is a first-class projection/index over:
  - generated seed facts;
  - committed `ResolvedEvent` records;
  - validated belief updates;
  - relationship deltas;
  - secret visibility changes;
  - character-specific observations.

Core rule:

```text
No important graph fact may be treated as canon unless it has provenance.
```

Required provenance:

- `source_type`: `generated_seed`, `resolved_event`, `belief_inference`, `relationship_projection`, `manual_edit`, or `validator_repair`;
- `source_id`: seed field id, event id, repair id, or edit id;
- `character_scope`: global, character-specific, faction-specific, or narrator-only;
- `valid_from_tick`;
- optional `valid_to_tick` for changed/retracted facts;
- confidence and status where relevant.

Character memory views:

- Each character receives a scoped graph view, not the global graph.
- `CharacterMemoryView` is deny-by-default.
- A memory item is returned only if at least one explicit visibility rule allows it.
- No raw graph result may be passed through and filtered later in the prompt layer.
- All character memory retrieval in one tick uses the same pre-resolution snapshot.
- No character may see events or graph updates produced later in the same tick until the next tick.
- A character can only retrieve:
  - facts they know;
  - events they perceived;
  - beliefs they hold;
  - secrets revealed to them;
  - relationship state from their own perspective;
  - justified inferences derived from their visible evidence.
- Characters must not receive narrator-only truth, hidden secrets, or global Director plans.

MVP implications:

- Model memory as graph-shaped data from the start: entities, facts, edges, observations, beliefs, relationships, and provenance.
- MVP-A should use a deterministic local graph adapter only as a contract-compatible acceptance oracle.
- MVP-B should integrate self-hosted Graphiti as the primary graph memory backend.
- Managed Zep is a later option if scale/governance needs justify it.
- The design should keep a clean adapter boundary so Graphiti remains replaceable if implementation evidence later shows it cannot satisfy project requirements.
- Memory retrieval should support relationship, time/tick, location, involved characters, secret visibility, emotional salience, and relevance.

Reasoning:

- A simple per-character memory list is easier but weak for long fiction, secrets, relationships, and changing beliefs.
- Graph-first memory better matches story worlds where who knows what, when, why, and through whom matters.
- Keeping EventLog as ground truth prevents graph drift from becoming untraceable canon.

## Graph Memory Backend Policy

Decision from user discussion:

```text
Use graph-first memory from MVP-A and self-hosted Graphiti as the MVP-B target adapter.
```

Meaning:

- The MVP should not postpone graph-shaped memory semantics to a later phase.
- Graph-first is mandatory from MVP-A.
- MVP-A may use a deterministic local graph adapter, but it must implement the same `MemoryGraphPort` and `CharacterMemoryView` contracts as the production adapter.
- MVP-B targets self-hosted Graphiti as the primary graph memory adapter for character memory, temporal facts, relationship evolution, secret visibility, and changing beliefs.
- Managed Zep is a future option if scale/governance requirements justify it.
- The app should still own the domain contract:
  - `MemoryGraphPort`
  - `CharacterMemoryView`
  - `GraphFact`
  - `GraphEdge`
  - `Observation`
  - `Belief`
  - `SecretKnowledge`
  - `RelationshipState`
  - provenance metadata
- Graphiti is an implementation adapter behind that contract, not the product domain model itself.
- Zep should be treated separately as a possible managed service option, not as the same dependency as self-hosted Graphiti.

Required integration rules:

- All writes into Graphiti must include source provenance back to seed fields, events, repairs, or manual edits.
- All reads for character agents must go through `CharacterMemoryView`, never raw global graph access.
- Global/narrator-only facts must be queryable for validation and narration, but not retrievable by character agents unless visibility rules allow it.
- Graph writes should happen after GM/Resolver commits events, not before.
- If a graph extraction produces inferred beliefs, those beliefs must be stored as beliefs/inferences, not canonical facts.

Implementation caution:

- Before locking dependency versions in the formal spec/plan, verify current Graphiti docs, license, deployment requirements, persistence backend, API shape, and local development setup.
- If integration is heavier than expected, the fallback is not to abandon graph-first memory; the fallback is a local contract-compatible graph adapter while keeping self-hosted Graphiti as the target backend.

Reasoning:

- The user wants a strong inner runtime that can handle long fiction, secrets, relationship graphs, and evolving knowledge without collapsing into flat memory lists.
- Starting with graph-first memory forces the architecture to confront temporal graph semantics early instead of bolting it on later.
- Keeping a project-owned port prevents the engine from becoming tightly coupled to one memory vendor/library.

## Secret Visibility Enforcement Policy

Decision from user discussion:

```text
Use both write-time scope and retrieval-time enforcement.
```

Meaning:

- Secret, private knowledge, belief, observation, and relationship graph records must carry visibility/scope metadata when written.
- Character agents must never query raw global graph memory directly.
- Every character-facing retrieval must go through `CharacterMemoryView`, which filters graph results by:
  - character id;
  - faction/role scope when applicable;
  - location/perception;
  - event witness status;
  - explicit secret reveal status;
  - belief/inference ownership;
  - valid tick range;
  - narrator-only/global-only flags.
- Retrieval filtering is mandatory even if write-time scope looks correct.

Two-layer model:

```text
Write-time:
  every fact/edge/observation is saved with visibility, provenance, and valid time range

Retrieval-time:
  every character query is constrained by CharacterMemoryView and returns only allowed facts
```

Trace requirements:

- Every retrieved memory item shown to a character should be traceable to:
  - source event/seed/repair/edit;
  - visibility rule that allowed access;
  - retrieval reason/relevance score;
  - tick range;
  - whether it is fact, belief, inference, rumor, or secret.
- Secret-leak evals must test that a character cannot retrieve:
  - secrets they do not know;
  - narrator-only truth;
  - Director plans;
  - other characters' private beliefs;
  - events they did not witness or learn about.

Reasoning:

- Write-time scope alone is insufficient because a bad query can still over-fetch.
- Retrieval-time filtering alone is dangerous because raw graph records lack durable access intent.
- Two-layer enforcement is necessary for a story engine where private knowledge and delayed reveals are core product behavior.

## EventLog Granularity Policy

Decision from Oracle-assisted design review:

```text
Use hybrid event tiers.
```

Meaning:

- EventLog should not record every tiny expressive behavior as canon.
- EventLog also should not be so sparse that memory, perception, and narrator grounding have no evidence.
- Use explicit event tiers so the system can preserve canon while still keeping useful support evidence.

Event tiers:

```text
system_event
  Runtime/control event for run lifecycle, replay roots, checkpoints, branches,
  projection rebuilds, pause/resume, and synthesis metadata.
  May update runtime metadata and replay/checkpoint state.
  Must not directly change story-world canon unless paired with canon_event records.

canon_event
  A committed event that changes continuity.
  Can update projections.

supporting_observation
  Perception/witness evidence that supports memory, inference, narration, or later reveal checks.
  Can update scoped character memory when visibility rules allow.

texture_note
  Soft narrative/debug material: atmosphere, hesitation, body language, momentary tone.
  Cannot update canonical projections.
  Cannot reveal secrets.
  Should have bounded retention and should not be required for replay.
```

Projection rule:

- `system_event` may update run lifecycle metadata, replay roots, checkpoint state, branch metadata, or projection recovery metadata.
- `canon_event` may update world state, character state, relationship state, memory graph, secret visibility, and output grounding.
- `supporting_observation` may update scoped character memory or belief only when it has witness/perception evidence.
- `texture_note` must not update canonical projections, relationship scores, secret visibility, or global truth.

Reasoning:

- Fine-grained events would make the engine feel mechanical and inflate storage.
- Macro-only events may lack enough evidence for graph memory and Inspect Why.
- Hybrid tiers preserve the "hard core, soft surface" principle.

## Narration Timing Policy

Decision from Oracle-assisted design review:

```text
Render narrative output from a selected committed event batch/window.
```

Meaning:

- The final readable chapter should not be generated tick-by-tick and stitched together.
- Per-tick text may exist as debug summaries for Inspect Why, but it is not the final prose artifact.
- Chapter prose and storyboard beats should be generated from the same committed event window after the relevant simulation slice is complete.
- For MVP acceptance, the window may be a 10-tick batch.
- For the full product, the window may be a chapter-sized arc selected from a longer-running world.

Default MVP output flow:

```text
selected EventLog batch/window
-> grounded chapter prose
-> optional storyboard beats
-> prose/span and beat/event trace links
-> critic/lore validation
```

Reasoning:

- Batch rendering lets the narrator manage pacing, foreshadowing, scene rhythm, and cliffhanger better.
- It prevents the final chapter from reading like stitched logs.
- The event batch still keeps narration grounded and auditable.

## Graph Fact Category Policy

Decision from Oracle-assisted design review:

```text
Graph memory must distinguish canon, belief, rumor, planning, and narrator support.
```

Fact categories:

- `canonical_fact`: only from valid seed initialization or GM/Resolver-committed `ResolvedEvent`.
- `character_belief`: scoped to a character; may be wrong or incomplete; may come from inference.
- `rumor`: non-canon until confirmed by a later event.
- `director_candidate`: confidential planning data; never visible to character agents and never canon until committed through GM/Resolver.
- `narrator_context`: read-only rendering support; not character knowledge unless separately revealed.

Rules:

- Auto-extracted graph facts are not automatically canon.
- Graph adapter extraction may produce candidate facts, beliefs, or relationships, but the product layer must classify them before use.
- `director_candidate` must never be written into character memory.
- `director_candidate` must never be returned by `CharacterMemoryView`.
- `director_candidate` must never be included in CharacterIntent prompts unless it has become canon through a committed event.

Reasoning:

- A graph backend can infer useful relationships, but inference is not the same as story truth.
- The engine must preserve the distinction between what happened, what someone believes, what someone heard, what the Director is considering, and what the Narrator can use for style.

## Pattern Library Anti-Copy Policy

Decision from Oracle-assisted design review:

```text
Story corpora can supply abstract patterns only, not copyable story material.
```

Allowed pattern extraction:

- abstract trope;
- pacing shape;
- conflict shape;
- scene shape;
- chapter opening/ending shape;
- archetype;
- worldbuilding category;
- escalation pattern.

Forbidden extraction/use:

- exact prose;
- proper names;
- unique plot sequence;
- distinctive scene construction;
- recognizable character package;
- specific dialogue;
- identifiable setting package from a source work.

Reasoning:

- The project can learn genre grammar without copying source works.
- This boundary protects the product direction and avoids turning pattern packs into disguised plagiarism.

## Oracle Design Review Findings

Date: 2026-06-19

Method:

- Used the local `oracle` skill with `@steipete/oracle` browser mode.
- Attached `PROJECT_NOTES.md` as the design context.
- Asked Oracle for a 15-pass internal critique covering UX, event sourcing, seed contract, Director/character autonomy, phased ticks, graph-first memory, Graphiti/Zep risk, secret enforcement, narrator grounding, output format, language policy, testability, MVP scope, library risk, and missing decisions.
- Initial attachment upload failed in browser mode, so the review was rerun with explicit inline-file fallback.

Oracle verdict:

```text
APPROVE_WITH_CHANGES
```

Oracle agreed that the overall architecture is directionally strong, especially:

- `Short Context -> Auto Story Setup -> Simulation Lab -> Narrated Story`;
- EventLog as the source of truth;
- Hybrid core plus `cultivation_fantasy` pattern pack;
- Layered Seed contract;
- Director-bounded character autonomy;
- phased tick pipeline;
- write-time plus retrieval-time secret visibility enforcement.

Oracle's main warning:

```text
Graph-first memory is good, but Graphiti/Zep must remain infrastructure,
not the product domain model.
```

Accepted refinements to carry into the formal spec:

- Keep `MemoryGraphPort`, `CharacterMemoryView`, visibility rules, provenance, and canon policy owned by the app domain.
- No character, narrator, Director, or resolver layer may depend directly on raw Graphiti APIs.
- Graphiti/Zep is the target primary graph memory adapter, but a deterministic local adapter remains necessary for tests, demos, and offline reproducibility.
- Auto-extracted graph facts are not automatically canon.
- Use explicit fact categories:
  - `canonical_fact`: only from seed initialization or GM/Resolver-committed `ResolvedEvent`;
  - `character_belief`: scoped to one character and possibly inferred;
  - `rumor`: non-canon until resolved;
  - `director_candidate`: confidential planning data, not canon and not visible to characters;
  - `narrator_context`: read-only rendering support.
- `director_candidate` must be narrator/director-only planning data:
  - never written into character memory;
  - never returned by `CharacterMemoryView`;
  - never shown to CharacterIntent generation unless later committed as an event.
- Final Chapter 1 should be rendered from the 10-tick event batch, not stitched tick-by-tick prose.
- Per-tick narration may exist as debug summaries, but final prose and storyboard beats should be batch-rendered from committed events.
- Strengthen corpus/pattern-library boundary:
  - allowed: abstract trope, pacing shape, conflict shape, scene shape, archetype;
  - forbidden: exact prose, proper names, unique plot sequence, distinctive scene construction, recognizable character package.
- Add required evals before attaching real LLM agents:
  - `character_cannot_retrieve_unrevealed_secret`;
  - `character_cannot_retrieve_other_character_private_belief`;
  - `character_cannot_retrieve_director_candidate`;
  - `narrator_cannot_render_secret_without_supporting_event`;
  - `relationship_delta_requires_source_event`;
  - `memory_fact_requires_provenance`;
  - `graph_adapter_cannot_return_raw_global_results_to_character_agent`.

Oracle recommendation for pending EventLog granularity decision:

```text
Choose C: Hybrid event tiers.
```

Refined interpretation:

- `canon_event`: affects continuity and drives projections;
- `supporting_observation`: witness/perception evidence, can support memory and later inferences;
- `texture_note`: optional narrator/debug material, not canon, bounded retention, cannot update projections;
- only `canon_event` and explicitly allowed `supporting_observation` may affect memory/relationship/knowledge projections.

Graphiti/Zep verification notes from official sources:

- Graphiti is described as a temporal context graph framework for AI agents with facts that change over time, provenance to source episodes, and hybrid retrieval.
- Graphiti docs list Python 3.10+, Neo4j 5.26+ or FalkorDB 1.1.2+, and an OpenAI API key by default for LLM inference/embeddings.
- Graphiti supports alternate LLM providers, but OpenAI is the default.
- Graphiti telemetry is opt-out and can be disabled with `GRAPHITI_TELEMETRY_ENABLED=false`; tests disable telemetry automatically.
- Current release inspection on 2026-06-19 showed recent active releases and a March 2026 security hardening release for Cypher/search filter injection.

Spec implications:

- Pin Graphiti dependency versions during implementation planning.
- Disable Graphiti telemetry by default in local/dev/test unless explicitly accepted.
- Run adapter-level secret-leak regression tests on every Graphiti/Zep upgrade.
- Do not expose raw graph query strings from user or agent text.
- Treat Graphiti extraction as candidate memory/belief material unless the source is a seed initialization fact or a committed `ResolvedEvent`.

## Oracle Review Round 2 Findings

Date: 2026-06-19

Oracle verdict:

```text
APPROVE_WITH_CHANGES
```

Interpretation:

- Oracle approved the product direction as strong enough to become the product contract.
- Oracle still blocked implementation until key invariants are explicitly recorded.
- The required changes are design-contract clarifications, not product direction reversals.

Round 2 required invariants:

1. Source-of-truth hierarchy.
2. MemoryGraphPort contract.
3. CharacterMemoryView visibility contract.
4. GraphFact category enum.
5. Event tier projection permissions.
6. GMResolver conflict-resolution rules.
7. Narrator grounding/span policy.
8. DirectorPrivatePlan storage rule.
9. Pattern-library ingestion quarantine.
10. MVP-A / MVP-B gates.

Additional verified Graphiti/Zep constraints:

- `graphiti-core <= 0.28.1` had a high-severity Cypher injection advisory via unsanitized `SearchFilters.node_labels`; patched version is `0.28.2`.
- The advisory noted possible exploitation in MCP/LLM workflows through prompt injection into `search_nodes`.
- Mitigation includes upgrading, avoiding untrusted `SearchFilters.node_labels` / MCP `entity_types`, and using least-privilege graph DB credentials.
- Graphiti LLM configuration docs say it works best with providers supporting structured output and defaults to OpenAI for inference/embeddings.

## Source Of Truth Hierarchy

Formal invariant:

```text
1. User prompt constraints: intent boundary, not canon by itself
2. Validated GeneratedStorySeed: canonical initialization before simulation starts
3. Appended EventLog entries: only runtime canon
4. Projections: rebuildable derived state from seed + EventLog
5. Narrator/storyboard/UI/trace: renderings and explanations, not canon
```

Canon creation rules:

- `GeneratedStorySeed` initializes the world but does not override later committed events.
- Every run begins with a durable `RunInitialized` record that snapshots the validated seed/schema/pattern-pack versions used for that run.
- `ResolvedEvent` becomes runtime canon only when appended to EventLog.
- A temporary `ResolvedEvent` object is not independently authoritative before durable append.
- EventLog is the durable source of truth after simulation starts.
- Projections are rebuildable from seed + EventLog.

Run root:

```text
Validated seed
-> RunInitialized event/record
-> tick events
-> projections
```

RunInitialized invariant:

- `RunInitialized` is the immutable root record of a run.
- Recommended shape: EventLog entry with `tier = system_event`.
- It snapshots:
  - validated seed id/version/content hash;
  - schema versions;
  - pattern pack version;
  - simulation engine version;
  - run config;
  - initial projection baseline.
- Replay root is:

```text
RunInitialized + EventLog suffix -> rebuilt projections
```

Not canon by themselves:

- LLM draft seed text;
- raw composer output before validation;
- `director_candidate`;
- graph auto-extraction;
- `character_belief`;
- `rumor`;
- `narrator_context`;
- storyboard beat;
- prose sentence;
- UI summary;
- debug trace text.

Short form:

```text
Prompt creates a proposed world.
Seed validation makes it runnable.
Simulation creates truth.
Graph memory remembers truth differently per character.
Narrator explains truth beautifully.
Trace proves the narrator did not cheat.
```

## MemoryGraphPort Contract

Decision:

```text
The product domain owns graph memory semantics.
Self-hosted Graphiti is an adapter behind MemoryGraphPort.
Managed Zep is a possible future adapter/service, not the domain model.
```

No domain component may depend on raw Graphiti APIs:

- CharacterAgent;
- Director;
- GMResolver;
- Narrator;
- Critic/Lore Keeper;
- UI Inspect Why.

Allowed access surfaces:

- `MemoryGraphPort`: write/read adapter boundary owned by the app.
- `CharacterMemoryView`: scoped character retrieval.
- `NarratorMemoryView`: narrator/lore retrieval with grounding constraints.
- `ValidatorMemoryView`: validation-only access for leak/canon checks.

Graphiti extraction handling:

- Extraction output is candidate material until classified by product policy.
- It may become:
  - `canonical_fact` only from valid seed initialization or committed `ResolvedEvent`;
  - `character_belief`;
  - `rumor`;
  - `narrator_context`;
  - `rejected_candidate`.

Minimum method-level shape for the formal spec:

```text
append_seed_facts(seed_id, facts[])
append_event_facts(event_id, tick_id, facts[], observations[], relationship_deltas[])
append_beliefs(character_id, source_event_id, beliefs[])
get_character_memory_view(character_id, tick_id, query_context)
get_narrator_context(event_ids, claim_scope)
get_validator_context(run_id, validation_scope)
rebuild_from_event_log(seed, event_log)
```

Every returned memory item must include:

- `id`;
- `category`;
- `visibility_scope`;
- `source_type`;
- `source_id`;
- `valid_from_tick`;
- `valid_to_tick`;
- `confidence`;
- `allowed_by_rule`;
- `retrieval_reason`.

## Graph Query Safety Policy

Decision:

```text
Graph query construction is a security boundary.
```

Rules:

- Never pass raw user text, agent text, or LLM-generated labels directly into graph filter labels.
- Use allowlisted entity and edge labels owned by the product schema.
- Pin Graphiti/Graphiti-core to a patched version during implementation planning.
- Minimum allowed Graphiti-core baseline: `>= 0.28.2` because of the 2026 Cypher injection advisory.
- Run adapter-level injection regression tests on every dependency upgrade.
- Graph DB credentials must use least privilege.
- Do not expose Graphiti MCP tools directly to untrusted prompts in MVP.
- Disable telemetry by default in local/dev/test/demo unless explicitly accepted:

```text
GRAPHITI_TELEMETRY_ENABLED=false
```

## Event Tier Projection Permissions

Decision:

```text
Event tiers must define projection permissions explicitly.
```

Permissions:

- `canon_event`
  - may update canonical projections;
  - may change world state, relationship state, memory graph, secret visibility, character state, goals, and output grounding.
- `supporting_observation`
  - may update scoped memory or belief only for characters allowed by perception/visibility;
  - may support narrator grounding, suspicion, inference, or later discovery;
  - may not update global canon;
  - may not reveal secret truth unless paired with a valid reveal event.
- `texture_note`
  - may support prose style/debug only;
  - must not update memory, relationship, secret visibility, world state, or canon;
  - must not be required for deterministic replay.

Required fields for `supporting_observation`:

- `observer_id` or `observer_scope`;
- `perception_channel`;
- `observed_event_id` or `scene_context_id`;
- `visibility_rule`;
- `confidence`;
- `allowed_effect`: memory, belief, suspicion, narrator_grounding, or debug_only.

Additional rule:

- A `supporting_observation` cannot reveal the true content of a secret unless paired with a `canon_event` reveal.

## Relationship Projection Semantics

Decision:

```text
Canonical relationship state and perceived relationship belief are different.
```

Rules:

- `canonical_relationship_delta` requires a `canon_event`.
- `perceived_relationship_belief` may be created from `supporting_observation` if visibility rules allow it.
- A character observing betrayal may change that character's belief, suspicion, fear, trust, or emotional state.
- That observation must not mutate global/canonical relationship truth unless GMResolver commits a relationship-changing `canon_event`.

Reasoning:

- Relationships in fiction are partly objective history and partly subjective interpretation.
- The engine needs both without letting observations mutate global canon accidentally.

## Persistent World Time Model

Decision:

```text
Long-running worlds need more than tick_id.
```

Required identifiers:

- `simulation_time`: in-world clock/time.
- `tick_id`: deterministic ordering within a run.
- `cycle_id`: scheduler/execution cycle grouping.
- `event_window_id`: selected event group for synthesis.
- `arc_id`: narrative/social/conflict arc grouping.
- `checkpoint_id`: replay/rebuild checkpoint for long-running worlds.

Rules:

- `tick_id` orders events within a run.
- `simulation_time` represents the world clock and may advance unevenly.
- `event_window_id` groups events for synthesis.
- `checkpoint_id` supports replay, rebuild, and long-running projection recovery.
- Synthesized chapters reference event windows, not arbitrary raw prose history.

## World Snapshot Contract

Decision:

```text
Parallel CharacterIntent generation must share one pre-resolution snapshot.
```

Minimum `WorldSnapshot` / `ProjectionSnapshot` fields:

- `snapshot_id`;
- `run_id`;
- `tick_id`;
- `cycle_id`;
- `event_log_high_watermark`;
- `projection_version`;
- `graph_projection_version`;
- `world_state_version`;
- `created_at`.

Rules:

- All `CharacterIntent` records in the same tick must reference the same pre-resolution `snapshot_id`.
- The snapshot freezes what is visible before intents are generated.
- No character may see events, graph writes, or projection updates produced later in the same tick.

## Run Advance Lease Policy

Decision:

```text
Only one scheduler/runner may advance a run at a time.
```

`RunAdvanceLease` fields:

- `run_id`;
- `lease_id`;
- `acquired_by`;
- `acquired_at`;
- `expires_at`;
- `last_heartbeat_at`;
- `current_cycle_id`.

Rules:

- Run advancement requires a run-scoped lease.
- A tick commit must verify the active lease before appending events.
- Duplicate or stale runners must not append EventLog entries.
- Interactive, background, and scheduled workers all use the same lease protocol.

## Event Summary And Compaction Policy

Decision:

```text
Summaries are navigation/retrieval aids, not replacement canon.
```

Summary categories:

- `event_summary`:
  - derived from an event range;
  - not a new canon source;
  - may support retrieval/navigation;
  - must cite source event ids or source event range.
- `offscreen_simulation_result`:
  - may become canon only if committed as `canon_event` records.

Rules:

- A summary is not canon unless backed by source event ranges.
- Summaries cannot replace raw EventLog for replay.
- Story Synthesizer may use summaries to select arcs but must ground major claims in source events.

## GMResolver Conflict Resolution Policy

Decision:

```text
Parallel CharacterIntents require deterministic conflict resolution.
```

When multiple `CharacterIntent` records conflict, GMResolver resolves by:

1. feasibility against current world snapshot;
2. visibility and knowledge validity;
3. physical, social, and canon constraints;
4. declared intent priority;
5. character capability/resource state;
6. Director pressure as soft bias, not forced outcome;
7. deterministic tie-breaker using simulation seed + tick id + stable actor ordering.

Rules:

- A character intent based on knowledge the character does not have should be rejected or repaired before resolution.
- GMResolver may produce partial success, costly success, delayed outcome, blocked outcome, misinterpretation, or backfire.
- GMResolver must explain every committed event with input intents and resolution reasons.

Transaction semantics:

- A tick commit is atomic: either all accepted `ResolvedEvent` records and projection writes for that tick are committed, or none are.
- Projection updates happen after EventLog append.
- Graph writes happen after EventLog append and must reference committed event ids.
- If graph write fails, the run enters a recoverable `projection_out_of_sync` state.
- EventLog remains authoritative during projection recovery.
- When `projection_out_of_sync` is true:
  - character agents must not continue using stale `CharacterMemoryView` results;
  - narrator may only render from EventLog-backed context;
  - the system must either rebuild projections from seed + EventLog or pause the run;
  - recovery must record `projection_rebuilt_at` and `projection_source_event_range`.

## Narrator Grounding And Span Policy

Decision:

```text
Narrator is renderer, not author of truth.
```

Claim categories:

- Strictly supported claim:
  - major action;
  - fact;
  - reveal;
  - relationship change;
  - location change;
  - injury;
  - promise;
  - betrayal;
  - ability/resource change.
- Allowed soft interpolation:
  - mood;
  - pacing;
  - sensory detail;
  - minor gesture;
  - prose rhythm;
  - atmospheric detail.
- Forbidden unsupported claim:
  - secret reveal;
  - new ability;
  - new faction motive;
  - relationship delta;
  - hidden identity;
  - off-screen event;
  - new canon fact.

Trace rule:

- Every major prose claim must link to one or more supporting event ids.
- Soft prose may link to event-span context instead of one exact event.
- Soft prose cannot introduce new canon.

Narrator claim classifier:

- Each prose sentence/span should be classified as:
  - `strict_claim`;
  - `soft_interpolation`;
  - `unsupported_claim`.
- `unsupported_claim` count must be zero for major facts.
- `soft_interpolation` must not create new canon.
- `strict_claim` must have event/support ids.

## Story Synthesizer / Narrative Compiler Policy

Decision:

```text
Story output is compiled from event history, not generated as the primary simulation loop.
```

Responsibilities:

- select an event window, character arc, location arc, faction arc, or conflict arc;
- identify salient events and supporting observations;
- group events into scenes;
- preserve causal order unless explicitly doing a recap/flashback;
- generate chapter prose and optional storyboard beats from the same event selection;
- link major claims to supporting event ids;
- mark skipped events or summarized intervals;
- preserve character knowledge boundaries when writing close POV;
- avoid unsupported new canon.

Inputs:

- EventLog window;
- relevant projection snapshots;
- character memory views when writing from a limited POV;
- relationship deltas;
- secret visibility history;
- narrator/lore context;
- tone/style settings.

Outputs:

- chapter prose;
- storyboard beats;
- event-to-prose support map;
- summary of omitted low-salience events;
- critic/lore findings.

Modes:

- latest-window chapter;
- character-focused chapter;
- location-focused scene;
- conflict recap;
- timeline summary;
- storyboard planning;
- chapter rewrite from same event support.

Reasoning:

- A long-running world will produce too many events to narrate linearly.
- The Synthesizer converts simulation history into readable fiction while preserving auditability.

## DirectorPrivatePlan Policy

Decision:

```text
Director planning data must be stored separately from character memory.
```

`DirectorPrivatePlan`:

- stored in a separate planning store outside character memory;
- not indexed into `CharacterMemoryView`;
- not written as a GraphFact visible to agents;
- if indexed for validation/search, it must live under a non-character namespace that `CharacterMemoryView` cannot query;
- not eligible for narrator rendering;
- not accessible to CharacterIntent generation;
- can become canon only through approved seed change or GM/Resolver committed event.

Reasoning:

- `director_candidate` being "not canon" is insufficient if it can leak through graph retrieval or prompts.
- Future twists must remain private planning data until legitimately introduced.

## Pattern Library Ingestion Quarantine

Decision:

```text
Raw corpus text must be quarantined away from generation prompts.
```

Pipeline:

```text
source text
-> abstract pattern extraction
-> copyright/plagiarism filter
-> pattern normalization
-> source quarantine
-> approved pattern pack
-> Auto Story Setup
```

Rules:

- Raw corpus text must not be placed directly into generation prompts for story output.
- Raw corpus text must not appear in Auto Story Setup prompts, narrator prompts, character prompts, or eval fixtures unless the fixture specifically tests rejection.
- Only approved abstract patterns may be used by Auto Story Setup.
- Forbidden source-specific material includes:
  - recognizable sequence of scenes;
  - distinctive power system names;
  - signature mentor/protagonist package;
  - unique betrayal/reveal chain;
  - named organizations/items/locations;
  - specific dialogue;
  - source-identifiable setting packages.

Required artifacts:

- `corpus_manifest.json`;
- `raw_source_quarantine/`;
- `pattern_candidates/`;
- `approved_pattern_pack/`;
- `rejected_patterns/`;
- `similarity_report.json`;
- `forbidden_names_terms.json`.

## MVP Gates

Decision:

```text
Split MVP into MVP-A deterministic contract demo and MVP-B Graphiti-backed product demo.
```

This does not abandon graph-first memory. It makes graph semantics mandatory from MVP-A and self-hosted Graphiti integration mandatory for MVP-B while preserving a deterministic acceptance oracle.

MVP-A: deterministic contract demo

- deterministic stub composer;
- local contract-compatible `MemoryGraphPort` adapter;
- one generated scenario;
- 3-5 characters;
- 1-2 secrets;
- 10 phased ticks;
- EventLog with hybrid event tiers;
- CharacterMemoryView;
- GMResolver;
- batch-rendered chapter prose;
- optional storyboard beats;
- Inspect Why;
- eval report.

MVP-A acceptance slices:

- MVP-A0: deterministic seed -> validation -> `RunInitialized`.
- MVP-A1: 3 ticks, 2 characters, 1 secret, EventLog only.
- MVP-A2: local `MemoryGraphPort` + `CharacterMemoryView` leak tests.
- MVP-A3: 10 ticks + relationship/memory projections.
- MVP-A4: grounded chapter prose + span trace.
- MVP-A5: Inspect Why + eval report.

Storyboard beats remain optional until prose grounding is proven.

MVP-B: Graphiti-backed product demo

- self-hosted Graphiti adapter behind the same `MemoryGraphPort`;
- provenance mapping into graph episodes/facts;
- character-scoped graph retrieval;
- adapter leak tests;
- dependency pinning;
- telemetry disabled by default;
- graph query safety checks;
- graph upgrade regression suite.

Exit rule:

- MVP-A must pass deterministic tests before real LLM agents are trusted.
- MVP-B must pass adapter leak/security/provenance tests before Graphiti-backed runs are presented as reliable.

## Generated Seed Field Provenance Policy

Decision:

```text
Every seed entity and important field must carry provenance.
```

Minimum provenance fields:

- `source`: `user_provided`, `inferred_from_prompt`, `genre_pattern`, or `director_added`;
- `confidence`;
- `editable`;
- `lock_status`;
- `source_span` or `source_reason` when available.

Fields requiring provenance:

- protagonist role;
- central conflict;
- secret truth;
- faction motive;
- relationship reason;
- opening pressure;
- power system assumptions;
- major setting rule;
- generated character goal;
- generated faction agenda.

Reasoning:

- Field-level provenance powers Repair Preview, review gate, later user edits, and traceable generation.
- Global seed provenance policy is insufficient because mixed-source entities are common.

## Versioning, Edit, Branch, And Replay Policy

Schema/version identifiers required for reproducible runs:

- `seed_schema_version`;
- `event_schema_version`;
- `graph_fact_schema_version`;
- `pattern_pack_version`;
- `simulation_engine_version`;
- `narrator_prompt_version`;
- `eval_suite_version`.

Edit-after-simulation rule:

- After simulation starts, user edits cannot mutate past canon directly.
- A user edit must create one of:
  - new run from edited seed;
  - `manual_edit` event;
  - retcon proposal requiring explicit approval;
  - branch/fork from tick N.

Branch/replay behavior:

- A run is immutable once committed.
- A branch references `parent_run_id` and `branch_from_tick`.
- Branch replay must use the same seed snapshot and event prefix up to `branch_from_tick`.
- Replay rebuilds projections from `RunInitialized` + EventLog.

## Required Core Vs Optional Layers Boundary

Decision:

```text
Anything GMResolver needs for feasibility cannot remain optional-only.
```

Rules:

- Any world rule, ability, resource, rank, item, location constraint, or faction rule required for GMResolver feasibility must live in `required_core` or be normalized into `required_core` before simulation starts.
- `optional_layers` may enrich prose, UI, tone, inspection, future editing, and pattern explanation.
- GMResolver must not depend on optional-only data.
- `optional_layers.power_system` may remain rich, but resolver-relevant subsets must be copied/normalized into:
  - `required_core.world.minimal_rules`;
  - `required_core.abilities`;
  - `required_core.resources`;
  - `required_core.items`;
  - `required_core.constraints`;
  - character abilities/resources;
  - faction constraints;
  - location constraints;
  - item/resource records.
- Genre-specific detail may still live in `extensions.cultivation`, but the resolver-relevant generic part must be present in required core.

Reasoning:

- A cultivation power system is optional for the generic core, but not optional for a cultivation run if it controls feasibility.

## GeneratedStorySeed And RunConfig Separation

Decision:

```text
GeneratedStorySeed defines the world.
RunConfig defines how the simulation is executed.
```

GeneratedStorySeed owns:

- premise;
- world;
- locations;
- characters;
- factions;
- secrets;
- relationships;
- opening scene;
- rules/resources/abilities required for feasibility;
- field-level provenance.

RunConfig owns:

- `run_mode`;
- `tick_budget`;
- `wall_clock_budget`;
- `event_budget`;
- `agent_scheduling_policy`;
- `stop_conditions`;
- `output_request_policy`;
- eval expectations for acceptance/demo runs.

Rules:

- A persistent world may reuse the same validated seed with multiple run configs.
- Acceptance expectations like `must_create_events` are demo/eval guidance, not hard plot commands.
- `must_create_events` may guide Director pressure, but GMResolver must not force impossible or unsupported events.
- RunConfig changes do not rewrite seed canon.

## SeedFact Policy

Decision:

```text
Seed facts must be structured, scoped, and provenance-bearing.
```

Minimum `SeedFact` fields:

- `id`;
- `category`;
- `text` or structured `value`;
- `visibility_scope`;
- `known_by`;
- `hidden_from`;
- `source`;
- `confidence`;
- `lock_status`;
- `source_reason` or `source_span`.

Rules:

- `known_facts` and `private_facts` must not remain raw text arrays at runtime.
- No raw private fact string may be passed directly into CharacterIntent, Narrator, Graphiti, or memory prompts.
- Raw seed facts must first become classified `SeedFact` records.
- Private fact, secret truth, belief, and rumor must remain separate categories.

Reasoning:

- A private belief may be false.
- A secret truth may be canon but hidden.
- A rumor may be non-canon.
- Treating all of these as raw text creates leak risk.

## Runtime Object Minimum Schemas

Decision:

```text
CharacterIntent and ResolvedEvent need minimum schemas before implementation.
```

Minimum `CharacterIntent` fields:

- `intent_id`;
- `run_id`;
- `tick_id`;
- `actor_id`;
- `perceived_snapshot_id`;
- `visible_memory_refs`;
- `visible_fact_refs`;
- `goal_refs`;
- `intended_action`;
- `target_entities`;
- `declared_priority`;
- `expected_outcome`;
- `risk_acceptance`;
- `knowledge_assumptions`;
- `generated_by`;
- `prompt_version`.

Minimum `ResolvedEvent` fields:

- `event_id`;
- `run_id`;
- `tick_id`;
- `tier`;
- `event_type`;
- `actor_ids`;
- `target_ids`;
- `source_intent_ids`;
- `resolver_outcome`;
- `resolver_reason`;
- `preconditions_checked`;
- `consequences`;
- `visibility_effects`;
- `projection_effects`;
- `narrator_grounding_eligible`;
- `committed_at`.

Reasoning:

- Phased ticks, replay, Inspect Why, conflict resolution, and narrator grounding all depend on these references.

## Projection Outbox Policy

Decision:

```text
Projection writes use an idempotent projection-outbox model.
```

Rules:

- EventLog append is durable first.
- Projection jobs then write memory, relationship, visibility, and graph facts using committed event ids.
- Each projection write must be idempotent by `run_id + event_id + projection_type`.
- If projection fails, the run enters `projection_out_of_sync`.
- While `projection_out_of_sync`, character-agent execution is paused until projections are rebuilt or caught up.
- Duplicate graph facts must be prevented by projection idempotency keys.

Reasoning:

- Self-hosted Graphiti is an external adapter and cannot be treated as the same local transaction as EventLog append.

## Run Isolation Policy

Decision:

```text
Every durable runtime artifact must be run-scoped.
```

Required scope fields:

- Every EventLog entry includes `run_id`.
- Every GraphFact, Observation, Belief, SecretKnowledge, RelationshipState, DirectorPrivatePlan, trace span, and projection row includes `run_id`.
- Branch data includes `parent_run_id` and `branch_from_tick`.
- `CharacterMemoryView` always filters by:
  - `run_id`;
  - branch/current run scope;
  - `character_id`;
  - `tick_id`;
  - visibility rules.

Reasoning:

- Multiple story runs and branches must never leak memory, secrets, or graph facts into each other.

## Director Candidates In Seed Policy

Decision:

```text
director_candidates in GeneratedStorySeed are setup/planning candidates only.
```

Rules:

- They must not initialize character memory.
- They must not become GraphFact records visible to characters.
- They must not be passed to CharacterIntent.
- They must not be used by Narrator as event support.
- They may be shown only in Generated Assumptions / Director panel.
- They may become canon only through explicit approval or GMResolver committed event.

Reasoning:

- A future twist can leak if stored as normal seed content.

## LLM And Prompt Boundary Policy

Decision:

```text
User/corpus/generated text is data, not instructions.
```

Rules:

- User story prompts, raw corpus text, generated pattern candidates, character dialogue, and LLM outputs are data.
- No agent may receive raw corpus text as system/developer instructions.
- No character agent may call tools directly in MVP.
- No generated text may define new schema labels, graph labels, eval rules, resolver permissions, or visibility rules.
- All LLM outputs must pass schema validation before entering seed, intent, event, graph, narrator, or eval layers.
- Tool calls, graph labels, and schema labels must come from allowlisted product code/config, not generated prose.

Reasoning:

- The product intentionally ingests user prompts and story corpora, so prompt injection must be treated as a domain boundary.

## MVP-A UI Scope Policy

Decision:

```text
MVP-A may be CLI/report-first before full UI.
```

Required proof:

- deterministic seed;
- validation;
- `RunInitialized`;
- 10 ticks;
- EventLog;
- scoped memory;
- grounded chapter;
- trace/eval report.

Rules:

- A polished web UI is not required until the deterministic runtime contract loop is passing.
- Inspect Why may begin as a structured report before becoming a full React panel.

## Oracle Final Living-World Approval

Date: 2026-06-19

Method:

- The previous full-note Oracle run hit browser readiness issues because `PROJECT_NOTES.md` had grown too large.
- Created a smaller approval brief at `.superpowers/oracle/living-world-final-approval-brief.md`.
- Ran Oracle browser review on the focused brief.

Oracle verdict:

```text
APPROVE
```

Oracle approval summary:

- The design is coherent enough to extract into formal product contract and ADRs.
- No remaining design contradiction justified `APPROVE_WITH_BLOCKERS`.
- The authority model is clear:
  - `GeneratedStorySeed` initializes the world but does not overwrite runtime truth.
  - `RunInitialized` is the immutable run-root event.
  - EventLog becomes the source of truth after simulation starts.
  - GMResolver is the only canon-committing runtime authority.
  - Director, Narrator, and Story Synthesizer are non-authoritative unless backed by committed events.
  - Graph memory is projection/index, not canon.
  - Character memory access is deny-by-default through `CharacterMemoryView`.
  - 10 ticks is an acceptance slice, not a product limit.

Oracle non-blocking extraction notes:

- Define the canonical `EventLogEntry` envelope once, then specialize `ResolvedEvent`, `RunInitialized`, checkpoint, branch, projection rebuild, and synthesis metadata under it.
- Make `projection_out_of_sync` a formal run state with allowed/blocked operations.
- Define the minimum `canon_event` taxonomy early, even if extensible.
- Make branch scoping mandatory in all memory/projection keys, not just `run_id`.
- Specify whether failed/rejected intents become trace-only records or committed non-canon events.
- Add deterministic fixture requirements for MVP-A: seed hash, scheduler seed, prompt versions, model/provider versions, and replay expectation.
- Treat narrator claim categories as an eval contract: unsupported major claims must fail the gate.

## Run Mode UX Policy

Decision from user discussion:

```text
Use hybrid controlled run mode plus optional background living mode.
```

Meaning:

- MVP default should use controlled/manual advancement for testability and debugging.
- User can advance N ticks/cycles, inspect the timeline, inspect memory, and then continue.
- Product direction still supports background living worlds.
- A later toggle such as `Let world run` can advance the world continuously within budget limits.

Modes:

- `controlled_step`: user advances one tick/cycle or a small chosen number.
- `controlled_batch`: user runs a bounded batch, such as 10 ticks, for acceptance/debugging.
- `background_living`: world advances under tick/time/event/token budgets until paused/stopped.
- `synthesis_only`: no new simulation; compile story from existing EventLog windows.

Rules:

- Background mode must support pause/resume.
- Background mode must obey run budgets and `RunAdvanceLease`.
- Background mode must stop on `projection_out_of_sync`, validation failure, safety stop, or user stop.
- Controlled mode remains the deterministic acceptance path.

Reasoning:

- The user wants a world that can keep living.
- The engine still needs a controlled path to prove memory, secrecy, event replay, and narrator grounding before long background runs are trusted.

## Required Eval Gate Additions

Required before real LLM agents are trusted:

- `character_cannot_retrieve_unrevealed_secret`;
- `character_cannot_retrieve_other_character_private_belief`;
- `character_cannot_retrieve_director_candidate`;
- `narrator_cannot_render_secret_without_supporting_event`;
- `relationship_delta_requires_source_event`;
- `memory_fact_requires_provenance`;
- `graph_adapter_cannot_return_raw_global_results_to_character_agent`;
- `supporting_observation_cannot_update_global_canon`;
- `texture_note_cannot_update_projection`;
- `director_candidate_cannot_be_written_to_graph_memory`;
- `graph_extracted_fact_defaults_to_candidate_not_canon`;
- `narrator_soft_detail_cannot_create_new_event`;
- `resolver_rejects_intent_based_on_unknown_secret`;
- `same_seed_same_tick_batch_produces_same_event_log`;
- `pattern_pack_cannot_emit_forbidden_source_specific_material`;
- `repair_preview_cannot_auto_change_core_premise`;
- `character_intent_prompt_contains_no_global_secret`;
- `character_intent_prompt_contains_no_director_private_plan`;
- `character_intent_prompt_memory_items_all_have_allowed_by_rule`;
- `narrator_prompt_contains_only_event_supported_strict_claims`;
- `composer_output_rejected_if_missing_provenance`;
- `seed_repair_requires_approval_for_protagonist_role_change`;
- `eventlog_replay_rebuilds_same_projection_state`;
- `graph_adapter_upgrade_preserves_visibility_results`.

## OpenCode Runtime Research and Agent Environment Decision

User intent:

```text
Use the locally installed OpenCode as an agent/model execution layer, potentially with multiple sub-agents or multiple processes, while building a shared world where agents interact continuously.
```

Local finding:

- `opencode` is installed locally.
- Local version checked: `opencode 1.2.27`.
- Available commands include `run`, `serve`, `agent`, `mcp`, `models`, `session`, `export`, `import`, and related CLI/server commands.

Research findings:

- OpenCode is an AI coding agent runtime, not a story-world simulator. It is useful as a programmable model/agent worker, but should not own world truth.
- OpenCode supports a headless server via `opencode serve`; official docs describe an HTTP API/OpenAPI server and multiple clients interacting with the same server.
- OpenCode supports custom agents with model, prompt, tools, permissions, and modes such as primary/subagent/all.
- OpenCode supports many providers through Models.dev / AI SDK, including local-model style provider routing depending on local config.
- OpenCode MCP integration can expose external tools, but story-world write tools must not be exposed directly to character agents.

Best-practice patterns from related systems:

- Concordia pattern: central environment/GM observes, schedules, resolves, and terminates; simultaneous engines can collect multiple agent actions then let the GM resolve the batch.
- AI Town pattern: agents run as async workers in the game loop, then submit inputs back to the engine; the engine processes state transitions.
- AgentScope pattern: event-based multi-agent runtime with permissions, sessions, monitoring, and distributed actor-style execution.
- LangGraph pattern: use explicit workflows, routers, subagents, and context engineering instead of letting every agent see everything.
- SOTOPIA pattern: useful social interaction/evaluation benchmark, but not a persistent story-world core.

Decision:

```text
Use OpenCode as the LLM/agent worker runtime.
Do not let OpenCode agents own or mutate the shared world directly.
Build a WorldRuntime/Environment Server as the authority.
```

Recommended interaction model:

```text
WorldRuntime
  -> Scheduler selects active/nearby/background/dormant agents
  -> PerceptionFilter builds CharacterMemoryView + WorldSnapshot
  -> OpenCode worker receives scoped task prompt
  -> Worker returns strict CharacterIntent JSON
  -> GMResolver validates and resolves batched intents
  -> EventLog appends canon/non-canon events
  -> ProjectionOutbox updates memory, relationships, secrets, world state
  -> StorySynthesizer compiles event windows into prose/storyboard
```

OpenCode usage options:

- MVP experiment: spawn `opencode run --agent <agent> --model <model> "<task>"` per character decision. Simple but heavier and less controllable.
- Preferred runtime: run `opencode serve` and drive it via HTTP/SDK sessions from the WorldRuntime. Better for orchestration, streaming, session tracking, and multiple clients.
- Advanced later: expose read-only world tools via MCP to character agents, while reserving write/event tools for GMResolver/WorldController only.

Permission policy:

- Character agents may read only their scoped prompt/context and return `CharacterIntent`.
- Character agents must not call `write_event`, `update_world_state`, `update_relationship`, or raw graph-memory queries.
- GM/Resolver tools may commit `ResolvedEvent`.
- Director/Critic/Narrator may inspect approved event windows and produce non-authoritative output unless GM commits repair events.

Primary rule:

```text
Multi-agent interaction must be environment-mediated, not peer-to-peer chat.
```

Why:

- Direct agent-to-agent chat leaks secrets and destroys traceability.
- A central world runtime can enforce visibility, schedule active agents, batch intents, resolve conflicts, and preserve EventLog as source of truth.
- OpenCode can still provide strong model diversity and sub-agent execution without becoming the simulation engine.
