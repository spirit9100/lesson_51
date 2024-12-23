import requests
import os
from dotenv import load_dotenv

# Получаем абсолютный путь к директории, где находится текущий файл
current_dir = os.path.dirname(os.path.abspath(__file__))
# Поднимаемся на уровень выше к корневой директории проекта
root_dir = os.path.dirname(current_dir)
# Путь к файлу .env
env_path = os.path.join(root_dir, '.env')

# Загружаем переменные окружения из .env файла
load_dotenv(env_path)

class OpenRouterClient:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.base_url = os.getenv("BASE_URL")   
        self.available_models = self._get_available_models()


    def _get_available_models(self):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.get(
                f"{self.base_url}/models",
                headers=headers
            )
            # Преобразуем ответ в нужный формат
            models_data = response.json()
            return [
                {
                    "id": model["id"],
                    "name": model["name"]
                }
                for model in models_data["data"]
            ]
        except Exception as e:
            print(f"Ошибка получения модели: {e}")
            # Возвращаем список базовых моделей если API недоступен
            return [
                {"id": "deepseek-coder", "name": "DeepSeek"},
                {"id": "claude-3-sonnet", "name": "Claude 3.5 Sonnet"},
                {"id": "gpt-3.5-turbo", "name": "GPT-3.5 Turbo"}
            ]

    def send_message(self, message: str, model: str):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": model,
            "messages": [{"role": "user", "content": message}]
        }

        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data
            )
            return response.json()
        except Exception as e:
            return {"error": str(e)}
        
    def get_balance(self):
        """Получить текущий баланс"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            response = requests.get(
                f"{self.base_url}/credits",
                headers=headers
            )
            data = response.json()
            if data:
                data = data.get('data') 
                return f"${(data.get('total_credits', 0)-data.get('total_usage', 0)):.2f}"
            return "Ошибка"
        except Exception as e:
            return "Ошибка"    
