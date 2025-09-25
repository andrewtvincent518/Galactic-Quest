"""Main game window for Galactic Quest."""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QMenuBar, QStatusBar, QMessageBox
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QAction, QFont, QKeySequence
from typing import Optional
import logging

from ..game import StoryManager, AudioManager
from .styles import DARK_THEME, WINDOW_CONFIG

logger = logging.getLogger(__name__)


class GalacticQuestWindow(QMainWindow):
    """Main window for the Galactic Quest game."""

    # Signals
    scene_changed = pyqtSignal(str)  # Emitted when scene changes
    choice_made = pyqtSignal(int)    # Emitted when player makes choice

    def __init__(self):
        """Initialize the main game window."""
        super().__init__()

        # Initialize managers
        self.story_manager = StoryManager()
        self.audio_manager = AudioManager()

        # UI components
        self.central_widget: Optional[QWidget] = None
        self.story_label: Optional[QLabel] = None
        self.choice_buttons: list[QPushButton] = []
        self.back_button: Optional[QPushButton] = None
        self.restart_button: Optional[QPushButton] = None

        # Setup UI
        self._setup_window()
        self._create_menu_bar()
        self._create_status_bar()
        self._create_central_widget()
        self._setup_shortcuts()

        # Connect signals
        self._connect_signals()

        # Initialize game state
        self._update_display()
        self._start_background_music()

    def _setup_window(self) -> None:
        """Configure the main window."""
        self.setWindowTitle(WINDOW_CONFIG["title"])
        self.setMinimumSize(WINDOW_CONFIG["min_width"], WINDOW_CONFIG["min_height"])
        self.resize(WINDOW_CONFIG["default_width"], WINDOW_CONFIG["default_height"])

        # Apply dark theme
        self.setStyleSheet(DARK_THEME)

    def _create_menu_bar(self) -> None:
        """Create the application menu bar."""
        menubar = self.menuBar()

        # Game menu
        game_menu = menubar.addMenu("&Game")

        restart_action = QAction("&Restart", self)
        restart_action.setShortcut(QKeySequence("Ctrl+R"))
        restart_action.triggered.connect(self.restart_game)
        game_menu.addAction(restart_action)

        game_menu.addSeparator()

        exit_action = QAction("E&xit", self)
        exit_action.setShortcut(QKeySequence("Ctrl+Q"))
        exit_action.triggered.connect(self.close)
        game_menu.addAction(exit_action)

        # Audio menu
        audio_menu = menubar.addMenu("&Audio")

        toggle_music_action = QAction("&Toggle Music", self)
        toggle_music_action.setShortcut(QKeySequence("Ctrl+M"))
        toggle_music_action.triggered.connect(self.toggle_music)
        audio_menu.addAction(toggle_music_action)

    def _create_status_bar(self) -> None:
        """Create the status bar."""
        status_bar = self.statusBar()
        status_bar.showMessage("Welcome to Galactic Quest!")

    def _create_central_widget(self) -> None:
        """Create the central widget and layout."""
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Main layout
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Story text label
        self.story_label = QLabel()
        self.story_label.setObjectName("story-text")
        self.story_label.setWordWrap(True)
        self.story_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        font = QFont()
        font.setPointSize(12)
        self.story_label.setFont(font)
        main_layout.addWidget(self.story_label)

        # Choices layout
        self.choices_layout = QVBoxLayout()
        self.choices_layout.setSpacing(8)
        main_layout.addLayout(self.choices_layout)

        # Control buttons layout
        controls_layout = QHBoxLayout()

        self.back_button = QPushButton("← Back")
        self.back_button.setObjectName("back-button")
        self.back_button.clicked.connect(self.go_back)
        self.back_button.setEnabled(False)
        controls_layout.addWidget(self.back_button)

        controls_layout.addStretch()

        self.restart_button = QPushButton("Restart")
        self.restart_button.setObjectName("restart-button")
        self.restart_button.clicked.connect(self.restart_game)
        controls_layout.addWidget(self.restart_button)

        main_layout.addLayout(controls_layout)

    def _setup_shortcuts(self) -> None:
        """Setup keyboard shortcuts."""
        # Number keys 1-9 for choices
        for i in range(1, 10):
            shortcut = QKeySequence(f"{i}")
            action = QAction(self)
            action.setShortcut(shortcut)
            action.triggered.connect(lambda checked, idx=i-1: self._make_choice(idx))
            self.addAction(action)

    def _connect_signals(self) -> None:
        """Connect internal signals."""
        self.scene_changed.connect(self._on_scene_changed)
        self.choice_made.connect(self._on_choice_made)

    def _update_display(self) -> None:
        """Update the display with current scene."""
        scene = self.story_manager.get_current_scene()

        # Update story text
        if self.story_manager.current_scene == "start":
            text = self.story_manager.get_intro_text()
        else:
            text = scene.text

        self.story_label.setText(text)

        # Clear existing choice buttons
        self._clear_choice_buttons()

        # Add new choice buttons
        for i, choice in enumerate(scene.choices):
            button = QPushButton(f"{i+1}. {choice.text}")
            button.clicked.connect(lambda checked, idx=i: self._make_choice(idx))
            self.choices_layout.addWidget(button)
            self.choice_buttons.append(button)

        # Update back button
        self.back_button.setEnabled(self.story_manager.can_go_back())

        # Update status bar
        if scene.is_ending:
            if scene.outcome == "success":
                self.statusBar().showMessage("Mission accomplished! 🚀")
            elif scene.outcome == "failure":
                self.statusBar().showMessage("Mission failed... Try again?")
            else:
                self.statusBar().showMessage("Journey complete.")
        else:
            choices_count = len(scene.choices)
            self.statusBar().showMessage(f"Choose your path... ({choices_count} options)")

    def _clear_choice_buttons(self) -> None:
        """Clear all choice buttons from the layout."""
        while self.choice_buttons:
            button = self.choice_buttons.pop()
            self.choices_layout.removeWidget(button)
            button.deleteLater()

    def _make_choice(self, choice_index: int) -> None:
        """Handle player choice."""
        scene = self.story_manager.get_current_scene()

        if 0 <= choice_index < len(scene.choices):
            success = self.story_manager.make_choice(choice_index)
            if success:
                self.choice_made.emit(choice_index)
                self._update_display()
                self.scene_changed.emit(self.story_manager.current_scene)

    def _start_background_music(self) -> None:
        """Start background music."""
        success = self.audio_manager.load_background_music()
        if success:
            self.audio_manager.play_background_music()
            logger.info("Background music started")
        else:
            logger.warning("Could not start background music")

    def go_back(self) -> None:
        """Go back to the previous scene."""
        if self.story_manager.go_back():
            self._update_display()
            self.scene_changed.emit(self.story_manager.current_scene)

    def restart_game(self) -> None:
        """Restart the game from the beginning."""
        reply = QMessageBox.question(
            self,
            "Restart Game",
            "Are you sure you want to restart the game?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.story_manager.reset()
            self._update_display()
            self.statusBar().showMessage("Game restarted!")
            self.scene_changed.emit(self.story_manager.current_scene)

    def toggle_music(self) -> None:
        """Toggle background music on/off."""
        if self.audio_manager.is_playing():
            self.audio_manager.stop_music()
            self.statusBar().showMessage("Music stopped", 2000)
        else:
            if self.audio_manager.play_background_music():
                self.statusBar().showMessage("Music started", 2000)
            else:
                self.statusBar().showMessage("Could not start music", 2000)

    def closeEvent(self, event) -> None:
        """Handle window close event."""
        self.audio_manager.cleanup()
        super().closeEvent(event)

    def _on_scene_changed(self, scene_id: str) -> None:
        """Handle scene change signal."""
        logger.debug(f"Scene changed to: {scene_id}")

    def _on_choice_made(self, choice_index: int) -> None:
        """Handle choice made signal."""
        logger.debug(f"Choice made: {choice_index}")