# Инструкция по установке среды сборки

Эта инструкция предназначена для Windows. Если вы используете Linux, вам не нужно устанавливать WSL - переходите сразу к разделу "Настройка зависимостей".

## Различия между Windows и Linux

### Windows
- Требуется установка WSL (Windows Subsystem for Linux)
- Сборка происходит через build.bat
- Файлы проекта копируются в WSL для сборки
- Готовый APK копируется обратно в Windows

### Linux
- Не требуется WSL
- Можно использовать buildozer напрямую
- Команды для сборки:
  ```bash
  buildozer android clean
  buildozer android debug
  ```
- APK создается сразу в директории bin/

## Windows: Установка WSL

1. Откройте PowerShell от администратора и выполните:
```powershell
wsl --install
```

2. Перезагрузите компьютер

3. После перезагрузки автоматически запустится Ubuntu в консоли. Создайте пользователя и пароль.

## 2. Настройка Ubuntu

1. Обновите пакеты:
```bash
sudo apt update
sudo apt upgrade -y
```

2. Установите необходимые системные зависимости:
```bash
sudo apt install -y python3 python3-pip git zip unzip openjdk-17-jdk python3-virtualenv autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
```

3. Установите дополнительные инструменты сборки:
```bash
sudo apt install -y build-essential libsqlite3-dev sqlite3 bzip2 libbz2-dev zlib1g-dev libssl-dev openssl libgdbm-dev libgdbm-compat-dev liblzma-dev libreadline-dev libncursesw5-dev libffi-dev uuid-dev
```

## 3. Установка зависимостей Python

1. Создайте и активируйте виртуальное окружение:
```bash
python3 -m venv ~/venv
source ~/venv/bin/activate
```

2. Установите все необходимые пакеты:
```bash
pip install appdirs==1.4.4 \
    build==1.2.2.post1 \
    buildozer==1.5.0 \
    colorama==0.4.6 \
    Cython==0.29.33 \
    distlib==0.3.9 \
    filelock==3.16.1 \
    Jinja2==3.1.5 \
    MarkupSafe==3.0.2 \
    packaging==24.2 \
    pexpect==4.9.0 \
    platformdirs==4.3.6 \
    ptyprocess==0.7.0 \
    pyproject_hooks==1.2.0 \
    python-for-android==2024.1.21 \
    setuptools==75.6.0 \
    sh==1.14.3 \
    toml==0.10.2 \
    virtualenv==20.28.0
```

## 4. Настройка переменных окружения

Добавьте следующие строки в конец файла ~/.bashrc:
```bash
export PATH=$PATH:~/.local/bin
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
```

Примените изменения:
```bash
source ~/.bashrc
```

## 5. Проверка установки

1. Проверьте версию buildozer:
```bash
buildozer --version
```

2. Проверьте наличие Java:
```bash
java -version
```

## 6. Сборка проекта

1. Перейдите в директорию с проектом в Windows
2. Запустите сборку:
```cmd
build.bat
```

## Возможные проблемы

1. Если возникает ошибка с правами доступа:
```bash
chmod -R 755 ~/aichat_build
```

2. Если buildozer не найден:
```bash
export PATH=$PATH:$HOME/.local/bin
```

3. Для очистки предыдущей сборки:
```bash
buildozer android clean
```

## Примечания

- Первая сборка может занять 30-60 минут
- Требуется минимум 10 ГБ свободного места
- Логи сборки находятся в ~/.buildozer/logs/
- Готовый APK будет в папке bin/ проекта
