from __future__ import annotations

from pathlib import Path

from .evals import evaluate_run
from .event_log import EventLog
from .models import EvalResult, StoryOutput, WorldSeed
from .projections import ProjectionStore
from .resolver import GMResolver
from .scheduler import TieredScheduler
from .synthesizer import StorySynthesizer
from .workers import CharacterWorker


class WorldRuntime:
    def __init__(
        self,
        *,
        seed: WorldSeed,
        worker: CharacterWorker,
        event_log_path: Path | None = None,
    ) -> None:
        self.seed = seed
        self.worker = worker
        self.event_log = EventLog(event_log_path)
        self.projections = ProjectionStore(seed)
        self.scheduler = TieredScheduler()
        self.resolver = GMResolver(seed, self.event_log)
        self.synthesizer = StorySynthesizer()
        self._initialized = False

    def initialize(self) -> None:
        event = self.resolver.initialize_run()
        self.projections.apply(event)
        self._initialized = True

    def advance(self, ticks: int) -> None:
        if ticks < 1:
            raise ValueError("ticks must be >= 1")
        if not self._initialized:
            self.initialize()
        start_tick = self.projections.tick + 1
        for tick in range(start_tick, start_tick + ticks):
            intents = []
            for character_id in self.scheduler.active_characters_for_tick(tick):
                view = self.projections.memory_view_for(
                    character_id,
                    public_scene=self.seed.premise,
                )
                intent = self.worker.decide(view)
                if intent.character_id != character_id:
                    raise ValueError(
                        f"worker for {character_id} returned intent for "
                        f"{intent.character_id}"
                    )
                intents.append(intent)
            for event in self.resolver.resolve_tick(tick, intents):
                self.projections.apply(event)

    def render_story(self) -> StoryOutput:
        return self.synthesizer.render_chapter(self.event_log.events)

    def evaluate(self) -> tuple[EvalResult, ...]:
        return evaluate_run(
            seed=self.seed,
            events=self.event_log.events,
            projections=self.projections,
            story=self.render_story(),
        )
