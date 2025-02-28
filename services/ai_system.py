# services/ai_system.py
import logging
import json
import aiohttp
import os
from pathlib import Path
from typing import Optional, Dict, Any
from abc import ABC, abstractmethod
from functools import lru_cache
import asyncio
import signal
import redis
from cryptography.fernet import Fernet
from prometheus_client import Counter, Histogram, start_http_server

# Configuration Manager Interface
class ConfigManager(ABC):
    @abstractmethod
    def get(self, key: str) -> Any:
        pass

# Concrete Configuration Manager
class FileConfigManager(ConfigManager):
    def __init__(self, config_path: Path):
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        with open(self.config_path) as config_file:
            return json.load(config_file)

    def get(self, key: str) -> Any:
        return self.config.get(key, os.getenv(key))

# Secure Configuration Manager
class SecureConfigManager(FileConfigManager):
    def __init__(self, config_path: Path, encryption_key: str):
        super().__init__(config_path)
        self.cipher = Fernet(encryption_key)

    def get(self, key: str) -> Any:
        encrypted_value = super().get(key)
        if encrypted_value:
            return self.cipher.decrypt(encrypted_value.encode()).decode()
        return None

# AI Client Interface
class AIClient(ABC):
    @abstractmethod
    async def get_response(self, prompt: str) -> str:
        pass

# OpenAI Client
class OpenAIClient(AIClient):
    def __init__(self, api_key: str, model: str, temperature: float, max_tokens: int, session: aiohttp.ClientSession):
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.session = session

    async def get_response(self, prompt: str) -> str:
        # Implement OpenAI API call here
        pass

# CodeGPT Client
class CodeGPTClient(AIClient):
    def __init__(self, api_key: str, temperature: float, max_tokens: int, session: aiohttp.ClientSession):
        self.api_key = api_key
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.session = session

    async def get_response(self, prompt: str) -> str:
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        data = {
            'messages': [{"role": "user", "content": prompt}],
            'temperature': self.temperature,
            'max_tokens': self.max_tokens
        }
        async with self.session.post('https://api.codegpt.co/v1/chat/completions', headers=headers, json=data) as response:
            if response.status != 200:
                error_data = await response.json()
                raise Exception(f"CodeGPT API error: {error_data.get('error', {}).get('message', 'Unknown error')}")
            result = await response.json()
            return result['choices'][0]['message']['content']

# AI System
class AISystem:
    def __init__(self, config_manager: ConfigManager, ai_client: AIClient, cache_client: redis.Redis):
        self.logger = logging.getLogger('BugHunter.AISystem')
        self.config_manager = config_manager
        self.ai_client = ai_client
        self.cache_client = cache_client
        self.rate_limiter = asyncio.Semaphore(5)  # Example rate limiter

        # Metrics
        self.request_counter = Counter('ai_requests_total', 'Total number of AI requests')
        self.error_counter = Counter('ai_errors_total', 'Total number of AI errors')
        self.response_time_histogram = Histogram('ai_response_time_seconds', 'AI response time in seconds')

        # Start Prometheus metrics server
        start_http_server(8000)

    async def get_response(self, prompt: str) -> Optional[str]:
        async with self.rate_limiter:
            self.request_counter.inc()
            with self.response_time_histogram.time():
                try:
                    cached_response = self.cache_client.get(prompt)
                    if cached_response:
                        return cached_response.decode()
                    response = await self._retry_request(prompt)
                    self.cache_client.set(prompt, response, ex=3600)  # Cache for 1 hour
                    return response
                except Exception as e:
                    self.error_counter.inc()
                    self.logger.error(f"Exception in get_response: {str(e)}")
                    return None

    async def _retry_request(self, prompt: str, retries: int = 3) -> str:
        for attempt in range(retries):
            try:
                return await self.ai_client.get_response(prompt)
            except Exception as e:
                self.logger.warning(f"Retry {attempt + 1}/{retries} failed: {str(e)}")
                if attempt == retries - 1:
                    raise

    async def analyze_code(self, code: str) -> Optional[Dict[str, str]]:
        try:
            response = await self.get_response(f"Analyze this code: {code}")
            return json.loads(response) if response else None
        except Exception as e:
            self.logger.error(f"Failed to analyze code: {str(e)}")
            return None

    async def explain_vulnerability(self, vulnerability: str) -> Optional[str]:
        try:
            return await self.get_response(f"Explain this vulnerability in simple terms: {vulnerability}")
        except Exception as e:
            self.logger.error(f"Failed to explain vulnerability: {str(e)}")
            return None

    async def shutdown(self):
        self.logger.info("Shutting down AISystem...")
        await self.ai_client.session.close()

    async def health_check(self) -> bool:
        try:
            response = await self.get_response("Health check")
            return response is not None
        except Exception as e:
            self.logger.error(f"Health check failed: {str(e)}")
            return False

# Factory for AI Clients
class AIClientFactory:
    @staticmethod
    async def create_client(api_type: str, config: Dict[str, Any], session: aiohttp.ClientSession) -> AIClient:
        if api_type == 'openai':
            return OpenAIClient(
                api_key=config['openai_api_key'],
                model=config.get('ai_model', 'gpt-4'),
                temperature=config.get('ai_temperature', 0.7),
                max_tokens=config.get('max_tokens', 2000),
                session=session
            )
        elif api_type == 'codegpt':
            return CodeGPTClient(
                api_key=config['codegpt_api_key'],
                temperature=config.get('ai_temperature', 0.7),
                max_tokens=config.get('max_tokens', 2000),
                session=session
            )
        else:
            raise ValueError(f"Unsupported API type: {api_type}")

# Usage 
async def main():
    encryption_key = os.getenv('ENCRYPTION_KEY')
    config_manager = SecureConfigManager(Path('src/config/ai_config.json'), encryption_key)
    config = config_manager.get('ai_config')
    cache_client = redis.Redis(host='localhost', port=6379, db=0)
    async with aiohttp.ClientSession() as session:
        ai_client = await AIClientFactory.create_client(config['ai_api_type'], config, session)
        ai_system = AISystem(config_manager, ai_client, cache_client)

        app = QApplication(sys.argv)
        loop = qasync.QEventLoop(app)
        asyncio.set_event_loop(loop)

        main_window = MainWindow(ai_system)
        main_window.show()

        with loop:
            loop.run_forever()

if __name__ == "__main__":
    asyncio.run(main())
