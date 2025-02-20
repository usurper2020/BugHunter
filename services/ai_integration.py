"""
AI integration for the BugHunter application.
"""

import re
import logging
from typing import Dict, List
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger('BugHunter.AIIntegration')

class AIIntegration:
    """Class for managing AI integration within the BugHunter application."""
    
    def __init__(self, nuclei_analyzer=None):
        """Initialize the AIIntegration instance."""
        self.initialized = True
        self.nuclei_analyzer = nuclei_analyzer
        self.technology_patterns = {
            'wordpress': [r'wp-content', r'wp-includes', r'wordpress'],
            'php': [r'\.php', r'PHPSESSID'],
            'java': [r'\.jsp', r'\.do', r'jsessionid'],
            'python': [r'\.py', r'django', r'flask'],
            'node.js': [r'node_modules', r'express', r'nextjs'],
            'database': [r'mysql', r'postgresql', r'mongodb']
        }

    def process(self, context: Dict) -> Dict:
        """Process a message context through the AI integration."""
        try:
            processed = {
                'message': context.get('message', ''),
                'processed_data': {},
                'template_suggestions': [],
                'technologies': [],
                'vulnerabilities': []
            }

            # Extract URL if present in message
            url_match = re.search(r'https?://[^\s<>"]+|www\.[^\s<>"]+', context['message'])
            url = url_match.group(0) if url_match else context.get('current_url')

            # If we have a URL and nuclei analyzer, get template suggestions
            if url and self.nuclei_analyzer:
                try:
                    processed['template_suggestions'] = self.nuclei_analyzer.get_template_suggestions(url, [])
                except Exception as e:
                    processed['error'] = f"Error getting template suggestions: {str(e)}"

            # Process message content
            processed['processed_data'] = {
                'intent': self._detect_intent(context['message']),
                'entities': self._extract_entities(context['message']),
                'context': self._build_context(context.get('chat_history', []))
            }

            return processed
            
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            raise

    def analyze_website(self, url: str) -> Dict:
        """Analyze a website for vulnerabilities."""
        try:
            # Fetch website content
            response = requests.get(url, timeout=30)
            content = response.text
            soup = BeautifulSoup(content, 'html.parser')
            
            # Detect technologies
            technologies = self._detect_technologies(content, soup)
            
            # Get template suggestions
            template_suggestions = []
            if self.nuclei_analyzer:
                template_suggestions = self.nuclei_analyzer.get_template_suggestions(url, technologies)
            
            # Analyze potential vulnerabilities
            vulnerabilities = self._analyze_vulnerabilities(url, content, soup, technologies)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(technologies, vulnerabilities)
            
            return {
                'status': 'success',
                'technologies': technologies,
                'template_suggestions': template_suggestions,
                'potential_vulnerabilities': vulnerabilities,
                'recommendations': recommendations
            }
            
        except Exception as e:
            logger.error(f"Error analyzing website: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }

    def _detect_technologies(self, content: str, soup: BeautifulSoup) -> List[str]:
        """Detect technologies used in the website."""
        technologies = []
        
        for tech, patterns in self.technology_patterns.items():
            for pattern in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    technologies.append(tech)
                    break
        
        # Check meta tags and scripts
        meta_tags = soup.find_all('meta')
        scripts = soup.find_all('script')
        
        for tag in meta_tags + scripts:
            tag_str = str(tag)
            for tech, patterns in self.technology_patterns.items():
                if tech not in technologies:
                    for pattern in patterns:
                        if re.search(pattern, tag_str, re.IGNORECASE):
                            technologies.append(tech)
                            break
        
        return list(set(technologies))

    def _analyze_vulnerabilities(self, url: str, content: str, 
                               soup: BeautifulSoup, technologies: List[str]) -> List[Dict]:
        """Analyze potential vulnerabilities."""
        vulnerabilities = []
        
        # Check for common security issues
        checks = [
            {
                'type': 'information_disclosure',
                'patterns': [
                    r'(?:password|passwd|pwd).*[\'"][^\'"]+[\'"]',
                    r'(?:api[_-]?key|api[_-]?token)[^\'"]*[\'"][^\'"]+[\'"]',
                    r'(?:access[_-]?token|auth[_-]?token)[^\'"]*[\'"][^\'"]+[\'"]'
                ],
                'severity': 'high'
            },
            {
                'type': 'security_misconfiguration',
                'patterns': [
                    r'(?:ALLOW-FROM|SAMEORIGIN|DENY)',
                    r'(?:strict-transport-security)',
                    r'(?:content-security-policy)'
                ],
                'severity': 'medium'
            },
            {
                'type': 'injection_point',
                'patterns': [
                    r'(?:id|user|username|password|search|query)=[^&]+',
                    r'<input[^>]+(?:text|password|search)[^>]+>',
                    r'<form[^>]*>'
                ],
                'severity': 'medium'
            }
        ]
        
        for check in checks:
            for pattern in check['patterns']:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    vulnerabilities.append({
                        'type': check['type'],
                        'severity': check['severity'],
                        'location': 'source code',
                        'confidence': 'medium',
                        'evidence': match.group(0)
                    })
        
        return vulnerabilities

    def _generate_recommendations(self, technologies: List[str], 
                                vulnerabilities: List[Dict]) -> List[str]:
        """Generate security recommendations."""
        recommendations = []
        
        # Technology-based recommendations
        tech_recommendations = {
            'wordpress': [
                'Keep WordPress core, themes, and plugins updated',
                'Implement WordPress security hardening measures'
            ],
            'php': [
                'Ensure proper input validation and sanitization',
                'Use prepared statements for database queries'
            ],
            'java': [
                'Keep Java and all dependencies up to date',
                'Implement proper error handling'
            ],
            'python': [
                'Use the latest security features of your framework',
                'Implement proper input validation'
            ],
            'node.js': [
                'Keep Node.js and npm packages updated',
                'Use security middleware like Helmet'
            ]
        }
        
        for tech in technologies:
            if tech in tech_recommendations:
                recommendations.extend(tech_recommendations[tech])
        
        # Vulnerability-based recommendations
        vuln_types = {v['type'] for v in vulnerabilities}
        
        if 'information_disclosure' in vuln_types:
            recommendations.append('Review and secure sensitive information in source code')
        
        if 'security_misconfiguration' in vuln_types:
            recommendations.append('Implement proper security headers and configurations')
        
        if 'injection_point' in vuln_types:
            recommendations.append('Implement input validation and output encoding')
        
        return list(set(recommendations))

    def _detect_intent(self, message: str) -> str:
        """Detect the intent of the user's message."""
        intents = {
            'scan': r'(?:scan|check|analyze|test)\s+(?:for|vulnerabilities|security)',
            'explain': r'(?:explain|what|how|why)\s+(?:is|are|does)',
            'help': r'(?:help|assist|guide)',
            'fix': r'(?:fix|solve|resolve|patch)\s+(?:vulnerability|issue|problem)'
        }

        for intent, pattern in intents.items():
            if re.search(pattern, message, re.IGNORECASE):
                return intent
        return 'general'

    def _extract_entities(self, message: str) -> List[Dict]:
        """Extract relevant entities from the message."""
        entities = []
        
        # Extract URLs
        urls = re.finditer(r'https?://[^\s<>"]+|www\.[^\s<>"]+', message)
        for url in urls:
            entities.append({
                'type': 'url',
                'value': url.group(0),
                'position': url.span()
            })

        # Extract security terms
        security_terms = [
            'vulnerability', 'exploit', 'injection', 'xss',
            'sql', 'authentication', 'bypass', 'misconfiguration'
        ]
        for term in security_terms:
            if term.lower() in message.lower():
                entities.append({
                    'type': 'security_term',
                    'value': term
                })

        return entities

    def _build_context(self, chat_history: List[Dict]) -> Dict:
        """Build context from chat history."""
        context = {
            'previous_urls': [],
            'security_concerns': set()
        }

        for msg in chat_history:
            # Extract URLs
            urls = re.finditer(r'https?://[^\s<>"]+|www\.[^\s<>"]+', msg.get('content', ''))
            context['previous_urls'].extend(url.group(0) for url in urls)

            # Extract security terms
            security_terms = [
                'vulnerability', 'exploit', 'injection', 'xss',
                'sql', 'authentication', 'bypass', 'misconfiguration'
            ]
            for term in security_terms:
                if term.lower() in msg.get('content', '').lower():
                    context['security_concerns'].add(term)

        return {
            'previous_urls': list(set(context['previous_urls'])),
            'security_concerns': list(context['security_concerns'])
        }

    def get_status(self) -> Dict:
        """Get the current status of the AI integration."""
        return {
            'initialized': self.initialized,
            'status': 'running' if self.initialized else 'not initialized',
            'nuclei_analyzer_available': self.nuclei_analyzer is not None
        }
