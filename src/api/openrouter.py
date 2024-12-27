# Импорт необходимых библиотек
import requests  # Для выполнения HTTP-запросов
import os  # Для работы с переменными окружения
from dotenv import load_dotenv  # Для загрузки переменных из .env файла
from utils.logger import AppLogger  # Импорт нашего логгера

# Получаем абсолютный путь к директории, где находится текущий файл
current_dir = os.path.dirname(os.path.abspath(__file__))
# Поднимаемся на уровень выше к корневой директории проекта
root_dir = os.path.dirname(current_dir)
# Путь к файлу .env
env_path = os.path.join(root_dir, '.env')

# Загружаем переменные окружения из .env файла
load_dotenv(env_path)

class OpenRouterClient:
    """Client for interacting with OpenRouter API"""
    
    def __init__(self):
        # Инициализация логгера для отслеживания работы клиента
        self.logger = AppLogger()
        
        # Получение API ключа и базового URL из переменных окружения
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.base_url = os.getenv("BASE_URL")
        
        # Проверка наличия API ключа
        if not self.api_key:
            # Логирование ошибки
            self.logger.error("OpenRouter API key not found in .env")
            # Выбрасывание исключения
            raise ValueError("OpenRouter API key not found in .env")

        # Настройка заголовков для API запросов
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",  # Токен авторизации
            "Content-Type": "application/json"          # Тип контента
        }

        # Логирование успешной инициализации
        self.logger.info("OpenRouterClient initialized successfully")
        
        # Загружаем доступные модели
        self.available_models = self.get_models()


    def get_models(self):
        """Get available models"""
        
        # Логирование начала получения списка моделей
        self.logger.debug("Fetching available models")

        
        try:
            response = requests.get(
                f"{self.base_url}/models",
                headers=self.headers
            )
            # Преобразуем ответ в нужный формат
            models_data = response.json()
            
            # Логирование количества полученных моделей
            self.logger.info(f"Retrieved {len(models_data)} models")
            return [
                {
                    "id": model["id"],
                    "name": model["name"]
                }
                for model in models_data["data"]
            ]
        except Exception as e:
            models_default = [
                {"id": "deepseek-coder", "name": "DeepSeek"},
                {"id": "claude-3-sonnet", "name": "Claude 3.5 Sonnet"},
                {"id": "gpt-3.5-turbo", "name": "GPT-3.5 Turbo"}
            ]
            self.logger.info(f"Retrieved {len(models_default)} models with Error: {e}")
                
            # Возвращаем список базовых моделей если API недоступен
            return models_default

    def send_message(self, message: str, model: str):
        """Send message to OpenRouter API"""
        # Логирование отправки сообщения конкретной модели
        self.logger.debug(f"Sending message to model: {model}")
        
        # Подготовка данных для отправки
        data = {
            "model": model, # ID выбранной модели
            "messages": [{"role": "user", "content": message}] # Сообщение пользователя
        }
        
        try:
            # Логирование начала выполнения API запроса
            self.logger.debug("Making API request")

            # Отправка POST запроса к API
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=data
            )
            
            # Проверка на ошибки HTTP
            response.raise_for_status()
            
            # Логирование успешного получения ответа
            self.logger.info("Successfully received response from API")
            
            
            return response.json()

        except Exception as e:
            # Формирование сообщения об ошибке
            error_msg = f"API request failed: {str(e)}"
            # Логирование ошибки с полным стектрейсом
            self.logger.error(error_msg, exc_info=True)
            # Возврат сообщения об ошибке пользователю
            return {"error": str(e)}       

        
    def get_balance(self):
        """Получить текущий баланс"""
        try:
            # Запрос на получение баланса в OpenRouter.ai
            response = requests.get(
                f"{self.base_url}/credits",
                headers=self.headers
            )
            data = response.json()
            if data:
                data = data.get('data') 
                return f"${(data.get('total_credits', 0)-data.get('total_usage', 0)):.2f}"
            return "Ошибка"
        except Exception as e:
            # Формирование сообщения об ошибке
            error_msg = f"API request failed: {str(e)}"
            # Логирование ошибки с полным стектрейсом
            self.logger.error(error_msg, exc_info=True)
            # Возврат сообщения об ошибке пользователю  
            return "Ошибка"    
