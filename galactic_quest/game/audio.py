"""Audio management for Galactic Quest."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

try:  # pragma: no cover - depends on optional dependency
    import pygame
except Exception as exc:  # pragma: no cover - handled at runtime
    pygame = None  # type: ignore[assignment]
    _PYGAME_IMPORT_ERROR = exc
else:  # pragma: no cover - depends on optional dependency
    _PYGAME_IMPORT_ERROR = None

logger = logging.getLogger(__name__)


class AudioManager:
    """Manages audio playback for the game."""

    def __init__(self, *, default_volume: float = 0.6) -> None:
        self.initialized: bool = False
        self.music_loaded: bool = False
        self._enabled: bool = True
        self._volume: float = self._clamp_volume(default_volume)
        self._music_file: Optional[Path] = None
        self._init_error: Optional[Exception] = None
        self._init_pygame()

    @staticmethod
    def _clamp_volume(volume: float) -> float:
        return max(0.0, min(1.0, volume))

    def _init_pygame(self) -> None:
        """Initialize pygame mixer if available."""

        if pygame is None:  # pragma: no cover - optional dependency
            self._init_error = _PYGAME_IMPORT_ERROR
            logger.warning("pygame is not available: %s", self._init_error)
            return

        try:
            pygame.mixer.init()
            pygame.mixer.music.set_volume(self._volume)
            self.initialized = True
            logger.info("Audio system initialized successfully")
        except Exception as exc:  # pragma: no cover - depends on mixer backend
            self._init_error = exc
            logger.error("Failed to initialize audio: %s", exc)
            self.initialized = False

    # ------------------------------------------------------------------
    # Music loading & playback
    # ------------------------------------------------------------------
    def _default_music_path(self) -> Optional[Path]:
        """Return the default background music path if it exists."""

        package_root = Path(__file__).resolve().parent.parent
        candidates = [
            package_root.parent / "surveillance.mp3",
            package_root / "data" / "surveillance.mp3",
        ]

        for candidate in candidates:
            if candidate.exists():
                return candidate
        return None

    def load_background_music(self, music_file: Optional[Path] = None) -> bool:
        """Load background music file."""

        if not self.initialized:
            logger.warning("Audio system not initialized")
            return False

        if music_file is None:
            music_file = self._default_music_path()
            if music_file is None:
                logger.warning("No background music file found")
                return False

        if not music_file.exists():
            logger.warning("Music file not found: %s", music_file)
            return False

        try:
            pygame.mixer.music.load(str(music_file))
            self._music_file = music_file
            self.music_loaded = True
            logger.info("Background music loaded: %s", music_file)
            return True
        except Exception as exc:  # pragma: no cover - depends on mixer backend
            logger.error("Failed to load music: %s", exc)
            return False

    def play_background_music(self, loops: int = -1) -> bool:
        """Play background music."""

        if not self.initialized or not self.music_loaded:
            logger.warning("Audio not ready for playback")
            return False

        if not self._enabled:
            logger.debug("Music playback suppressed because audio is disabled")
            return False

        try:
            pygame.mixer.music.play(loops)
            logger.info("Background music started")
            return True
        except Exception as exc:  # pragma: no cover - depends on mixer backend
            logger.error("Failed to play music: %s", exc)
            return False

    def stop_music(self) -> None:
        """Stop background music."""

        if self.initialized:
            try:
                pygame.mixer.music.stop()
                logger.info("Background music stopped")
            except Exception as exc:  # pragma: no cover - depends on mixer backend
                logger.error("Error stopping music: %s", exc)

    def toggle_enabled(self) -> bool:
        """Toggle whether music playback is enabled."""

        self.set_enabled(not self._enabled)
        return self._enabled

    def set_enabled(self, enabled: bool) -> None:
        """Enable or disable audio playback."""

        self._enabled = bool(enabled)
        if not self._enabled:
            self.stop_music()
        elif self.music_loaded and not self.is_playing():
            self.play_background_music()

    def is_enabled(self) -> bool:
        """Return ``True`` if audio playback is enabled."""

        return self._enabled

    def set_volume(self, volume: float) -> None:
        """Set music volume."""

        self._volume = self._clamp_volume(volume)
        if self.initialized:
            try:
                pygame.mixer.music.set_volume(self._volume)
                logger.debug("Volume set to %.2f", self._volume)
            except Exception as exc:  # pragma: no cover - depends on mixer backend
                logger.error("Error setting volume: %s", exc)

    def is_playing(self) -> bool:
        """Check if music is currently playing."""

        if not self.initialized or pygame is None:
            return False

        try:
            return pygame.mixer.music.get_busy()
        except Exception:  # pragma: no cover - depends on mixer backend
            return False

    def cleanup(self) -> None:
        """Clean up audio resources."""

        if self.initialized and pygame is not None:
            try:
                pygame.mixer.music.stop()
                pygame.mixer.quit()
                logger.info("Audio system cleaned up")
            except Exception as exc:  # pragma: no cover - depends on mixer backend
                logger.error("Error during audio cleanup: %s", exc)
