import sqlite3  # Импорт модуля для работы с SQLite
import json  # Импорт модуля для работы с JSON
from datetime import datetime  # Импорт для работы с датой и временем
import threading  # Импорт для работы с потоками

class ChatCache:
    def __init__(self):
        """Инициализация кэша чата"""
        self.db_name = 'chat_cache.db'  # Имя файла базы данных
        self.local = threading.local()  # Создание потокобезопасного хранилища
        self.create_tables()  # Вызов метода создания таблиц

    def get_connection(self):
        """Получение соединения для текущего потока"""
        # Проверяем, есть ли уже соединение в текущем потоке
        if not hasattr(self.local, 'connection'):
            # Если нет - создаем новое соединение
            self.local.connection = sqlite3.connect(self.db_name)
        return self.local.connection  # Возвращаем соединение

    def create_tables(self):
        """Создание таблиц в базе данных"""
        # Создаем новое соединение с базой
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Создаем таблицу messages если она не существует
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,  
                model TEXT,                           
                user_message TEXT,                    
                ai_response TEXT,                     
                timestamp DATETIME,                   
                tokens_used INTEGER                   
            )
        ''')
        conn.commit()  # Сохраняем изменения
        conn.close()   # Закрываем соединение

    def save_message(self, model, user_message, ai_response, tokens_used):
        """Сохранение сообщения в базу данных"""
        conn = self.get_connection()  # Получаем соединение для текущего потока
        cursor = conn.cursor()
        
        # Вставляем новую запись в таблицу
        cursor.execute('''
            INSERT INTO messages (model, user_message, ai_response, timestamp, tokens_used)
            VALUES (?, ?, ?, ?, ?)
        ''', (model, user_message, ai_response, datetime.now(), tokens_used))
        conn.commit()  # Сохраняем изменения

    def get_chat_history(self, limit=50):
        """Получение истории чата с ограничением по количеству записей"""
        conn = self.get_connection()  # Получаем соединение для текущего потока
        cursor = conn.cursor()
        
        # Получаем последние сообщения из базы
        cursor.execute('''
            SELECT * FROM messages 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (limit,))
        return cursor.fetchall()  # Возвращаем все найденные записи

    def __del__(self):
        """Деструктор класса - закрывает соединения при уничтожении объекта"""
        # Проверяем наличие соединения в текущем потоке
        if hasattr(self.local, 'connection'):
            self.local.connection.close()  # Закрываем соединение
            
    def clear_history(self):
        """Очистка всей истории сообщений"""
        conn = self.get_connection()  # Получаем соединение
        cursor = conn.cursor()
        cursor.execute('DELETE FROM messages')  # Удаляем все записи из таблицы
        conn.commit()  # Сохраняем изменения

    def get_formatted_history(self):
        """Получение отформатированной истории диалога"""
        conn = self.get_connection()  # Получаем соединение
        cursor = conn.cursor()
        
        # Получаем все сообщения, отсортированные по времени
        cursor.execute('''
            SELECT 
                id,
                model,
                user_message,
                ai_response,
                timestamp,
                tokens_used
            FROM messages 
            ORDER BY timestamp ASC
        ''')
        
        # Формируем список словарей с данными
        history = []
        for row in cursor.fetchall():
            history.append({
                "id": row[0],              # ID сообщения
                "model": row[1],           # Использованная модель
                "user_message": row[2],    # Сообщение пользователя
                "ai_response": row[3],     # Ответ AI
                "timestamp": row[4],       # Временная метка
                "tokens_used": row[5]      # Использовано токенов
            })
        return history  # Возвращаем форматированную историю