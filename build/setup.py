from cx_Freeze import setup, Executable
import sys

build_exe_options = {"packages": ["os", "sys", "PyQt5", "pygame"],
                     "include_files":[r"C:\Users\andr2378\Documents\Programs\Python\Galactic-Quest\surveillance.mp3"],
                     "excludes": ["tkinter"]}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  
    name = "GalacticQuestGame",
    version = "0.1",
    description = "A space exploration game!",
    options = {"build_exe": build_exe_options},
    executables = [Executable("main.py", base=base)]
)