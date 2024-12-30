@echo off
REM Установка Flutter SDK
chcp 65001 >nul
mode con: cols=120 lines=3000

REM Установка переменных
set FLUTTER_VERSION=3.27.1
set FLUTTER_URL=https://storage.googleapis.com/flutter_infra_release/releases/stable/windows/flutter_windows_%FLUTTER_VERSION%-stable.zip
set FLUTTER_HOME=%USERPROFILE%\flutter

REM Проверка существования Flutter SDK
if exist "%FLUTTER_HOME%\flutter\bin\flutter.bat" (
    echo Flutter SDK уже установлен в %FLUTTER_HOME%.
    pause
    exit /b 0
)



REM Создание папки для Flutter
if not exist "%FLUTTER_HOME%" (
    mkdir "%FLUTTER_HOME%"
)

REM Загрузка Flutter SDK с использованием curl
echo Скачивание Flutter SDK...
curl -L -o "%FLUTTER_HOME%\flutter.zip" "%FLUTTER_URL%"
if %errorlevel% neq 0 (
    echo Ошибка при загрузке Flutter SDK.
    pause
    exit /b 1
)

REM Распаковка Flutter SDK
echo Распаковка Flutter SDK...
powershell -Command "Expand-Archive -Path '%FLUTTER_HOME%\flutter.zip' -DestinationPath '%FLUTTER_HOME%' -Force"
if %errorlevel% neq 0 (
    echo Ошибка при распаковке Flutter SDK.
    pause
    exit /b 1
)

REM Удаление архива
del "%FLUTTER_HOME%\flutter.zip"

REM Добавление Flutter в PATH
echo Добавление Flutter в PATH...
setx PATH "%FLUTTER_HOME%\flutter\bin;%PATH%"
if %errorlevel% neq 0 (
    echo Ошибка при добавлении Flutter в PATH.
    pause
    exit /b 1
)

REM Проверка установки
echo Проверка установки Flutter...
flutter --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Ошибка при установке Flutter.
    pause
    exit /b 1
)

REM Очистка переменных
set FLUTTER_VERSION=
set FLUTTER_URL=
set FLUTTER_HOME=

echo Flutter успешно установлен.
pause
