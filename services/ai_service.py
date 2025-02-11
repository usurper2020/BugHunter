import openai
from typing import Dict, Any, List, Optional
import json
import aiohttp
from datetime import datetime

from config import config
from logger_config import logger_config
from database import DatabaseManager, CacheManager
from models import Finding, ScanResult, SeverityLevel

logger = logger_config.get_logger(__name__)

class AIService:
    """Service for AI-powered vulnerability analysis and assistance"""

    def __init__(self):
        self.api_type = config.get('AI_API_TYPE', 'codegpt')  # Set default to 'codegpt'
        self.api_key = config.get('AI_API_KEY')
        self.model = config.get('AI_MODEL', 'gpt-4')
        self.temperature = config.get('AI_TEMPERATURE', 0.7)
        self.cache_ttl = config.get('AI_CACHE_TTL_MINUTES', 60)

        if self.api_type == 'openai':
            openai.api_key = self.api_key  # Set the API key here

    async def analyze_vulnerability(self, finding: Finding) -> Dict[str, Any]:
        """Analyze a vulnerability finding using AI"""
        cache_key = f"ai_analysis:{finding.id}"
        
        # Check cache first
        cached_analysis = CacheManager.get(cache_key)
        if cached_analysis:
            return json.loads(cached_analysis)

        try:
            # Prepare context for AI
            context = {
                'type': finding.type,
                'severity': finding.severity.value,
                'description': finding.description,
                'details': finding.details
            }

            # Generate prompt
            prompt = self._generate_analysis_prompt(context)

            # Get AI analysis
            if self.api_type == 'openai':
                analysis = await self._get_openai_analysis(prompt)
            else:
                analysis = await self._get_codegpt_analysis(prompt)

            # Cache the result
            CacheManager.set(
                cache_key,
                json.dumps(analysis),
                expire=self.cache_ttl * 60
            )

            return analysis

        except Exception as e:
            logger.error(f"AI analysis failed: {str(e)}", exc_info=True)
            return {
                'success': False,
                'message': f'AI analysis failed: {str(e)}'
            }

    async def suggest_fixes(self, finding: Finding) -> Dict[str, Any]:
        """Get AI-suggested fixes for a vulnerability"""
        try:
            context = {
                'type': finding.type,
                'severity': finding.severity.value,
                'description': finding.description,
                'details': finding.details
            }

            prompt = self._generate_fix_prompt(context)

            if self.api_type == 'openai':
                suggestions = await self._get_openai_analysis(prompt)
            else:
                suggestions = await self._get_codegpt_analysis(prompt)

            return suggestions

        except Exception as e:
            logger.error(f"Failed to get fix suggestions: {str(e)}", exc_info=True)
            return {
                'success': False,
                'message': f'Failed to get fix suggestions: {str(e)}'
            }

    async def analyze_scan_results(self, scan_id: str) -> Dict[str, Any]:
        """Analyze complete scan results using AI"""
        with DatabaseManager.get_session() as session:
            scan = session.query(ScanResult).filter_by(scan_id=scan_id).first()
            if not scan:
                return {
                    'success': False,
                    'message': 'Scan not found'
                }

            findings = scan.findings

            try:
                # Prepare context for AI
                context = {
                    'target_url': scan.target_url,
                    'findings': [
                        {
                            'type': f.type,
                            'severity': f.severity.value,
                            'description': f.description,
                            'details': f.details
                        }
                        for f in findings
                    ]
                }

                prompt = self._generate_scan_analysis_prompt(context)

                if self.api_type == 'openai':
                    analysis = await self._get_openai_analysis(prompt)
                else:
                    analysis = await self._get_codegpt_analysis(prompt)

                return analysis

            except Exception as e:
                logger.error(f"Scan analysis failed: {str(e)}", exc_info=True)
                return {
                    'success': False,
                    'message': f'Scan analysis failed: {str(e)}'
                }

    async def get_security_recommendations(self, target_url: str) -> Dict[str, Any]:
        """Get AI-powered security recommendations"""
        try:
            prompt = self._generate_recommendations_prompt(target_url)

            if self.api_type == 'openai':
                recommendations = await self._get_openai_analysis(prompt)
            else:
                recommendations = await self._get_codegpt_analysis(prompt)

            return recommendations

        except Exception as e:
            logger.error(f"Failed to get recommendations: {str(e)}", exc_info=True)
            return {
                'success': False,
                'message': f'Failed to get recommendations: {str(e)}'
            }

    async def _get_openai_analysis(self, prompt: str) -> Dict[str, Any]:
        """Get analysis from OpenAI API"""
        try:
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.temperature
            )

            return {
                'success': True,
                'analysis': response.choices[0].message.content
            }

        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}", exc_info=True)
            raise

    async def _get_codegpt_analysis(self, prompt: str) -> Dict[str, Any]:
        """Get analysis from CodeGPT API"""
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    'Authorization': f'Bearer {self.api_key}',
                    'Content-Type': 'application/json'
                }
                
                data = {
                    'messages': [
                        {
                            'role': 'user',
                            'content': prompt
                        }
                    ],
                    'temperature': self.temperature,
                    'max_tokens': config.get('AI_MAX_TOKENS', 2000)
                }

                async with session.post(
                    'https://api.codegpt.co/v1/chat/completions',
                    headers=headers,
                    json=data
                ) as response:
                    result = await response.json()

                    if response.status != 200:
                        logger.error(f"CodeGPT API error: {result}")
                        return {
                            'success': False,
                            'message': result.get('error', {}).get('message', 'Unknown error')
                        }

                    return {
                        'success': True,
                        'analysis': result['choices'][0]['message']['content']
                    }

        except Exception as e:
            logger.error(f"CodeGPT API error: {str(e)}", exc_info=True)
            raise

    def _generate_analysis_prompt(self, context: Dict[str, Any]) -> str:
        """Generate prompt for vulnerability analysis"""
        return f"""
        Analyze the following vulnerability:
        Type: {context['type']}
        Severity: {context['severity']}
        Description: {context['description']}
        Details: {context['details']}

        Please provide:
        1. A detailed analysis of the vulnerability
        2. Potential impact on the system
        3. Common attack vectors
        4. Detection methods
        5. Risk assessment
        """

    def _generate_fix_prompt(self, context: Dict[str, Any]) -> str:
        """Generate prompt for fix suggestions"""
        return f"""
        Suggest fixes for the following vulnerability:
        Type: {context['type']}
        Severity: {context['severity']}
        Description: {context['description']}
        Details: {context['details']}

        Please provide:
        1. Immediate mitigation steps
        2. Long-term fixes
        3. Best practices to prevent similar vulnerabilities
        4. Code examples or configuration changes if applicable
        5. Testing procedures to verify the fix
        """

    def _generate_scan_analysis_prompt(self, context: Dict[str, Any]) -> str:
        """Generate prompt for scan results analysis"""
        findings_text = "\n".join([f"- {f['type']} ({f['severity']}): {f['description']}" for f in context['findings']])

        return f"""
        Analyze the security scan results for {context['target_url']}:

        Findings:
        {findings_text}

        Please provide:
        1. Overall security assessment
        2. Critical issues requiring immediate attention
        3. Common patterns or systemic issues
        4. Prioritized remediation plan
        5. Strategic recommendations for improving security posture
        """

    def _generate_recommendations_prompt(self, target_url: str) -> str:
        """Generate prompt for security recommendations"""
        return f"""
        Provide security recommendations for {target_url}:

        Please include:
        1. Security best practices specific to this type of target
        2. Common vulnerabilities to check
        3. Recommended security controls
        4. Testing strategies
        5. Monitoring and maintenance recommendations
        """
