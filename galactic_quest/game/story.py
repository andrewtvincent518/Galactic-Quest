"""Story management for Galactic Quest."""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)


class Choice:
    """Represents a choice in the story."""

    def __init__(self, text: str, next_scene: str):
        self.text = text
        self.next_scene = next_scene


class Scene:
    """Represents a scene in the story."""

    def __init__(
        self,
        text: str,
        choices: List[Choice],
        is_ending: bool = False,
        outcome: Optional[str] = None
    ):
        self.text = text
        self.choices = choices
        self.is_ending = is_ending
        self.outcome = outcome


class StoryManager:
    """Manages the story data and progression."""

    def __init__(self, story_file: Optional[Path] = None):
        """Initialize the story manager.

        Args:
            story_file: Path to the story JSON file. If None, uses default.
        """
        self.scenes: Dict[str, Scene] = {}
        self.background = ""
        self.introduction = ""
        self.current_scene = "start"
        self.choice_history: List[str] = []

        if story_file is None:
            story_file = Path(__file__).parent.parent / "data" / "story.json"

        self._load_story(story_file)

    def _load_story(self, story_file: Path) -> None:
        """Load story data from JSON file."""
        try:
            with open(story_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self.background = data.get("background", "")
            self.introduction = data.get("introduction", "")

            # Parse scenes
            for scene_id, scene_data in data.get("scenes", {}).items():
                choices = [
                    Choice(choice["text"], choice["next"])
                    for choice in scene_data.get("choices", [])
                ]

                scene = Scene(
                    text=scene_data.get("text", ""),
                    choices=choices,
                    is_ending=scene_data.get("ending", False),
                    outcome=scene_data.get("outcome")
                )

                self.scenes[scene_id] = scene

        except FileNotFoundError:
            logger.error(f"Story file not found: {story_file}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in story file: {e}")
            raise
        except Exception as e:
            logger.error(f"Error loading story: {e}")
            raise

    def get_current_scene(self) -> Scene:
        """Get the current scene."""
        return self.scenes.get(self.current_scene, self.scenes["start"])

    def make_choice(self, choice_index: int) -> bool:
        """Make a choice and advance to the next scene.

        Args:
            choice_index: Index of the chosen option

        Returns:
            True if the choice was valid and scene changed, False otherwise
        """
        current = self.get_current_scene()

        if 0 <= choice_index < len(current.choices):
            choice = current.choices[choice_index]
            self.choice_history.append(f"{self.current_scene}:{choice.text}")
            self.current_scene = choice.next_scene
            return True

        return False

    def can_go_back(self) -> bool:
        """Check if player can go back to previous scene."""
        return len(self.choice_history) > 0

    def go_back(self) -> bool:
        """Go back to the previous scene.

        Returns:
            True if successfully went back, False otherwise
        """
        if not self.can_go_back():
            return False

        # Remove last choice and extract previous scene
        last_choice = self.choice_history.pop()
        scene_id = last_choice.split(':')[0]
        self.current_scene = scene_id
        return True

    def reset(self) -> None:
        """Reset the story to the beginning."""
        self.current_scene = "start"
        self.choice_history.clear()

    def get_intro_text(self) -> str:
        """Get the introduction text for the game."""
        return f"{self.background}\n\n{self.introduction}"