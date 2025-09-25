"""Main entry point for Galactic Quest."""

import sys
import logging
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

from .ui import GalacticQuestWindow
from .game import AudioManager


def setup_logging() -> None:
    """Setup application logging."""
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout),
        ]
    )

    # Set specific log levels for noisy modules
    logging.getLogger("pygame").setLevel(logging.WARNING)


def main() -> int:
    """Main application entry point."""
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)

    try:
        # Create QApplication
        app = QApplication(sys.argv)
        app.setApplicationName("Galactic Quest")
        app.setApplicationVersion("1.0.0")
        app.setOrganizationName("Andrew Vincent")

        # Enable high DPI scaling (automatic in PyQt6)
        app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)

        logger.info("Starting Galactic Quest...")

        # Create and show main window
        window = GalacticQuestWindow()
        window.show()

        # Start event loop
        return app.exec()

    except Exception as e:
        logger.critical(f"Critical error: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())