import time
from datetime import datetime

class Analytics:
    """Класс для сбора и анализа данных об использовании приложения"""
    
    def __init__(self):
        self.start_time = time.time()
        self.model_usage = {}
        self.session_data = []

    def track_message(self, model: str, message_length: int, response_time: float, tokens_used: int):
        """Отслеживание сообщения"""
        if model not in self.model_usage:
            self.model_usage[model] = {'count': 0, 'tokens': 0}
        
        self.model_usage[model]['count'] += 1
        self.model_usage[model]['tokens'] += tokens_used

        self.session_data.append({
            'timestamp': datetime.now(),
            'model': model,
            'message_length': message_length,
            'response_time': response_time,
            'tokens_used': tokens_used
        })

    def get_statistics(self) -> dict:
        """Получение статистики использования"""
        total_time = time.time() - self.start_time
        total_tokens = sum(model['tokens'] for model in self.model_usage.values())
        total_messages = sum(model['count'] for model in self.model_usage.values())
        
        return {
            'total_messages': total_messages,
            'total_tokens': total_tokens,
            'session_duration': total_time,
            'messages_per_minute': (total_messages * 60) / total_time if total_time > 0 else 0,
            'tokens_per_message': total_tokens / total_messages if total_messages > 0 else 0,
            'model_usage': self.model_usage
        }

    def export_data(self) -> list:
        """Экспорт данных сессии"""
        return self.session_data
    
    def clear_data(self):
        """Очистка всех данных аналитики"""
        self.model_usage.clear()
        self.session_data.clear()
        self.start_time = time.time()
