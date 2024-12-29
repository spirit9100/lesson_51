# AI Chat Application

A chat application that uses OpenRouter API to interact with various AI models.

## Building the Application

### Prerequisites

- Python 3.9 or higher
- For Android build: Flutter SDK and Android SDK

### Windows Build

1. Install requirements:
```bash
pip install -r requirements_win.txt
```

2. Build executable:
```bash
python build.py windows
```

The executable will be created at `bin/AIChat.exe`

### Android Build

1. Install requirements:
```bash
pip install -r requirements_android.txt
```

2. Install Flutter dependencies:
```bash
cd src
flutter pub get
```

3. Build APK:
```bash
python build.py android
```

The APK will be created at `bin/AIChat.apk`

## Configuration

Create a `.env` file in the root directory with the following content:
```
OPENROUTER_API_KEY=your_api_key_here
BASE_URL=https://openrouter.ai/api/v1
DEBUG=False
LOG_LEVEL=INFO
MAX_TOKENS=1000
TEMPERATURE=0.7
```

## Features

- Chat with various AI models
- Save chat history
- View usage analytics
- Export conversations
