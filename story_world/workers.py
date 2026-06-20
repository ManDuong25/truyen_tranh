from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import asdict
from json import JSONDecoder, JSONDecodeError
from typing import Protocol

from .models import CharacterIntent, CharacterMemoryView


class CharacterWorker(Protocol):
    def decide(self, view: CharacterMemoryView) -> CharacterIntent:
        ...


class OpenCodeExecutionError(RuntimeError):
    def __init__(
        self,
        message: str,
        *,
        stdout: str = "",
        stderr: str = "",
        returncode: int | None = None,
        error_name: str | None = None,
    ) -> None:
        super().__init__(message)
        self.stdout = stdout
        self.stderr = stderr
        self.returncode = returncode
        self.error_name = error_name

    def is_provider_unavailable(self) -> bool:
        text = f"{self.error_name or ''}\n{self}".lower()
        return any(
            marker in text
            for marker in (
                "providerautherror",
                "api key is missing",
                "unable to connect",
            "connection refused",
            "econnrefused",
            "timeoutexpired",
            "timed out",
        )
        )


class ScriptedCharacterWorker:
    """Deterministic worker used for tests and replayable acceptance runs."""

    def decide(self, view: CharacterMemoryView) -> CharacterIntent:
        character_id = view.character_id
        tick = view.tick + 1
        if character_id == "linh":
            return CharacterIntent(
                character_id="linh",
                intent_type="confront",
                target_id="khai",
                surface_action="presses Khai about her father",
                spoken_line=self._linh_line(tick),
                inner_motive="force the truth while hiding fear",
                desired_outcome="make Khai reveal what he knows",
            )
        if character_id == "khai":
            secret_known = "s_khai_black_lotus" in view.known_secret_ids
            motive = (
                "protect Linh while preserving the oath"
                if secret_known
                else "avoid making an unsafe claim"
            )
            return CharacterIntent(
                character_id="khai",
                intent_type="deflect",
                target_id="linh",
                surface_action="answers without revealing the oath",
                spoken_line=self._khai_line(tick),
                inner_motive=motive,
                desired_outcome="lower immediate danger without exposing the secret",
            )
        if character_id == "minh":
            return CharacterIntent(
                character_id="minh",
                intent_type="exploit",
                target_id="linh",
                surface_action="keeps hidden and listens for leverage",
                spoken_line="",
                inner_motive="learn enough to use Linh and Khai against each other",
                desired_outcome="gain leverage without being noticed",
            )
        raise ValueError(f"unknown scripted character {character_id}")

    def _linh_line(self, tick: int) -> str:
        if tick <= 2:
            return "Nếu anh biết chuyện về cha ta, đừng né tránh nữa."
        if tick <= 6:
            return "Mỗi lần anh im lặng, ta càng chắc anh đang che giấu điều gì đó."
        return "Ta không cần sự thương hại. Ta cần sự thật."

    def _khai_line(self, tick: int) -> str:
        if tick == 3:
            return "Có những chuyện nếu nói ra lúc này, người chết sẽ không chỉ có ta."
        if tick >= 7:
            return "Ta nợ nàng một lời giải thích, nhưng cây cầu này không phải nơi an toàn."
        return "Ta chỉ biết rằng đêm đó không đơn giản như lời đồn."


