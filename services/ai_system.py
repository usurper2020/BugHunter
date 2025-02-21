"""
AI integration service for the BugHunter application.
Handles AI-powered analysis, recommendations, and automation.
"""

import logging
import json
import aiohttp
import os
from pathlib import Path
from typing import Dict, List, Optional, Any, Literal
from datetime import datetime
from dataclasses import dataclass
from openai import OpenAI

@dataclass
class AIAnalysisRequest:
    """Represents a request for AI analysis"""
    content: str
    context: Dict[str, Any]
    analysis_type: str
    options: Dict[str, Any]

@dataclass
class AIAnalysisResult:
    """Represents the result of an AI analysis"""
    analysis: Dict[str, Any]
    recommendations: List[Dict[str, Any]]
    confidence: float
    timestamp: str
    duration: float

class AISystem:
    """Manages AI-powered operations and analysis"""
    
    def __init__(self):
        self.logger = logging.getLogger('BugHunter.AISystem')
        self.cache_dir = Path('data/ai_cache')
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.config: Dict[str, Any] = {}
        self.models: Dict[str, Any] = {}
        self.initialized = False
        self.api_type: Literal['openai', 'codegpt'] = 'openai'
        self.openai_client: Optional[OpenAI] = None
        
    def initialize(self) -> bool:
        """Initialize AI system"""
        try:
            # Load configuration
            config_file = Path('config/ai_config.json')
            if config_file.exists():
                with open(config_file, 'r') as f:
                    self.config = json.load(f)
            
            # Set API type
            self.api_type = self.config.get('ai_api_type', 'openai')
            
            # Initialize API clients based on type
            if self.api_type == 'openai':
                openai_api_key = self.config.get('openai_api_key') or os.getenv('OPENAI_API_KEY')
                if not openai_api_key:
                    raise ValueError("OpenAI API key not configured")
                self.openai_client = OpenAI(api_key=openai_api_key)
            else:  # codegpt
                codegpt_api_key = self.config.get('codegpt_api_key') or os.getenv('CODEGPT_API_KEY')
                if not codegpt_api_key:
                    raise ValueError("CodeGPT API key not configured")
                self.codegpt_api_key = codegpt_api_key
            
            # Load AI models configuration
            models_file = Path('config/ai_models.json')
            if models_file.exists():
                with open(models_file, 'r') as f:
                    self.models = json.load(f)
            
            self.initialized = True
            self.logger.info(f"AI system initialized successfully using {self.api_type} API")
            return True
            
        except Exception as e:
            self.logger.error(f"AI system initialization failed: {str(e)}")
            return False
    
    async def analyze_vulnerability(self, scan_result: Dict[str, Any]) -> AIAnalysisResult:
        """Analyze vulnerability scan results"""
        try:
            start_time = datetime.now()
            
            # Prepare analysis request
            request = AIAnalysisRequest(
                content=json.dumps(scan_result),
                context={
                    'scan_type': scan_result.get('scan_type'),
                    'target': scan_result.get('target')
                },
                analysis_type='vulnerability',
                options=self.config.get('vulnerability_analysis', {})
            )
            
            # Get cached analysis if available
            cached = self._get_cached_analysis(request)
            if cached:
                return cached
            
            # Prepare prompt for vulnerability analysis
            prompt = self._prepare_vulnerability_prompt(scan_result)
            
            # Get AI response based on API type
            if self.api_type == 'openai':
                response = await self._get_openai_response(prompt)
            else:
                response = await self._get_codegpt_response(prompt)
            
            # Parse AI response
            analysis = self._parse_vulnerability_analysis(response)
            
            # Create result
            result = AIAnalysisResult(
                analysis=analysis['analysis'],
                recommendations=analysis['recommendations'],
                confidence=analysis['confidence'],
                timestamp=datetime.now().isoformat(),
                duration=(datetime.now() - start_time).total_seconds()
            )
            
            # Cache result
            self._cache_analysis(request, result)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Vulnerability analysis failed: {str(e)}")
            raise
    
    async def generate_report(self, scan_result: Dict[str, Any], analysis: AIAnalysisResult) -> str:
        """Generate a detailed report with AI insights"""
        try:
            # Prepare prompt for report generation
            prompt = self._prepare_report_prompt(scan_result, analysis)
            
            # Get AI response based on API type
            if self.api_type == 'openai':
                response = await self._get_openai_response(prompt)
            else:
                response = await self._get_codegpt_response(prompt)
            
            return response
            
        except Exception as e:
            self.logger.error(f"Report generation failed: {str(e)}")
            raise
    
    async def _get_openai_response(self, prompt: str) -> str:
        """Get response from OpenAI API"""
        if not self.openai_client:
            raise ValueError("OpenAI client not initialized")
            
        response = await self.openai_client.chat.completions.create(
            model=self.models.get('openai_model', 'gpt-4'),
            messages=[
                {"role": "system", "content": "You are a security expert analyzing vulnerability scan results."},
                {"role": "user", "content": prompt}
            ],
            temperature=self.config.get('temperature', 0.3),
            max_tokens=self.config.get('max_tokens', 2000)
        )
        
        return response.choices[0].message.content
    
    async def _get_codegpt_response(self, prompt: str) -> str:
        """Get response from CodeGPT API"""
        async with aiohttp.ClientSession() as session:
            headers = {
                'Authorization': f'Bearer {self.codegpt_api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'messages': [
                    {
                        'role': 'system',
                        'content': 'You are a security expert analyzing vulnerability scan results.'
                    },
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                'temperature': self.config.get('temperature', 0.3),
                'max_tokens': self.config.get('max_tokens', 2000)
            }
            
            async with session.post(
                'https://api.codegpt.co/v1/chat/completions',
                headers=headers,
                json=data
            ) as response:
                if response.status != 200:
                    result = await response.json()
                    raise Exception(f"CodeGPT API error: {result.get('error', {}).get('message', 'Unknown error')}")
                    
                result = await response.json()
                return result['choices'][0]['message']['content']
    
    def _prepare_vulnerability_prompt(self, scan_result: Dict[str, Any]) -> str:
        """Prepare prompt for vulnerability analysis"""
        return f"""
        Please analyze the following vulnerability scan results and provide:
        1. A detailed analysis of each vulnerability found
        2. Risk assessment and potential impact
        3. Recommended remediation steps
        4. Priority order for addressing the vulnerabilities
        
        Scan Results:
        {json.dumps(scan_result, indent=2)}
        
        Please format your response as JSON with the following structure:
        {{
            "analysis": {{
                "vulnerabilities": [
                    {{
                        "id": "...",
                        "severity": "...",
                        "analysis": "...",
                        "impact": "...",
                        "remediation": "..."
                    }}
                ],
                "summary": "..."
            }},
            "recommendations": [
                {{
                    "priority": 1,
                    "action": "...",
                    "details": "..."
                }}
            ],
            "confidence": 0.95
        }}
        """
    
    def _prepare_report_prompt(self, scan_result: Dict[str, Any], analysis: AIAnalysisResult) -> str:
        """Prepare prompt for report generation"""
        return f"""
        Please generate a detailed security report based on the following scan results and analysis:
        
        Scan Results:
        {json.dumps(scan_result, indent=2)}
        
        Analysis:
        {json.dumps(analysis, indent=2)}
        
        The report should include:
        1. Executive Summary
        2. Methodology
        3. Findings and Analysis
        4. Risk Assessment
        5. Recommendations
        6. Technical Details
        7. Remediation Steps
        
        Please format the report in Markdown.
        """
    
    def _parse_vulnerability_analysis(self, response: str) -> Dict[str, Any]:
        """Parse AI response for vulnerability analysis"""
        try:
            return json.loads(response)
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse AI response: {str(e)}")
            raise
    
    def _get_cached_analysis(self, request: AIAnalysisRequest) -> Optional[AIAnalysisResult]:
        """Get cached analysis result"""
        try:
            cache_key = self._generate_cache_key(request)
            cache_file = self.cache_dir / f"{cache_key}.json"
            
            if cache_file.exists():
                with open(cache_file, 'r') as f:
                    cached = json.load(f)
                return AIAnalysisResult(**cached)
            
            return None
            
        except Exception as e:
            self.logger.error(f"Cache retrieval failed: {str(e)}")
            return None
    
    def _cache_analysis(self, request: AIAnalysisRequest, result: AIAnalysisResult):
        """Cache analysis result"""
        try:
            cache_key = self._generate_cache_key(request)
            cache_file = self.cache_dir / f"{cache_key}.json"
            
            with open(cache_file, 'w') as f:
                json.dump(result.__dict__, f, indent=4)
                
        except Exception as e:
            self.logger.error(f"Cache storage failed: {str(e)}")
    
    def _generate_cache_key(self, request: AIAnalysisRequest) -> str:
        """Generate cache key for request"""
        import hashlib
        content = f"{request.content}_{request.analysis_type}_{self.api_type}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def cleanup(self):
        """Cleanup AI system resources"""
        try:
            self.initialized = False
            self.openai_client = None
            self.logger.info("AI system resources cleaned up")
        except Exception as e:
            self.logger.error(f"AI system cleanup failed: {str(e)}")
