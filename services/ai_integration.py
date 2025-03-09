import os
import openai
from typing import Dict, List, Optional

class AIIntegration:
    """Handles integration with AI services"""
    
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY', '')
        if self.api_key:
            openai.api_key = self.api_key
            
    def set_api_key(self, key: str):
        """Set the OpenAI API key"""
        self.api_key = key
        openai.api_key = key
        
    async def get_completion(
        self, 
        prompt: str, 
        model: str = "gpt-3.5-turbo",
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> str:
        """Get a completion from the AI model"""
        try:
            response = await openai.ChatCompletion.acreate(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error getting AI completion: {str(e)}"
            
    def analyze_code(self, code: str) -> Dict:
        """Analyze code for security vulnerabilities"""
        try:
            prompt = f"""
            Please analyze this code for security vulnerabilities:
            
            {code}
            
            Provide a detailed analysis including:
            1. Potential security issues
            2. Best practice violations
            3. Recommended fixes
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            return {
                "status": "success",
                "analysis": response.choices[0].message.content
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
            
    def suggest_fixes(self, code: str, issues: List[str]) -> Dict:
        """Get AI suggestions for fixing code issues"""
        try:
            prompt = f"""
            Please suggest fixes for the following issues in this code:
            
            Code:
            {code}
            
            Issues:
            {chr(10).join(f'- {issue}' for issue in issues)}
            
            Provide:
            1. Specific code changes
            2. Explanation of fixes
            3. Any additional recommendations
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            return {
                "status": "success",
                "suggestions": response.choices[0].message.content
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
            
    def generate_test_cases(self, code: str) -> Dict:
        """Generate test cases for the given code"""
        try:
            prompt = f"""
            Please generate comprehensive test cases for this code:
            
            {code}
            
            Include:
            1. Unit tests
            2. Edge cases
            3. Security test scenarios
            4. Input validation tests
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            return {
                "status": "success",
                "test_cases": response.choices[0].message.content
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
