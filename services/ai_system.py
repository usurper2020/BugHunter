"""
Main AI system for the BugHunter application.
"""

import sys
import logging
from pathlib import Path

# Add project root to Python path
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

from ai_models import AIModels
from ai_integration import AIIntegration

logger = logging.getLogger('BugHunter.AISystem')

class AISystem:
    """Main AI system that coordinates AI models and integration."""
    
    def __init__(self, config=None, nuclei_analyzer=None):
        """Initialize the AISystem with optional configuration."""
        self.config = config if config else {}
        self.models = AIModels()
        self.integration = AIIntegration(nuclei_analyzer)
        self.nuclei_analyzer = nuclei_analyzer
        self.initialized = False
        
    def initialize(self):
        """Initialize the AI system components."""
        try:
            # Always create fresh instances
            self.models = AIModels()
            self.integration = AIIntegration(self.nuclei_analyzer)
            
            # Set initialized flag
            self.initialized = True
            logger.info("AI system initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize AI system: {str(e)}")
            self.initialized = False
            raise
        
    def process_message(self, context):
        """Process a message with context through the AI system."""
        if not self.initialized:
            raise RuntimeError("AI system not initialized")
            
        try:
            # First process through integration
            processed = self.integration.process(context)
            
            # Generate response through models with enhanced context
            response = self.models.generate_response(processed)
            
            # Format the response
            return self.format_response(response)
            
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            raise
        
    def analyze_website(self, url):
        """Analyze a website for vulnerabilities."""
        if not self.initialized:
            raise RuntimeError("AI system not initialized")
            
        try:
            return self.integration.analyze_website(url)
        except Exception as e:
            logger.error(f"Error analyzing website: {str(e)}")
            raise
        
    def detect_relevant_technologies(self, context):
        """Detect technologies relevant to the conversation context."""
        technologies = []
        
        # Extract from message content
        message = context.get('message', '')
        tech_keywords = [
            'wordpress', 'php', 'apache', 'nginx', 'iis',
            'java', 'python', 'node.js', 'javascript',
            'sql', 'mongodb', 'postgresql', 'mysql'
        ]
        
        for tech in tech_keywords:
            if tech.lower() in message.lower():
                technologies.append(tech)
                
        # Extract from chat history
        for msg in context.get('chat_history', []):
            content = msg.get('content', '').lower()
            for tech in tech_keywords:
                if tech.lower() in content and tech not in technologies:
                    technologies.append(tech)
                    
        return technologies
        
    def format_response(self, response):
        """Format the AI response for display."""
        if isinstance(response, dict):
            if 'response' in response:
                content = response['response']
                if isinstance(content, str) and content.startswith("Processed: "):
                    content = content[11:]
                return content
            return str(response)
        return str(response)
        
    def set_api(self, api_name: str):
        """Set the API backend to use."""
        try:
            self.config['api'] = api_name
            # Re-initialize with new API
            self.initialize()
            logger.info(f"API switched to {api_name}")
        except Exception as e:
            logger.error(f"Failed to set API to {api_name}: {str(e)}")
            raise
        
    def get_status(self):
        """Get the current status of the AI system."""
        return {
            'initialized': self.initialized,
            'models_status': self.models.get_status() if self.models else None,
            'integration_status': self.integration.get_status() if self.integration else None,
            'current_api': self.config.get('api', 'openai')
        }
