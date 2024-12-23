import unittest
import asyncio
from src.api.openrouter import OpenRouterClient
from src.utils.cache import ChatCache
from src.utils.analytics import Analytics

class TestChatApp(unittest.TestCase):
    def setUp(self):
        self.api_client = OpenRouterClient()
        self.cache = ChatCache()
        self.analytics = Analytics()
        
    async def test_api_connection(self):
        models = await self.api_client._get_available_models()
        self.assertIsNotNone(models)
        self.assertTrue(len(models) > 0)
        
    def test_cache_operations(self):
        test_message = "Test message"
        test_response = "Test response"
        self.cache.save_message("gpt-3.5-turbo", test_message, test_response, 10)
        history = self.cache.get_chat_history(limit=1)
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0][2], test_message)
        
    def test_analytics_data(self):
        stats = self.analytics.get_usage_statistics(days=7)
        self.assertIsNotNone(stats)
        
def run_tests():
    unittest.main()