class OpenCodeCharacterWorker:
    """OpenCode-backed worker adapter. Not used by deterministic tests."""

    def __init__(
        self,
        *,
        agent: str,
        model: str | None = None,
        command: str = "opencode",
        timeout_seconds: int = 120,
        runner=subprocess.run,
    ) -> None:
        self.agent = agent
        self.model = model
        self.command = command
        self.timeout_seconds = timeout_seconds
        self.runner = runner

    def decide(self, view: CharacterMemoryView) -> CharacterIntent:
        prompt = self._build_prompt(view)
        executable = shutil.which(self.command) or self.command
        cmd = [executable, "run", "--format", "json", "--agent", self.agent]
        if self.model:
            cmd.extend(["--model", self.model])
        cmd.append(prompt)
        try:
            completed = self.runner(
                cmd,
                check=False,
                capture_output=True,
                text=True,
                timeout=self.timeout_seconds,
            )
        except FileNotFoundError as exc:
            raise OpenCodeExecutionError(
                f"OpenCode command not found: {self.command}",
                error_name=type(exc).__name__,
            ) from exc
        except subprocess.TimeoutExpired as exc:
            raise OpenCodeExecutionError(
                f"OpenCode command timed out after {exc.timeout} seconds.",
                stdout=exc.stdout or "",
                stderr=exc.stderr or "",
                error_name=type(exc).__name__,
            ) from exc
        if completed.returncode != 0:
            raise OpenCodeExecutionError(
                "OpenCode process exited with non-zero status.",
                stdout=completed.stdout,
                stderr=completed.stderr,
                returncode=completed.returncode,
            )
        return self._parse_intent(completed.stdout, stderr=completed.stderr)

    def _build_prompt(self, view: CharacterMemoryView) -> str:
        relationships = json.dumps(view.relationship_state, ensure_ascii=False)
        recent_events = json.dumps(
            [asdict(event) for event in view.visible_recent_events],
            ensure_ascii=False,
        )
        return (
            f"EXPECTED_CHARACTER_ID={view.character_id}\n"
            "Return exactly one JSON object and no other text.\n"
            f"Your JSON must start with: {{\"character_id\":\"{view.character_id}\",\n"
            "Required keys: character_id, intent_type, target_id, surface_action, "
            "spoken_line, inner_motive, desired_outcome, metadata.\n"
            "Valid intent_type examples: observe, confront, deflect, exploit, move, wait.\n"
            "Use null for target_id if there is no target.\n"
            "Context:\n"
            f"- run_id: {view.run_id}\n"
            f"- tick: {view.tick}\n"
            f"- character_name: {view.character_name}\n"
            f"- role: {view.role}\n"
            f"- public_description: {view.public_description}\n"
            f"- personality_traits: {list(view.personality_traits)}\n"
            f"- short_term_goal: {view.short_term_goal}\n"
            f"- long_term_goal: {view.long_term_goal}\n"
            f"- location: {view.location}\n"
            f"- scene: {view.public_scene}\n"
            f"- known_secret_ids: {list(view.known_secret_ids)}\n"
            f"- known_secret_truths: {list(view.known_secret_truths)}\n"
            f"- relationships: {relationships}\n"
            f"- recent_events: {recent_events}\n"
            "The context is complete enough for a first simulation tick. "
            "Choose a plausible active next character intent that advances the "
            "short_term_goal now. If the character has a tense relationship in "
            "the scene, prefer a concrete social intent such as confront, "
            "deflect, probe, reassure, hide, or exploit over generic observe. "
            "If relationships is not empty, target_id must be one of the "
            "relationship keys and the intent should address that target. "
            "Do not claim missing context. Avoid intent_type wait unless no "
            "action is possible.\n"
        )

    def _parse_intent(self, output: str, stderr: str = "") -> CharacterIntent:
        text_candidates: list[str] = []
        for line in output.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
            except JSONDecodeError:
                text_candidates.append(line)
                continue
            if isinstance(event, dict) and event.get("type") == "error":
                error = event.get("error", {})
                data = error.get("data", {}) if isinstance(error, dict) else {}
                message = data.get("message") or error.get("message") or "OpenCode error event."
                raise OpenCodeExecutionError(
                    message,
                    stdout=output,
                    stderr=stderr,
                    error_name=error.get("name") if isinstance(error, dict) else None,
                )
            intent = self._intent_from_payload(event)
            if intent is not None:
                return intent
            text_candidates.extend(self._collect_text(event))

        for candidate in [output, *text_candidates]:
            for payload in self._json_objects(candidate):
                intent = self._intent_from_payload(payload)
                if intent is not None:
                    return intent

        raise OpenCodeExecutionError(
            "OpenCode output did not contain a valid CharacterIntent JSON object.",
            stdout=output,
            stderr=stderr,
        )

    def _intent_from_payload(self, payload) -> CharacterIntent | None:
        if not isinstance(payload, dict):
            return None
        required = {
            "character_id",
            "intent_type",
            "target_id",
            "surface_action",
            "spoken_line",
            "inner_motive",
            "desired_outcome",
        }
        payload = {
            str(key).strip(): value for key, value in payload.items()
        }
        if not required.issubset(payload):
            return None
        metadata = payload.get("metadata", {})
        if metadata is None:
            metadata = {}
        if not isinstance(metadata, dict):
            raise OpenCodeExecutionError(
                "OpenCode returned malformed CharacterIntent metadata.",
                error_name="MalformedCharacterIntent",
            )
        return CharacterIntent(
            character_id=str(payload["character_id"]),
            intent_type=str(payload["intent_type"]),
            target_id=(
                None if payload.get("target_id") is None else str(payload["target_id"])
            ),
            surface_action=str(payload["surface_action"]),
            spoken_line=str(payload["spoken_line"]),
            inner_motive=str(payload["inner_motive"]),
            desired_outcome=str(payload["desired_outcome"]),
            metadata=dict(metadata),
        )

    def _json_objects(self, text: str):
        decoder = JSONDecoder()
        for index, char in enumerate(text):
            if char != "{":
                continue
            try:
                payload, _ = decoder.raw_decode(text[index:])
            except JSONDecodeError:
                continue
            yield payload

    def _collect_text(self, value) -> list[str]:
        if isinstance(value, str):
            return [value]
        if isinstance(value, list):
            collected: list[str] = []
            for item in value:
                collected.extend(self._collect_text(item))
            return collected
        if not isinstance(value, dict):
            return []
        collected = []
        for key in ("text", "content", "message", "delta", "output"):
            if key in value:
                collected.extend(self._collect_text(value[key]))
        for key, child in value.items():
            if key not in {"text", "content", "message", "delta", "output"}:
                collected.extend(self._collect_text(child))
        return collected
