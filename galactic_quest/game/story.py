"""Story management for Galactic Quest."""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from importlib import resources
from pathlib import Path
from typing import Iterable, Iterator, Mapping, MutableMapping, Optional

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class Choice:
    """Represents a choice in the story."""

    text: str
    next_scene: str


@dataclass(frozen=True, slots=True)
class Scene:
    """Represents a scene in the story."""

    text: str
    choices: tuple[Choice, ...] = field(default_factory=tuple)
    is_ending: bool = False
    outcome: Optional[str] = None

    @classmethod
    def from_mapping(cls, mapping: Mapping[str, object]) -> "Scene":
        """Create a :class:`Scene` from a mapping loaded from JSON."""

        raw_choices = mapping.get("choices", [])
        choices: list[Choice] = []
        if isinstance(raw_choices, Iterable):
            for raw_choice in raw_choices:
                if not isinstance(raw_choice, Mapping):
                    continue
                text = str(raw_choice.get("text", ""))
                next_scene = str(raw_choice.get("next", ""))
                choices.append(Choice(text=text, next_scene=next_scene))

        return cls(
            text=str(mapping.get("text", "")),
            choices=tuple(choices),
            is_ending=bool(mapping.get("ending", False)),
            outcome=str(mapping.get("outcome")) if mapping.get("outcome") else None,
        )


@dataclass(frozen=True, slots=True)
class HistoryEntry:
    """Represents a choice made by the player."""

    scene_id: str
    choice_index: int
    choice_text: str
    next_scene: str


class StoryManager:
    """Manages the story data and progression."""

    DEFAULT_STORY = resources.files("galactic_quest.data").joinpath("story.json")

    def __init__(self, story_file: Optional[Path] = None) -> None:
        """Initialize the story manager.

        Args:
            story_file: Optional path to the story JSON file. When ``None`` the
                bundled story file distributed with the package is used.
        """

        self.scenes: dict[str, Scene] = {}
        self.background: str = ""
        self.introduction: str = ""
        self._current_scene: str = "start"
        self._history: list[HistoryEntry] = []

        story_path = self._resolve_story_path(story_file)
        self._load_story(story_path)

    @property
    def current_scene(self) -> str:
        """Return the identifier of the current scene."""

        return self._current_scene

    def _resolve_story_path(self, story_file: Optional[Path]) -> Path:
        """Resolve the absolute path to the story file."""

        if story_file is not None:
            return story_file

        try:
            with resources.as_file(self.DEFAULT_STORY) as resolved:
                return resolved
        except FileNotFoundError as exc:  # pragma: no cover - defensive guard
            logger.error("Bundled story file is missing: %s", exc)
            raise

    def _load_story(self, story_file: Path) -> None:
        """Load story data from JSON file."""

        try:
            raw_data = story_file.read_text(encoding="utf-8")
            data = json.loads(raw_data)
        except FileNotFoundError:
            logger.error("Story file not found: %s", story_file)
            raise
        except json.JSONDecodeError as exc:
            logger.error("Invalid JSON in story file: %s", exc)
            raise

        scenes_data = data.get("scenes", {})
        if not isinstance(scenes_data, MutableMapping):
            raise ValueError("Story data must contain a 'scenes' mapping")

        self.background = str(data.get("background", ""))
        self.introduction = str(data.get("introduction", ""))

        parsed_scenes: dict[str, Scene] = {}
        for scene_id, scene_mapping in scenes_data.items():
            if not isinstance(scene_mapping, Mapping):
                logger.warning("Skipping invalid scene definition: %s", scene_id)
                continue
            parsed_scenes[str(scene_id)] = Scene.from_mapping(scene_mapping)

        if "start" not in parsed_scenes:
            raise ValueError("Story must define a 'start' scene")

        self.scenes = parsed_scenes
        self._current_scene = "start"
        self._history.clear()

    def get_scene(self, scene_id: str) -> Scene:
        """Return the :class:`Scene` identified by ``scene_id``."""

        try:
            return self.scenes[scene_id]
        except KeyError:
            logger.error("Unknown scene requested: %s", scene_id)
            raise

    def get_current_scene(self) -> Scene:
        """Return the current scene."""

        return self.get_scene(self._current_scene)

    def iter_history(self) -> Iterator[HistoryEntry]:
        """Iterate over the history of choices made by the player."""

        return iter(self._history)

    def make_choice(self, choice_index: int) -> bool:
        """Make a choice and advance to the next scene.

        Args:
            choice_index: Index of the chosen option.

        Returns:
            ``True`` if the choice was valid and the scene changed, ``False``
            otherwise.
        """

        scene = self.get_current_scene()
        if not (0 <= choice_index < len(scene.choices)):
            return False

        choice = scene.choices[choice_index]
        if choice.next_scene not in self.scenes:
            logger.error(
                "Scene '%s' references unknown next scene '%s'",
                self._current_scene,
                choice.next_scene,
            )
            return False

        self._history.append(
            HistoryEntry(
                scene_id=self._current_scene,
                choice_index=choice_index,
                choice_text=choice.text,
                next_scene=choice.next_scene,
            )
        )
        self._current_scene = choice.next_scene
        return True

    def can_go_back(self) -> bool:
        """Return ``True`` if the player can go back to a previous scene."""

        return bool(self._history)

    def go_back(self) -> bool:
        """Go back to the previous scene if possible."""

        if not self._history:
            return False

        last_entry = self._history.pop()
        self._current_scene = last_entry.scene_id
        return True

    def reset(self) -> None:
        """Reset the story to the beginning."""

        self._current_scene = "start"
        self._history.clear()

    def get_intro_text(self) -> str:
        """Return the introduction text for the game."""

        return f"{self.background}\n\n{self.introduction}".strip()

    def get_available_choices(self) -> tuple[Choice, ...]:
        """Return the choices available in the current scene."""

        return self.get_current_scene().choices

    def jump_to_scene(self, scene_id: str) -> None:
        """Jump to an arbitrary scene, clearing future history."""

        if scene_id not in self.scenes:
            raise KeyError(f"Unknown scene: {scene_id}")

        while self._history and self._history[-1].next_scene != scene_id:
            self._history.pop()

        self._current_scene = scene_id
