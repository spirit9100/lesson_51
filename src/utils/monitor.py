import psutil
import time
from typing import Dict
from datetime import datetime, timedelta  # Добавляем импорт

class PerformanceMonitor:
    """Класс для мониторинга производительности приложения"""
    
    def __init__(self):
        self.start_time = time.time()
        self.process = psutil.Process()
        self.metrics_history = []

    def get_metrics(self) -> Dict:
        """Получение метрик производительности"""
        metrics = {
            'cpu_percent': self.process.cpu_percent(),
            'memory_used': self.process.memory_info().rss / 1024 / 1024,  # МБ
            'uptime': time.time() - self.start_time,
            'threads': self.process.num_threads(),
            'timestamp': datetime.now()
        }
        
        # Сохраняем метрики в историю
        self.metrics_history.append(metrics)
        
        return metrics

    def check_health(self) -> bool:
        """Проверка состояния приложения"""
        metrics = self.get_metrics()
        
        # Проверка на превышение пороговых значений
        thresholds = {
            'cpu_percent': 80,
            'memory_used': 1024,  # 1 ГБ
            'threads': 100
        }
        
        return all(
            metrics[key] < value 
            for key, value in thresholds.items()
        )

    def get_average_metrics(self, minutes: int = 5) -> Dict:
        """Получение средних метрик за последние n минут"""
        cutoff_time = datetime.now() - timedelta(minutes=minutes)
        recent_metrics = [
            m for m in self.metrics_history 
            if m['timestamp'] > cutoff_time
        ]
        
        if not recent_metrics:
            return {}
            
        return {
            'avg_cpu': sum(m['cpu_percent'] for m in recent_metrics) / len(recent_metrics),
            'avg_memory': sum(m['memory_used'] for m in recent_metrics) / len(recent_metrics),
            'avg_threads': sum(m['threads'] for m in recent_metrics) / len(recent_metrics)
        }

    def log_metrics(self, logger):
        """Логирование метрик"""
        metrics = self.get_metrics()
        logger.info(f"Performance metrics: {metrics}")
