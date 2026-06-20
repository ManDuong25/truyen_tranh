from __future__ import annotations

import json
import subprocess
import unittest

from story_world.projections import ProjectionStore
from story_world.scenarios import build_bridge_scenario
from story_world.workers import OpenCodeCharacterWorker, OpenCodeExecutionError


class OpenCodeWorkerTests(unittest.TestCase):
    def memory_view(self):
        seed = build_bridge_scenario()
        return ProjectionStore(seed).memory_view_for("linh", public_scene=seed.premise)

    def test_parse_direct_intent_json(self) -> None:
        worker = OpenCodeCharacterWorker(agent="build")
        output = json.dumps(
            {
                "character_id": "linh",
                "intent_type": "observe",
                "target_id": "khai",
                "surface_action": "watches Khai",
                "spoken_line": "",
                "inner_motive": "test motive",
                "desired_outcome": "understand what Khai hides",
                "metadata": {"source": "test"},
            }
        )

        intent = worker._parse_intent(output)

        self.assertEqual(intent.character_id, "linh")
        self.assertEqual(intent.intent_type, "observe")
        self.assertEqual(intent.metadata["source"], "test")

    def test_parse_intent_embedded_in_opencode_message_event(self) -> None:
        worker = OpenCodeCharacterWorker(agent="build")
        intent_json = json.dumps(
            {
                "character_id": "linh",
                "intent_type": "confront",
                "target_id": "khai",
                "surface_action": "asks one careful question",
                "spoken_line": "Anh đang giấu gì?",
                "inner_motive": "test motive",
                "desired_outcome": "pressure Khai without overcommitting",
                "metadata": {},
            },
            ensure_ascii=False,
        )
        output = json.dumps(
            {
                "type": "message",
                "message": {"content": [{"type": "text", "text": intent_json}]},
            },
            ensure_ascii=False,
        )

        intent = worker._parse_intent(output)

        self.assertEqual(intent.intent_type, "confront")
        self.assertEqual(intent.spoken_line, "Anh đang giấu gì?")

    def test_parse_intent_embedded_in_opencode_part_text_event(self) -> None:
        worker = OpenCodeCharacterWorker(agent="story-character-intent")
        intent_json = json.dumps(
            {
                "character_id": "linh",
                "intent_type": "observe",
                "target_id": None,
                "surface_action": "listens under the rain",
                "spoken_line": "",
                "inner_motive": "avoid exposing fear",
                "desired_outcome": "learn what Khai avoids",
                "metadata": {},
            }
        )
        output = json.dumps(
            {
                "type": "text",
                "part": {"type": "text", "text": intent_json},
            }
        )

        intent = worker._parse_intent(output)

        self.assertEqual(intent.character_id, "linh")
        self.assertEqual(intent.intent_type, "observe")

    def test_opencode_error_event_raises_typed_error(self) -> None:
        worker = OpenCodeCharacterWorker(agent="build")
        output = json.dumps(
            {
                "type": "error",
                "error": {
                    "name": "ProviderAuthError",
                    "data": {"message": "OpenAI API key is missing."},
                },
            }
        )

        with self.assertRaises(OpenCodeExecutionError) as ctx:
            worker._parse_intent(output)

        self.assertEqual(ctx.exception.error_name, "ProviderAuthError")
        self.assertTrue(ctx.exception.is_provider_unavailable())

    def test_timeout_raises_typed_provider_unavailable_error(self) -> None:
        def timeout_runner(cmd, **kwargs):
            raise subprocess.TimeoutExpired(cmd=cmd, timeout=kwargs["timeout"])

        worker = OpenCodeCharacterWorker(agent="build", runner=timeout_runner)

        with self.assertRaises(OpenCodeExecutionError) as ctx:
            worker.decide(self.memory_view())

        self.assertEqual(ctx.exception.error_name, "TimeoutExpired")
        self.assertTrue(ctx.exception.is_provider_unavailable())

    def test_null_metadata_is_accepted_as_empty_dict(self) -> None:
        worker = OpenCodeCharacterWorker(agent="build")
        output = json.dumps(
            {
                "character_id": "linh",
                "intent_type": "observe",
                "target_id": None,
                "surface_action": "listens",
                "spoken_line": "",
                "inner_motive": "stay cautious",
                "desired_outcome": "learn safely",
                "metadata": None,
            }
        )

        intent = worker._parse_intent(output)

        self.assertEqual(intent.metadata, {})

    def test_malformed_metadata_raises_typed_error(self) -> None:
        worker = OpenCodeCharacterWorker(agent="build")
        output = json.dumps(
            {
                "character_id": "linh",
                "intent_type": "observe",
                "target_id": None,
                "surface_action": "listens",
                "spoken_line": "",
                "inner_motive": "stay cautious",
                "desired_outcome": "learn safely",
                "metadata": "not-a-dict",
            }
        )

        with self.assertRaises(OpenCodeExecutionError) as ctx:
            worker._parse_intent(output)

        self.assertEqual(ctx.exception.error_name, "MalformedCharacterIntent")

    def test_decide_invokes_opencode_with_scoped_json_mode(self) -> None:
        calls = []

        def fake_runner(cmd, **kwargs):
            calls.append((cmd, kwargs))
            return subprocess.CompletedProcess(
                cmd,
                0,
                stdout=json.dumps(
                    {
                        "character_id": "linh",
                        "intent_type": "observe",
                        "target_id": None,
                        "surface_action": "listens",
                        "spoken_line": "",
                        "inner_motive": "stay cautious",
                        "desired_outcome": "learn safely",
                        "metadata": {},
                    }
                ),
                stderr="",
            )

        worker = OpenCodeCharacterWorker(
            agent="story-character-intent",
            model="opencode/deepseek-v4-flash-free",
            runner=fake_runner,
        )
        intent = worker.decide(self.memory_view())

        self.assertEqual(intent.intent_type, "observe")
        cmd, kwargs = calls[0]
        self.assertTrue(cmd[0].lower().endswith(("opencode", "opencode.cmd")))
        self.assertEqual(cmd[1:5], ["run", "--format", "json", "--agent"])
        self.assertIn("story-character-intent", cmd)
        self.assertIn("--model", cmd)
        self.assertFalse(kwargs["check"])
        self.assertTrue(kwargs["capture_output"])

    def test_missing_opencode_command_is_typed_error(self) -> None:
        worker = OpenCodeCharacterWorker(
            agent="build",
            command="definitely-missing-opencode",
        )

        with self.assertRaises(OpenCodeExecutionError) as ctx:
            worker.decide(self.memory_view())

        self.assertEqual(ctx.exception.error_name, "FileNotFoundError")


if __name__ == "__main__":
    unittest.main()
