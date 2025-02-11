import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

from ai_integration import AIIntegration
from ai_models import AIModels
from ai_module import ChatSystem
from ai_training import AITraining
from analytics_system import AnalyticsSystem

class AISystem:
    def __init__(self, config=None):
        self.config = config or {}
        self.integration = AIIntegration()
        self.models = AIModels()
        self.chat_system = ChatSystem()
        self.training = AITraining()
        self.analytics = AnalyticsSystem()
        
    def initialize(self):
        """Initialize all AI subsystems"""
        # Load AI models
        self.models.initialize()
        
        # Setup chat system
        self.chat_system.initialize()
        
        # Initialize training system
        self.training.initialize()
        
        # Start analytics
        self.analytics.initialize()
        
    def process_message(self, message, context=None):
        """Process a message using the AI system"""
        # Log analytics
        self.analytics.log_interaction(message)
        
        # Process through AI pipeline
        processed = self.integration.process(message)
        
        # Get model response
        response = self.models.generate_response(processed)
        
        # Train on interaction if applicable
        self.training.train_on_interaction(message, response)
        
        return response
        
    def get_system_status(self):
        """Get status of all AI subsystems"""
        return {
            'models_status': self.models.get_status(),
            'chat_status': self.chat_system.get_status(),
            'training_status': self.training.get_status(),
            'analytics_status': self.analytics.get_status()
        }
