import time  # Импорт модуля для работы со временем
from datetime import datetime  # Импорт для работы с датой и временем

class Analytics:
    """Класс для сбора и анализа данных об использовании приложения"""

    def __init__(self):
        """Инициализация аналитики"""
        self.start_time = time.time()  # Время запуска для отслеживания длительности сессии
        self.model_usage = {}  # Словарь для хранения статистики использования моделей
        self.session_data = []  # Список для хранения данных текущей сессии

    def track_message(self, model: str, message_length: int, response_time: float, tokens_used: int):
        """Отслеживание метрик отдельного сообщения"""
        # Инициализация статистики для новой модели
        if model not in self.model_usage:
            self.model_usage[model] = {'count': 0, 'tokens': 0}

        # Обновление счетчиков использования модели
        self.model_usage[model]['count'] += 1  # Увеличение счетчика сообщений
        self.model_usage[model]['tokens'] += tokens_used  # Добавление токенов

        # Сохранение подробной информации о сообщении
        self.session_data.append({
            'timestamp': datetime.now(),  # Время отправки
            'model': model,  # Использованная модель
            'message_length': message_length,  # Длина сообщения
            'response_time': response_time,  # Время ответа
            'tokens_used': tokens_used  # Использовано токенов
        })

    def get_statistics(self) -> dict:
        """Получение общей статистики использования"""
        # Расчет общей длительности сессии
        total_time = time.time() - self.start_time
        # Подсчет общего количества токенов
        total_tokens = sum(model['tokens'] for model in self.model_usage.values())
        # Подсчет общего количества сообщений
        total_messages = sum(model['count'] for model in self.model_usage.values())

        # Формирование и возврат статистики
        return {
            'total_messages': total_messages,  # Всего сообщений
            'total_tokens': total_tokens,  # Всего токенов
            'session_duration': total_time,  # Длительность сессии
            'messages_per_minute': (total_messages * 60) / total_time if total_time > 0 else 0,  # Сообщений в минуту
            'tokens_per_message': total_tokens / total_messages if total_messages > 0 else 0,  # Токенов на сообщение
            'model_usage': self.model_usage  # Статистика по моделям
        }

    def export_data(self) -> list:
        """Экспорт всех собранных данных сессии"""
        return self.session_data  # Возврат полных данных о сессии

    def clear_data(self):
        """Очистка всех накопленных данных аналитики"""
        self.model_usage.clear()  # Очистка статистики моделей
        self.session_data.clear()  # Очистка данных сессии
        self.start_time = time.time()  # Сброс времени начала