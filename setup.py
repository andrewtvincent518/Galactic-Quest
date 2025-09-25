"""Setup script for building Galactic Quest executable."""

from cx_Freeze import setup, Executable
import sys
from pathlib import Path

# Build options
build_exe_options = {
    "packages": [
        "galactic_quest",
        "PyQt6",
        "pygame",
        "json",
        "pathlib",
        "logging",
        "typing"
    ],
    "include_files": [
        ("surveillance.mp3", "surveillance.mp3"),
        ("galactic_quest/data/story.json", "galactic_quest/data/story.json"),
    ],
    "excludes": [
        "tkinter",
        "unittest",
        "test",
        "distutils",
        "email",
        "html",
        "http",
        "urllib",
        "xml"
    ],
    "optimize": 2,
}

# Base configuration for Windows
base = None
if sys.platform == "win32":
    base = "Win32GUI"

# Executable configuration
executables = [
    Executable(
        script="galactic_quest/main.py",
        base=base,
        target_name="GalacticQuest.exe",
        icon=None,  # Add icon file path if you have one
    )
]

# Setup configuration
setup(
    name="Galactic Quest",
    version="1.0.0",
    description="A space-themed adventure game",
    author="Andrew Vincent",
    options={"build_exe": build_exe_options},
    executables=executables,
)