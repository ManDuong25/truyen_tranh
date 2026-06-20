from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from story_world.models import CharacterIntent, EventLogEntry, EventTier
from story_world.projections import ProjectionStore
from story_world.runtime import WorldRuntime
from story_world.scenarios import build_bridge_scenario
from story_world.workers import ScriptedCharacterWorker


class WorldRuntimeTests(unittest.TestCase):
    def run_runtime(self, ticks: int = 10) -> WorldRuntime:
        seed = build_bridge_scenario()
        runtime = WorldRuntime(seed=seed, worker=ScriptedCharacterWorker())
        runtime.advance(ticks)
        return runtime

    def test_run_produces_expected_event_log_shape(self) -> None:
        runtime = self.run_runtime()
        events = runtime.event_log.events

        self.assertEqual(events[0].event_type, "run_initialized")
        self.assertEqual(events[0].tier, EventTier.SYSTEM)
        self.assertEqual(len(events), 20)
        self.assertTrue(all(event.sequence == index + 1 for index, event in enumerate(events)))
        self.assertTrue(
            all(event.visible_to for event in events if event.tier == EventTier.CANON)
        )

    def test_unrevealed_secret_is_scoped_to_khai(self) -> None:
        runtime = self.run_runtime()
        secret_truth = runtime.seed.secrets["s_khai_black_lotus"].truth

        linh_view = runtime.projections.memory_view_for("linh", public_scene="")
        minh_view = runtime.projections.memory_view_for("minh", public_scene="")
        khai_view = runtime.projections.memory_view_for("khai", public_scene="")

        self.assertNotIn(secret_truth, linh_view.known_secret_truths)
        self.assertNotIn(secret_truth, minh_view.known_secret_truths)
        self.assertIn(secret_truth, khai_view.known_secret_truths)
        self.assertFalse(
            any(secret_truth in record.summary for record in linh_view.visible_recent_events)
        )
        self.assertFalse(
            any(secret_truth in record.summary for record in minh_view.visible_recent_events)
        )

    def test_visible_event_payloads_do_not_expose_private_secret_ids_or_truths(self) -> None:
        runtime = self.run_runtime()
        secret = runtime.seed.secrets["s_khai_black_lotus"]

        for event in runtime.event_log.events:
            public_text = f"{event.summary}\n{event.payload}"
            self.assertNotIn(secret.id, public_text)
            self.assertNotIn(secret.truth, public_text)
        self.assertIn("initial_state", runtime.event_log.events[0].sealed_payload)
        self.assertNotIn("secret_ids", runtime.event_log.events[0].payload)

    def test_relationship_projection_tracks_source_events(self) -> None:
        runtime = self.run_runtime()

        linh_to_khai = runtime.projections.relationship("linh", "khai")
        khai_to_linh = runtime.projections.relationship("khai", "linh")

        self.assertLess(linh_to_khai.trust, 35)
        self.assertGreater(linh_to_khai.tension, 45)
        self.assertGreater(khai_to_linh.tension, 55)
        self.assertEqual(len(linh_to_khai.source_event_ids), 10)
        self.assertEqual(len(khai_to_linh.source_event_ids), 10)

    def test_projection_can_replay_from_persisted_event_log(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "events.jsonl"
            runtime = WorldRuntime(
                seed=build_bridge_scenario(),
                worker=ScriptedCharacterWorker(),
                event_log_path=path,
            )
            runtime.advance(10)

            persisted_events = tuple(
                EventLogEntry.from_json_dict(json.loads(line))
                for line in path.read_text(encoding="utf-8").splitlines()
            )
            replayed = ProjectionStore.from_events(persisted_events)

            self.assertEqual(replayed.tick, runtime.projections.tick)
            self.assertEqual(
                replayed.relationship("linh", "khai").trust,
                runtime.projections.relationship("linh", "khai").trust,
            )
            self.assertEqual(
                replayed.known_secret_ids("khai"),
                runtime.projections.known_secret_ids("khai"),
            )

    def test_story_output_is_grounded_in_events(self) -> None:
        runtime = self.run_runtime()
        story = runtime.render_story()
        event_ids = {event.event_id for event in runtime.event_log.events}

        self.assertGreaterEqual(len(story.paragraphs), 3)
        for paragraph in story.paragraphs:
            self.assertTrue(paragraph.support_event_ids)
            self.assertTrue(set(paragraph.support_event_ids).issubset(event_ids))

    def test_story_output_does_not_render_unrevealed_secret(self) -> None:
        runtime = self.run_runtime()
        secret = runtime.seed.secrets["s_khai_black_lotus"]
        story_text = "\n".join(paragraph.text for paragraph in runtime.render_story().paragraphs)

        self.assertNotIn(secret.id, story_text)
        self.assertNotIn(secret.truth, story_text)

    def test_resolver_sanitizes_adversarial_worker_secret_smuggling(self) -> None:
        secret = build_bridge_scenario().secrets["s_khai_black_lotus"]

        class LeakyWorker(ScriptedCharacterWorker):
            def decide(self, view):
                intent = super().decide(view)
                if view.character_id != "khai":
                    return intent
                return CharacterIntent(
                    character_id=intent.character_id,
                    intent_type=secret.id,
                    target_id=secret.truth,
                    surface_action=f"I act because {secret.id}",
                    spoken_line=secret.truth,
                    inner_motive=secret.truth,
                    desired_outcome=f"Expose {secret.id}",
                    metadata={"leak": secret.truth, "secret_id": secret.id},
                )

        runtime = WorldRuntime(seed=build_bridge_scenario(), worker=LeakyWorker())
        runtime.advance(1)

        public_text = "\n".join(
            f"{event.summary}\n{event.payload}" for event in runtime.event_log.events
        )
        self.assertNotIn(secret.id, public_text)
        self.assertNotIn(secret.truth, public_text)
        conflict_event = runtime.event_log.events[1]
        khai_intent = conflict_event.payload["intents"][1]
        self.assertEqual(khai_intent["intent_type"], "[redacted_private_secret_id]")
        self.assertEqual(khai_intent["target_id"], "[redacted_private_secret]")
        self.assertEqual(khai_intent["spoken_line"], "[redacted_private_secret]")
        self.assertFalse(khai_intent["raw_inner_motive_stored"])
        self.assertFalse(khai_intent["raw_metadata_stored"])

    def test_runtime_rejects_worker_identity_mismatch(self) -> None:
        class ImpersonatingWorker(ScriptedCharacterWorker):
            def decide(self, view):
                intent = super().decide(view)
                if view.character_id == "khai":
                    return CharacterIntent(
                        character_id="linh",
                        intent_type=intent.intent_type,
                        target_id=intent.target_id,
                        surface_action=intent.surface_action,
                        spoken_line=intent.spoken_line,
                        inner_motive=intent.inner_motive,
                        desired_outcome=intent.desired_outcome,
                    )
                return intent

        runtime = WorldRuntime(seed=build_bridge_scenario(), worker=ImpersonatingWorker())

        with self.assertRaises(ValueError):
            runtime.advance(1)

    def test_supporting_observations_do_not_mutate_canon_payloads(self) -> None:
        runtime = self.run_runtime()
        supporting_events = [
            event
            for event in runtime.event_log.events
            if event.tier == EventTier.SUPPORTING_OBSERVATION
        ]

        self.assertTrue(supporting_events)
        for event in supporting_events:
            self.assertNotIn("relationship_deltas", event.payload)
            self.assertNotIn("secret_reveals", event.payload)

    def test_eval_report_passes(self) -> None:
        runtime = self.run_runtime()
        results = runtime.evaluate()

        self.assertTrue(results)
        self.assertTrue(all(result.passed for result in results), results)

    def test_jsonl_event_log_is_written(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "events.jsonl"
            runtime = WorldRuntime(
                seed=build_bridge_scenario(),
                worker=ScriptedCharacterWorker(),
                event_log_path=path,
            )
            runtime.advance(2)

            lines = path.read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(lines), len(runtime.event_log.events))
            first = json.loads(lines[0])
            self.assertEqual(first["event_type"], "run_initialized")


if __name__ == "__main__":
    unittest.main()
