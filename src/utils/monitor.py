import psutil  # Импорт библиотеки для мониторинга системных ресурсов
import time  # Импорт модуля для работы со временем
from datetime import datetime  # Импорт для работы с датой и временем
import threading  # Импорт для работы с потоками

class PerformanceMonitor:
    """Класс для мониторинга производительности приложения"""
    
    def __init__(self):
        """Инициализация монитора производительности"""
        self.start_time = time.time()  # Время запуска мониторинга
        self.metrics_history = []  # История метрик
        self.process = psutil.Process()  # Получение текущего процесса
        # Пороговые значения для метрик
        self.thresholds = {
            'cpu_percent': 80.0,  # Максимальный процент CPU
            'memory_percent': 75.0,  # Максимальный процент памяти
            'thread_count': 50  # Максимальное количество потоков
        }

    def get_metrics(self) -> dict:
        """Получение текущих метрик производительности"""
        try:
            metrics = {
                'timestamp': datetime.now(),  # Текущее время
                'cpu_percent': self.process.cpu_percent(),  # Использование CPU
                'memory_percent': self.process.memory_percent(),  # Использование памяти
                'thread_count': len(self.process.threads()),  # Количество потоков
                'uptime': time.time() - self.start_time  # Время работы
            }
            
            self.metrics_history.append(metrics)  # Сохранение метрик в историю
            # Ограничение истории последними 1000 записями
            if len(self.metrics_history) > 1000:
                self.metrics_history.pop(0)
                
            return metrics  # Возврат текущих метрик
            
        except Exception as e:
            return {
                'error': str(e),  # Возврат ошибки при сборе метрик
                'timestamp': datetime.now()
            }

    def check_health(self) -> dict:
        """Проверка состояния системы на основе пороговых значений"""
        metrics = self.get_metrics()  # Получение текущих метрик
        
        if 'error' in metrics:
            return {'status': 'error', 'error': metrics['error']}
            
        health_status = {
            'status': 'healthy',  # Статус по умолчанию
            'warnings': [],  # Список предупреждений
            'timestamp': metrics['timestamp']  # Время проверки
        }
        
        # Проверка CPU
        if metrics['cpu_percent'] > self.thresholds['cpu_percent']:
            health_status['warnings'].append(f"High CPU usage: {metrics['cpu_percent']}%")
            health_status['status'] = 'warning'
            
        # Проверка памяти    
        if metrics['memory_percent'] > self.thresholds['memory_percent']:
            health_status['warnings'].append(f"High memory usage: {metrics['memory_percent']}%")
            health_status['status'] = 'warning'
            
        # Проверка количества потоков    
        if metrics['thread_count'] > self.thresholds['thread_count']:
            health_status['warnings'].append(f"High thread count: {metrics['thread_count']}")
            health_status['status'] = 'warning'
            
        return health_status  # Возврат статуса здоровья системы

    def get_average_metrics(self) -> dict:
        """Расчет средних показателей за всю историю"""
        if not self.metrics_history:
            return {"error": "No metrics available"}
            
        # Расчет средних значений
        avg_metrics = {
            'avg_cpu': sum(m['cpu_percent'] for m in self.metrics_history) / len(self.metrics_history),
            'avg_memory': sum(m['memory_percent'] for m in self.metrics_history) / len(self.metrics_history),
            'avg_threads': sum(m['thread_count'] for m in self.metrics_history) / len(self.metrics_history),
            'samples_count': len(self.metrics_history)  # Количество измерений
        }
        
        return avg_metrics  # Возврат средних показателей

    def log_metrics(self, logger) -> None:
        """Логирование текущих метрик"""
        metrics = self.get_metrics()  # Получение текущих метрик
        health = self.check_health()  # Проверка здоровья системы
        
        # Логирование метрик
        if 'error' not in metrics:
            logger.info(
                f"Performance metrics - "
                f"CPU: {metrics['cpu_percent']:.1f}%, "
                f"Memory: {metrics['memory_percent']:.1f}%, "
                f"Threads: {metrics['thread_count']}, "
                f"Uptime: {metrics['uptime']:.0f}s"
            )
            
        # Логирование предупреждений
        if health['status'] == 'warning':
            for warning in health['warnings']:
                logger.warning(f"Performance warning: {warning}")