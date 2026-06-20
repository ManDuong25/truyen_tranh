from __future__ import annotations

import argparse
import json
from pathlib import Path

from .runtime import WorldRuntime
from .scenarios import build_bridge_scenario
from .workers import ScriptedCharacterWorker


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the story-world POC.")
    parser.add_argument("--ticks", type=int, default=10)
    parser.add_argument("--out", type=Path, default=Path("runs/us001-demo"))
    args = parser.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    seed = build_bridge_scenario()
    runtime = WorldRuntime(
        seed=seed,
        worker=ScriptedCharacterWorker(),
        event_log_path=args.out / "events.jsonl",
    )
    runtime.advance(args.ticks)
    story = runtime.render_story()
    eval_results = runtime.evaluate()

    (args.out / "chapter_1.txt").write_text(
        _format_story(story),
        encoding="utf-8",
    )
    (args.out / "story.json").write_text(
        json.dumps(story.to_json_dict(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    (args.out / "eval_report.json").write_text(
        json.dumps(
            [result.to_json_dict() for result in eval_results],
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    print(f"Wrote {len(runtime.event_log.events)} events to {args.out / 'events.jsonl'}")
    print(f"Wrote story and eval report to {args.out}")
    failed = [result.name for result in eval_results if not result.passed]
    if failed:
        print(f"Eval failures: {failed}")
        return 1
    print("All evals passed.")
    return 0


def _format_story(story) -> str:
    lines = [story.title, ""]
    for paragraph in story.paragraphs:
        lines.append(paragraph.text)
        lines.append(f"[supports: {', '.join(paragraph.support_event_ids)}]")
        lines.append("")
    return "\n".join(lines).strip() + "\n"


if __name__ == "__main__":
    raise SystemExit(main())
