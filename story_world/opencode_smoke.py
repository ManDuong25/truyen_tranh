from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from .projections import ProjectionStore
from .scenarios import build_bridge_scenario
from .workers import OpenCodeCharacterWorker, OpenCodeExecutionError


def main() -> int:
    parser = argparse.ArgumentParser(description="Run an OpenCode worker smoke test.")
    parser.add_argument("--agent", default="story-character-intent")
    parser.add_argument("--model", default="opencode/deepseek-v4-flash-free")
    parser.add_argument("--character", default="linh")
    parser.add_argument("--out", type=Path, default=Path("runs/us002-opencode-smoke"))
    args = parser.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    report = run_smoke(
        agent=args.agent,
        model=args.model,
        character_id=args.character,
    )
    (args.out / "opencode_smoke_report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["status"] == "passed" else 2


def run_smoke(
    *,
    agent: str = "story-character-intent",
    model: str | None = "opencode/deepseek-v4-flash-free",
    character_id: str = "linh",
) -> dict:
    seed = build_bridge_scenario(run_id="run_opencode_smoke")
    projections = ProjectionStore(seed)
    view = projections.memory_view_for(character_id, public_scene=seed.premise)
    worker = OpenCodeCharacterWorker(agent=agent, model=model)
    try:
        intent = worker.decide(view)
    except OpenCodeExecutionError as exc:
        status = "unavailable" if exc.is_provider_unavailable() else "failed"
        return {
            "status": status,
            "agent": agent,
            "model": model,
            "character_id": character_id,
            "error_name": exc.error_name,
            "error": str(exc),
            "provider_unavailable": exc.is_provider_unavailable(),
        }
    if intent.character_id != character_id:
        return {
            "status": "failed",
            "agent": agent,
            "model": model,
            "character_id": character_id,
            "error_name": "CharacterIdentityMismatch",
            "error": (
                f"OpenCode returned intent for {intent.character_id}, "
                f"expected {character_id}."
            ),
            "provider_unavailable": False,
            "intent": asdict(intent),
        }
    return {
        "status": "passed",
        "agent": agent,
        "model": model,
        "character_id": character_id,
        "intent": asdict(intent),
    }


if __name__ == "__main__":
    raise SystemExit(main())
