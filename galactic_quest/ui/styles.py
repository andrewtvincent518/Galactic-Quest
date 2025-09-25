"""UI styling constants and themes."""

from typing import Dict, Any

# Dark theme for the application
DARK_THEME = """
QMainWindow {
    background-color: #1e1e1e;
    color: #ffffff;
}

QWidget {
    background-color: #2d2d2d;
    color: #ffffff;
    font-family: "Segoe UI", Arial, sans-serif;
    font-size: 11pt;
}

QLabel {
    background-color: transparent;
    padding: 10px;
    line-height: 1.4;
}

QLabel#story-text {
    font-size: 12pt;
    padding: 20px;
    background-color: #383838;
    border: 1px solid #555555;
    border-radius: 8px;
    margin: 10px;
}

QGroupBox {
    border: 1px solid #3f3f3f;
    border-radius: 8px;
    margin-top: 12px;
    font-weight: 600;
    padding: 16px 12px 12px 12px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 4px;
}

QListWidget#history-list {
    background-color: #303030;
    border: 1px solid #444444;
    border-radius: 6px;
    padding: 8px;
}

QListWidget#history-list::item {
    padding: 6px 4px;
}

QListWidget#history-list::item:alternate {
    background-color: #2a2a2a;
}

QPushButton {
    background-color: #0078d4;
    border: none;
    color: #ffffff;
    padding: 12px 24px;
    font-size: 11pt;
    font-weight: 500;
    border-radius: 4px;
    min-width: 120px;
    min-height: 20px;
    margin: 4px;
}

QPushButton:hover {
    background-color: #106ebe;
}

QPushButton:pressed {
    background-color: #005a9e;
}

QPushButton:disabled {
    background-color: #555555;
    color: #888888;
}

QPushButton#back-button {
    background-color: #6c757d;
    min-width: 80px;
}

QPushButton#back-button:hover {
    background-color: #5a6268;
}

QPushButton#restart-button {
    background-color: #dc3545;
}

QPushButton#restart-button:hover {
    background-color: #c82333;
}

QMenuBar {
    background-color: #2d2d2d;
    color: #ffffff;
    border-bottom: 1px solid #555555;
}

QMenuBar::item {
    background-color: transparent;
    padding: 4px 8px;
}

QMenuBar::item:selected {
    background-color: #0078d4;
}

QMenu {
    background-color: #2d2d2d;
    color: #ffffff;
    border: 1px solid #555555;
}

QMenu::item {
    padding: 4px 16px;
}

QMenu::item:selected {
    background-color: #0078d4;
}

QStatusBar {
    background-color: #2d2d2d;
    color: #ffffff;
    border-top: 1px solid #555555;
}
"""

# Window configuration
WINDOW_CONFIG: Dict[str, Any] = {
    "title": "Galactic Quest",
    "min_width": 600,
    "min_height": 500,
    "default_width": 800,
    "default_height": 700,
}

# Animation settings
ANIMATION_DURATION = 200  # milliseconds
