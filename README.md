# Galactic Quest - A Space-Themed Adventure Game

Welcome to Galactic Quest, a modern text-based adventure game where you play as the captain of the spacecraft Pegasus! Your mission is to explore the Andromeda galaxy and find a new habitable planet for humanity to colonize.

## 🚀 Features

- **Modern PyQt6 Interface**: Clean, responsive GUI with dark theme
- **Branching Narrative**: Multiple story paths with meaningful choices
- **Background Music**: Immersive audio experience
- **Keyboard Shortcuts**: Use number keys 1-9 to make choices quickly
- **Save Progress**: Go back to previous choices and restart anytime
- **Professional Architecture**: Modern Python code structure

## 📋 Requirements

- Python 3.8 or higher
- PyQt6
- pygame

## 🛠️ Installation

### Using pip (Recommended)

1. Clone the repository:
   ```bash
   git clone https://github.com/andrewtvincent518/Galactic-Quest.git
   cd Galactic-Quest
   ```

2. Install dependencies:
   ```bash
   pip install -e .
   ```

3. Run the game:
   ```bash
   galactic-quest
   ```

### Manual Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install PyQt6 pygame
   ```

3. Run directly:
   ```bash
   python -m galactic_quest.main
   ```

## 🎮 How to Play

1. **Launch the game** and read the introduction
2. **Make choices** by clicking buttons or using number keys (1-9)
3. **Navigate** using the Back button or Ctrl+Z
4. **Restart** anytime with Ctrl+R
5. **Toggle music** with Ctrl+M

### Keyboard Shortcuts

- `1-9`: Select choice options
- `Ctrl+R`: Restart game
- `Ctrl+Q`: Quit game
- `Ctrl+M`: Toggle background music

## 🏗️ Building Executable

To create a standalone executable:

```bash
pip install cx-Freeze
python setup.py build
```

The executable will be created in the `build/` directory.

## 🎯 Game Story

The year is 2123, and humanity has developed technology to travel across galaxies. As captain of the spacecraft Pegasus, you must:

- Choose between safe and risky routes
- Handle distress signals and alien encounters
- Navigate dangerous space anomalies
- Make decisions that affect your crew's survival
- Find a new home for humanity in the Andromeda galaxy

## 🏛️ Architecture

The game uses a modern, modular architecture:

```
galactic_quest/
├── main.py              # Application entry point
├── ui/                  # User interface components
│   ├── game_window.py   # Main game window
│   └── styles.py        # UI styling and themes
├── game/                # Game logic
│   ├── story.py         # Story management
│   └── audio.py         # Audio handling
└── data/                # Game data
    └── story.json       # Story content and structure
```

### Key Components

- **StoryManager**: Handles story progression and choice management
- **AudioManager**: Manages background music and sound effects
- **GalacticQuestWindow**: Main UI with modern Qt6 features
- **JSON-based story data**: Easy to modify and extend

## 🔧 Development

### Running Tests

```bash
pip install pytest
pytest
```

### Code Formatting

```bash
pip install black
black galactic_quest/
```

### Type Checking

```bash
pip install mypy
mypy galactic_quest/
```

## 📝 Extending the Game

The game is designed to be easily extensible:

1. **Add new scenes**: Edit `galactic_quest/data/story.json`
2. **Modify UI**: Update `galactic_quest/ui/styles.py`
3. **Add sound effects**: Extend `AudioManager` class
4. **New features**: Add modules to the appropriate package

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests!

## 📄 License

MIT © Andrew Vincent

---

*Embark on your galactic adventure and secure humanity's future among the stars!* 🌌