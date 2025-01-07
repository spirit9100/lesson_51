import os
import sys
import shutil
import subprocess
from pathlib import Path

def build_windows():
    """Build Windows executable using PyInstaller"""
    print("Building Windows executable...")
    
    # Install Windows requirements
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # Create bin directory if it doesn't exist
    bin_dir = Path("bin")
    bin_dir.mkdir(exist_ok=True)
    
    # Build executable
    subprocess.run([
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--icon=assets/icon.ico",
        "--name=AI Chat",
        "src/main.py"
    ])
    
    # Move executable to bin directory
    try:
        shutil.move("dist/AI Chat.exe", "bin/AIChat.exe")
        print("Windows build completed! Executable location: bin/AIChat.exe")
    except:
        print("Windows build completed! Executable location: dist/AI Chat.exe")

def main():
    """Main build function"""
    build_windows()

if __name__ == "__main__":
    main()
