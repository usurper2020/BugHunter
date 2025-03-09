import requests
import logging

class CodeGPTClient:
    """Client for interacting with CodeGPT API"""
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.codegpt.co/v1"  # Replace with actual CodeGPT API URL
        self.logger = logging.getLogger('BugHunter.CodeGPTClient')
        
    def test_connection(self):
        """Test the API connection"""
        try:
            response = requests.get(
                f"{self.base_url}/test",
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
            response.raise_for_status()
            return True
        except Exception as e:
            self.logger.error(f"CodeGPT API test failed: {e}")
            raise

    def generate_code(self, prompt, language=None, **kwargs):
        """Generate code using CodeGPT"""
        try:
            payload = {
                "prompt": prompt,
                "language": language,
                **kwargs
            }
            
            response = requests.post(
                f"{self.base_url}/generate",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.logger.error(f"Code generation failed: {e}")
            raise
