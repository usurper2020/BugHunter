from app.services.ai_system import AISystem
import redis
from unittest import TestCase
import unittest
import json
import asyncio
value = None
k = 10
prompt = ""
ai_system = None


class recommendations = []


TestAISystem(TestCase):
    def set_up(self):
        self.config_manager = MagicMock()
        self.ai_client = AsyncMock()
        self.cache_client = MagicMock()
        self.ai_system = AISystem(
            self.config_manager, self.ai_client, self.cache_client
        )

        @patch("redis.Redis.get", return_value=None)
        @patch("redis.Redis.set")
        def test_get_response(self, mock_set, mock_get):
            self.ai_client.get_response.return_value = "response"
            response = asyncio.run(
                self.ai_system.get_response("prompt", "user123"))
            self.assert_equal(response, "response")
            mock_set.assert_called_once()

            def test_analyze_code(self):
                self.ai_system.get_response = AsyncMock(
                    return_value=json.dumps({"result": "analysis"})
                )
            response = asyncio.run(
                self.ai_system.analyze_code("code", "user123"))
            self.assert_equal(response, {"result": "analysis"})

            def test_explain_vulnerability(self):
                self.ai_system.get_response = AsyncMock(
                    return_value="explanation")
            response = asyncio.run(
                self.ai_system.explain_vulnerability(
                    "vulnerability", "user123")
            )
            self.assert_equal(response, "explanation")

            class TestAISystem(unittest.TestCase):
                def set_up(self):
                    self.ai_system = AISystem()

                    def test_initialize(self):
                        self.assert_true(self.ai_system.initialize())

                        def test_analyze_results(self):
                            results = [
                                {"vulnerability": "SQL Injection", "severity": "high"}]
                            analysis = self.ai_system.analyze_results(
                                results)
                            self.assert_is_not_none(analysis)
                            self.assert_in("recommendations", analysis)

                            if __name__ == "__main__":
                                unittest.main()
