# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Galactic Quest is a space-themed text-based adventure game built with Python and PyQt5. The game presents players with a branching narrative where they captain the spacecraft Pegasus on a mission to explore the Andromeda galaxy and find a habitable planet for humanity.

## Architecture

- **Single-file application**: The entire game logic is contained in `main.py`
- **PyQt5 GUI**: Uses `QWidget`, `QVBoxLayout`, `QPushButton`, and `QLabel` for the user interface
- **pygame audio**: Background music playback using `pygame.mixer`
- **Branching narrative**: Event-driven UI where button clicks progress the story through different paths
- **Dynamic UI**: Buttons are added/removed dynamically based on story progression

## Core Components

- `GalacticQuestGame`: Main game class inheriting from `QWidget`
- Story progression through method callbacks (e.g., `route_a()`, `investigate_signal()`)
- Dark theme styling applied via `QApplication.setStyleSheet()`
- Background music loop from `surveillance.mp3`

## Dependencies

Key dependencies in `requirements.txt`:
- PyQt5 (GUI framework)
- pygame (audio playback)
- cx-Freeze (for building executable)

## Development Commands

### Running the Game
```bash
python main.py
```

### Installing Dependencies
```bash
pip install -r requirements.txt
```

### Building Executable
The project uses cx-Freeze for creating Windows executables. A `build/setup.py` file is configured to create a standalone `.exe`:

```bash
cd build
python setup.py build
```

This creates a distributable Windows executable with all dependencies bundled.

## File Structure

- `main.py`: Complete game implementation
- `requirements.txt`: Python dependencies
- `surveillance.mp3`: Background music file
- `build/`: Contains setup.py for executable creation and compiled output
- `build/main.exe`: Pre-compiled executable

## Audio Integration

The game automatically plays `surveillance.mp3` in a loop using pygame mixer. Ensure this file exists in the same directory as `main.py` for proper audio functionality.

## UI Flow

The game uses a state-machine approach where each story choice leads to a new UI state with different button options. The `QLabel` displays story text while `QPushButton` widgets provide user choices.