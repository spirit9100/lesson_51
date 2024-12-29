@echo off
echo Starting Android build process...

REM Create build directory in WSL
echo Creating build directory...
wsl mkdir -p ~/aichat_build

REM Copy project files to WSL
echo Copying project files...
wsl cp -r ./* ~/aichat_build/

REM Change to build directory and run buildozer
echo Starting build process in WSL...
wsl bash -c "cd ~/aichat_build && buildozer android clean && buildozer android debug -v"

REM Check if build was successful
wsl test -f ~/aichat_build/bin/aichat-1.0-arm64-v8a-debug.apk
if errorlevel 1 (
    echo Build failed! Check the logs for details.
    exit /b 1
)

REM Copy APK back to Windows
echo Copying APK to project directory...
if not exist "bin" mkdir bin
wsl cp ~/aichat_build/bin/aichat-1.0-arm64-v8a-debug.apk ./bin/

REM Clean up
echo Cleaning up build directory...
wsl rm -rf ~/aichat_build

echo Build process completed!
echo APK location: bin/aichat-1.0-arm64-v8a-debug.apk
