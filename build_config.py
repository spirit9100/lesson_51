from setuptools import setup
import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["flet", "requests", "asyncio", "sqlite3"],
    "excludes": ["tkinter", "unittest"],
    "include_files": [
        "assets/",
        "app_settings.json",
        "README.md",
        "LICENSE"
    ],
    "optimize": 2
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="AI Chat Assistant",
    version="1.0.0",
    description="AI Chat Assistant with multiple models support",
    options={"build_exe": build_exe_options},
    executables=[Executable(
        "src/main.py",
        base=base,
        icon="assets/icon.ico",
        target_name="AI_Chat_Assistant"
    )]
)
