"""Main game window for Galactic Quest."""

from __future__ import annotations

import logging
from typing import Optional

from PyQt6.QtCore import Qt, QSettings, pyqtSignal
from PyQt6.QtGui import QAction, QFont, QKeySequence
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)

from ..game import AudioManager, HistoryEntry, StoryManager
from .styles import DARK_THEME, WINDOW_CONFIG

logger = logging.getLogger(__name__)


class GalacticQuestWindow(QMainWindow):
    """Main window for the Galactic Quest game."""

    # Signals
    scene_changed = pyqtSignal(str)  # Emitted when scene changes
    choice_made = pyqtSignal(int)  # Emitted when player makes choice

    def __init__(self) -> None:
        """Initialize the main game window."""
        super().__init__()

        # Initialize managers
        self.story_manager = StoryManager()
        self.audio_manager = AudioManager()
        self.settings = QSettings()

        # UI components
        self.central_widget: Optional[QWidget] = None
        self.story_label: Optional[QLabel] = None
        self.choice_buttons: list[QPushButton] = []
        self.back_button: Optional[QPushButton] = None
        self.restart_button: Optional[QPushButton] = None
        self.history_group: Optional[QGroupBox] = None
        self.history_list: Optional[QListWidget] = None
        self.toggle_music_action: Optional[QAction] = None
        self.toggle_history_action: Optional[QAction] = None
        self._history_visible: bool = True

        # Setup UI
        self._setup_window()
        self._create_menu_bar()
        self._create_status_bar()
        self._create_central_widget()
        self._setup_shortcuts()

        # Load persisted configuration
        self._load_settings()

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

        self.toggle_music_action = QAction("Enable &Music", self)
        self.toggle_music_action.setCheckable(True)
        self.toggle_music_action.toggled.connect(self.toggle_music)
        audio_menu.addAction(self.toggle_music_action)

        # View menu
        view_menu = menubar.addMenu("&View")

        self.toggle_history_action = QAction("Show Mission &Log", self)
        self.toggle_history_action.setCheckable(True)
        self.toggle_history_action.toggled.connect(self.toggle_history_panel)
        view_menu.addAction(self.toggle_history_action)

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

        # Mission log
        self.history_group = QGroupBox("Mission Log")
        history_layout = QVBoxLayout(self.history_group)
        self.history_list = QListWidget()
        self.history_list.setObjectName("history-list")
        self.history_list.setUniformItemSizes(True)
        self.history_list.setAlternatingRowColors(True)
        self.history_list.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.history_list.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        history_layout.addWidget(self.history_list)
        main_layout.addWidget(self.history_group)

    def _setup_shortcuts(self) -> None:
        """Setup keyboard shortcuts."""
        # Number keys 1-9 for choices
        for i in range(1, 10):
            shortcut = QKeySequence(f"{i}")
            action = QAction(self)
            action.setShortcut(shortcut)
            action.triggered.connect(lambda checked, idx=i - 1: self._make_choice(idx))
            self.addAction(action)

        back_action = QAction(self)
        back_action.setShortcut(QKeySequence("Ctrl+Z"))
        back_action.triggered.connect(self.go_back)
        self.addAction(back_action)

        toggle_log_action = QAction(self)
        toggle_log_action.setShortcut(QKeySequence("Ctrl+L"))
        toggle_log_action.triggered.connect(self._trigger_history_toggle)
        self.addAction(toggle_log_action)

        music_shortcut = QAction(self)
        music_shortcut.setShortcut(QKeySequence("Ctrl+M"))
        music_shortcut.triggered.connect(self._trigger_music_toggle)
        self.addAction(music_shortcut)

    def _connect_signals(self) -> None:
        """Connect internal signals."""
        self.scene_changed.connect(self._on_scene_changed)
        self.choice_made.connect(self._on_choice_made)

    def _load_settings(self) -> None:
        """Load persisted UI and audio settings."""

        width = self.settings.value(
            "window/width", WINDOW_CONFIG["default_width"], type=int
        )
        height = self.settings.value(
            "window/height", WINDOW_CONFIG["default_height"], type=int
        )
        self.resize(width, height)

        pos_x = self.settings.value("window/x", None, type=int)
        pos_y = self.settings.value("window/y", None, type=int)
        if pos_x is not None and pos_y is not None:
            self.move(pos_x, pos_y)

        self._history_visible = self.settings.value(
            "ui/history_visible", True, type=bool
        )
        if self.toggle_history_action is not None:
            self.toggle_history_action.blockSignals(True)
            self.toggle_history_action.setChecked(self._history_visible)
            self.toggle_history_action.blockSignals(False)

        if self.history_group is not None:
            self.history_group.setVisible(self._history_visible)

        music_enabled = self.settings.value("audio/enabled", True, type=bool)
        if self.toggle_music_action is not None:
            self.toggle_music_action.blockSignals(True)
            self.toggle_music_action.setChecked(music_enabled)
            self.toggle_music_action.blockSignals(False)
        self.audio_manager.set_enabled(music_enabled)

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

        # Update mission log
        self._update_history_view()

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
            self.statusBar().showMessage(
                f"Choose your path... ({choices_count} options)"
            )

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
        if not self.audio_manager.music_loaded:
            loaded = self.audio_manager.load_background_music()
            if not loaded:
                logger.warning("Background music file unavailable")
                return

        if self.audio_manager.is_enabled():
            if self.audio_manager.play_background_music():
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
            QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.story_manager.reset()
            self._update_display()
            self.statusBar().showMessage("Game restarted!")
            self.scene_changed.emit(self.story_manager.current_scene)

    def toggle_music(self, checked: bool) -> None:
        """Toggle background music on/off."""

        self.audio_manager.set_enabled(checked)
        if checked:
            if not self.audio_manager.music_loaded:
                self.audio_manager.load_background_music()
            if self.audio_manager.play_background_music():
                self.statusBar().showMessage("Music enabled", 2000)
            else:
                self.statusBar().showMessage("Could not start music", 2000)
                if self.toggle_music_action is not None:
                    self.toggle_music_action.blockSignals(True)
                    self.toggle_music_action.setChecked(False)
                    self.toggle_music_action.blockSignals(False)
                self.audio_manager.set_enabled(False)
        else:
            self.audio_manager.stop_music()
            self.statusBar().showMessage("Music muted", 2000)

        self.settings.setValue("audio/enabled", self.audio_manager.is_enabled())

    def toggle_history_panel(self, checked: bool) -> None:
        """Show or hide the mission history panel."""

        self._history_visible = checked
        if self.history_group is not None:
            self.history_group.setVisible(checked)
        self.settings.setValue("ui/history_visible", checked)

    def _trigger_history_toggle(self) -> None:
        if self.toggle_history_action is not None:
            self.toggle_history_action.toggle()

    def _trigger_music_toggle(self) -> None:
        if self.toggle_music_action is not None:
            self.toggle_music_action.toggle()

    def _save_settings(self) -> None:
        """Persist window and audio settings."""

        self.settings.setValue("window/width", self.width())
        self.settings.setValue("window/height", self.height())
        self.settings.setValue("window/x", self.x())
        self.settings.setValue("window/y", self.y())
        self.settings.setValue("ui/history_visible", self._history_visible)
        self.settings.setValue("audio/enabled", self.audio_manager.is_enabled())
        self.settings.sync()

    def closeEvent(self, event) -> None:
        """Handle window close event."""
        self._save_settings()
        self.audio_manager.cleanup()
        super().closeEvent(event)

    def _update_history_view(self) -> None:
        if self.history_list is None:
            return

        self.history_list.clear()

        if not self.story_manager.can_go_back():
            item = QListWidgetItem("No decisions made yet.")
            item.setFlags(Qt.ItemFlag.NoItemFlags)
            self.history_list.addItem(item)
            return

        for entry in self.story_manager.iter_history():
            self.history_list.addItem(self._format_history_entry(entry))

    def _on_scene_changed(self, scene_id: str) -> None:
        """Handle scene change signal."""
        logger.debug(f"Scene changed to: {scene_id}")

    def _on_choice_made(self, choice_index: int) -> None:
        """Handle choice made signal."""
        logger.debug(f"Choice made: {choice_index}")

    def _format_history_entry(self, entry: HistoryEntry) -> str:
        """Format a history entry for display."""

        return f"{entry.scene_id} → {entry.choice_text} → {entry.next_scene}"
