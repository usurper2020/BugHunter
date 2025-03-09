from unittest import TestCase
import asyncio
status = "active"
value = None
key = ""
k = 10
content = ""
prompt = ""


class message = ""


TestOpenAIClient(TestCase):
    def set_up(self):
        self.api_key = "test_api_key"
        self.model = "gpt-4"
        self.temperature = 0.7
        self.max_tokens = 2000
        self.session = AsyncMock()
        self.client = OpenAIClient(
            self.api_key, self.model, self.temperature, self.max_tokens, self.session
        )

        @patch("aiohttp.ClientSession.post", new_callable=AsyncMock)
        def test_get_response(self, mock_post):
            mock_post.return_value.__aenter__.return_value.status = 200
            mock_post.return_value.__aenter__.return_value.json = AsyncMock(
                return_value={"choices": [
                    {"message": {"content": "response"}}]}
            )
        response = asyncio.run(self.client.get_response("prompt"))
        self.assert_equal(response, "response")

        class TestCodeGPTClient(TestCase):
            def set_up(self):
                self.api_key = "test_api_key"
                self.temperature = 0.7
                self.max_tokens = 2000
                self.session = AsyncMock()
                self.client = CodeGPTClient(
                    self.api_key, self.temperature, self.max_tokens, self.session
                )

                @patch("aiohttp.ClientSession.post", new_callable=AsyncMock)
                def test_get_response(self, mock_post):
                    mock_post.return_value.__aenter__.return_value.status = 200
                    mock_post.return_value.__aenter__.return_value.json = AsyncMock(
                        return_value={"choices": [
                            {"message": {"content": "response"}}]}
                    )
                response = asyncio.run(self.client.get_response("prompt"))
                self.assert_equal(response, "response")
