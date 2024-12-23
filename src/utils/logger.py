import logging
from datetime import datetime
import os

class AppLogger:
    """Класс для логирования работы приложения"""
    
    def __init__(self, log_file: str = None):
        self.logger = logging.getLogger('ChatApp')
        self.logger.setLevel(logging.INFO)

        # Создаем форматтер для логов
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        # Добавляем вывод в консоль
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # Добавляем вывод в файл если указан путь
        if log_file:
            #os.makedirs(os.path.dirname(log_file), exist_ok=True)
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def info(self, message: str):
        """Логирование информационного сообщения"""
        self.logger.info(message)

    def error(self, message: str, exc_info=True):
        """Логирование ошибки"""
        self.logger.error(message, exc_info=exc_info)

    def warning(self, message: str):
        """Логирование предупреждения"""
        self.logger.warning(message)

    def debug(self, message: str):
        """Логирование отладочной информации"""
        self.logger.debug(message)
