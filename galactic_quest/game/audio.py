"""Audio management for Galactic Quest."""

import pygame
from pathlib import Path
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class AudioManager:
    """Manages audio playback for the game."""

    def __init__(self):
        """Initialize the audio manager."""
        self.initialized = False
        self.music_loaded = False
        self._init_pygame()

    def _init_pygame(self) -> None:
        """Initialize pygame mixer."""
        try:
            pygame.mixer.init()
            self.initialized = True
            logger.info("Audio system initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize audio: {e}")
            self.initialized = False

    def load_background_music(self, music_file: Optional[Path] = None) -> bool:
        """Load background music file.

        Args:
            music_file: Path to music file. If None, uses default.

        Returns:
            True if music loaded successfully, False otherwise
        """
        if not self.initialized:
            logger.warning("Audio system not initialized")
            return False

        if music_file is None:
            # Look for music file in project root
            music_file = Path("surveillance.mp3")

        if not music_file.exists():
            logger.warning(f"Music file not found: {music_file}")
            return False

        try:
            pygame.mixer.music.load(str(music_file))
            self.music_loaded = True
            logger.info(f"Background music loaded: {music_file}")
            return True
        except Exception as e:
            logger.error(f"Failed to load music: {e}")
            return False

    def play_background_music(self, loops: int = -1) -> bool:
        """Play background music.

        Args:
            loops: Number of times to loop (-1 for infinite)

        Returns:
            True if music started playing, False otherwise
        """
        if not self.initialized or not self.music_loaded:
            logger.warning("Audio not ready for playback")
            return False

        try:
            pygame.mixer.music.play(loops)
            logger.info("Background music started")
            return True
        except Exception as e:
            logger.error(f"Failed to play music: {e}")
            return False

    def stop_music(self) -> None:
        """Stop background music."""
        if self.initialized:
            try:
                pygame.mixer.music.stop()
                logger.info("Background music stopped")
            except Exception as e:
                logger.error(f"Error stopping music: {e}")

    def set_volume(self, volume: float) -> None:
        """Set music volume.

        Args:
            volume: Volume level (0.0 to 1.0)
        """
        if self.initialized:
            try:
                volume = max(0.0, min(1.0, volume))  # Clamp to valid range
                pygame.mixer.music.set_volume(volume)
                logger.debug(f"Volume set to {volume}")
            except Exception as e:
                logger.error(f"Error setting volume: {e}")

    def is_playing(self) -> bool:
        """Check if music is currently playing."""
        if not self.initialized:
            return False

        try:
            return pygame.mixer.music.get_busy()
        except Exception:
            return False

    def cleanup(self) -> None:
        """Clean up audio resources."""
        if self.initialized:
            try:
                pygame.mixer.music.stop()
                pygame.mixer.quit()
                logger.info("Audio system cleaned up")
            except Exception as e:
                logger.error(f"Error during audio cleanup: {e}")