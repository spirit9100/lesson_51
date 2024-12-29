import os
import sys
import shutil
import subprocess
from pathlib import Path

def build_windows():
    """Build Windows executable using PyInstaller"""
    print("Building Windows executable...")
    
    # Install Windows requirements
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements_win.txt"])
    
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

def build_android():
    """Build Android APK using Flutter"""
    print("Building Android APK...")
    
    # Install Android requirements
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements_android.txt"])
    
    # Create bin directory if it doesn't exist
    bin_dir = Path("bin")
    bin_dir.mkdir(exist_ok=True)
    
    # Navigate to src directory
    os.chdir("src")
    
    try:
        # Build Android APK
        subprocess.run(["flutter", "build", "apk", "--release"])
        
        # Move APK to bin directory
        shutil.move(
            "build/app/outputs/flutter-apk/app-release.apk",
            "../bin/AIChat.apk"
        )
        print("Android build completed! APK location: bin/AIChat.apk")
    except Exception as e:
        print(f"Error building Android APK: {e}")
    finally:
        # Return to original directory
        os.chdir("..")

def main():
    """Main build function"""
    if len(sys.argv) < 2:
        print("Please specify build target: windows or android")
        return
        
    target = sys.argv[1].lower()
    
    if target == "windows":
        build_windows()
    elif target == "android":
        build_android()
    else:
        print("Invalid target. Use 'windows' or 'android'")

if __name__ == "__main__":
    main()
