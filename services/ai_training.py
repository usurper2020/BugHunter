import os
from datetime import datetime
from typing import Dict, List, Optional
import json

class AITraining:
    """
    Class for managing AI training within the BugHunter application.
    
    This class handles the collection and management of training data
    from user interactions for improving AI responses.
    """
    
    def __init__(self):
        """
        Initialize the AITraining instance.
        
        Sets the initialized state to False and prepares a list to hold
        training data samples.
        """
        self.initialized = True
        self.training_data = []  # Added to store training data
        
    def train_on_interaction(self, message, response):
        """
        Add a message-response pair to the training data.
        
        This method collects interaction data for future model training.
        
        Parameters:
            message (str): The user's input message.
            response (str): The system's response to the message.
        
        Raises:
            RuntimeError: If the training system has not been initialized.
        """
        if not self.initialized:
            raise RuntimeError("Training system not initialized")
        self.training_data.append({
            'message': message,
            'response': response,
            'timestamp': None  # Could add actual timestamp if needed
        })
        
    def get_training_data(self):
        """
        Retrieve the collected training data.
        
        Returns:
            list: A list of training samples, each containing a message,
            response, and timestamp.
        """
        return self.training_data
        
    def clear_training_data(self):
        """
        Clear all collected training data.
        
        This method resets the training data list to an empty state,
        effectively removing all collected samples.
        """
        self.training_data = []
        
    def get_status(self):
        """
        Retrieve the current status of the training system.
        
        Returns:
            dict: A dictionary containing the initialization status,
            the number of training samples collected, and the current
            operational status.
        """
        return {
            'initialized': self.initialized,
            'training_samples': len(self.training_data),
            'status': 'running' if self.initialized else 'not initialized'
        }
    """
    Class for managing AI training within the BugHunter application.
    
    This class handles the collection and management of training data
    from user interactions for improving AI responses.
    """
    
    def __init__(self):
        """
        Initialize the AITraining instance.
        
        Sets the initialized state to False and prepares a list to hold
        training data samples.
        """
        self.initialized = True
        self.training_data = []  # Added to store training data
        
    def train_on_interaction(self, message, response):
        """
        Add a message-response pair to the training data.
        
        This method collects interaction data for future model training.
        
        Parameters:
            message (str): The user's input message.
            response (str): The system's response to the message.
        
        Raises:
            RuntimeError: If the training system has not been initialized.
        """
        if not self.initialized:
            raise RuntimeError("Training system not initialized")
        self.training_data.append({
            'message': message,
            'response': response,
            'timestamp': None  # Could add actual timestamp if needed
        })
        
    def get_training_data(self):
        """
        Retrieve the collected training data.
        
        Returns:
            list: A list of training samples, each containing a message,
            response, and timestamp.
        """
        return self.training_data
        
    def clear_training_data(self):
        """
        Clear all collected training data.
        
        This method resets the training data list to an empty state,
        effectively removing all collected samples.
        """
        self.training_data = []
        
    def get_status(self):
        """
        Retrieve the current status of the training system.
        
        Returns:
            dict: A dictionary containing the initialization status,
            the number of training samples collected, and the current
            operational status.
        """
        return {
            'initialized': self.initialized,
            'training_samples': len(self.training_data),
            'status': 'running' if self.initialized else 'not initialized'
        }
    """Handles AI model training and fine-tuning"""
    
    def __init__(self):
        self.training_data_path = os.path.join('data', 'training')
        self.ensure_directories()
        
    def ensure_directories(self):
        """Ensure required directories exist"""
        os.makedirs(self.training_data_path, exist_ok=True)
        
    def add_training_example(self, category: str, input_text: str, output_text: str) -> Dict:
        """Add a new training example"""
        try:
            example = {
                "input": input_text,
                "output": output_text,
                "category": category,
                "timestamp": str(datetime.now())
            }
            
            filename = os.path.join(
                self.training_data_path, 
                f"{category}_{len(os.listdir(self.training_data_path))}.json"
            )
            
            with open(filename, 'w') as f:
                json.dump(example, f, indent=2)
                
            return {
                "status": "success",
                "message": "Training example added successfully"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
            
    def get_training_examples(self, category: Optional[str] = None) -> List[Dict]:
        """Get training examples, optionally filtered by category"""
        examples = []
        try:
            for filename in os.listdir(self.training_data_path):
                if filename.endswith('.json'):
                    with open(os.path.join(self.training_data_path, filename)) as f:
                        example = json.load(f)
                        if not category or example['category'] == category:
                            examples.append(example)
            return examples
        except Exception as e:
            print(f"Error loading training examples: {e}")
            return []
            
    def prepare_training_data(self, category: Optional[str] = None) -> Dict:
        """Prepare training data for model fine-tuning"""
        try:
            examples = self.get_training_examples(category)
            if not examples:
                return {
                    "status": "error",
                    "message": "No training examples found"
                }
                
            training_data = []
            for example in examples:
                training_data.append({
                    "messages": [
                        {"role": "user", "content": example['input']},
                        {"role": "assistant", "content": example['output']}
                    ]
                })
                
            output_file = os.path.join(self.training_data_path, "prepared_data.jsonl")
            with open(output_file, 'w') as f:
                for item in training_data:
                    f.write(json.dumps(item) + '\n')
                    
            return {
                "status": "success",
                "message": "Training data prepared successfully",
                "file_path": output_file
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
            
    def validate_training_data(self, data_path: str) -> Dict:
        """Validate training data format and content"""
        try:
            with open(data_path) as f:
                lines = f.readlines()
                
            valid_count = 0
            errors = []
            
            for i, line in enumerate(lines, 1):
                try:
                    item = json.loads(line)
                    if self._validate_training_item(item):
                        valid_count += 1
                    else:
                        errors.append(f"Line {i}: Invalid format")
                except json.JSONDecodeError:
                    errors.append(f"Line {i}: Invalid JSON")
                    
            return {
                "status": "success",
                "valid_count": valid_count,
                "total_count": len(lines),
                "errors": errors
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
            
    def _validate_training_item(self, item: Dict) -> bool:
        """Validate individual training item format"""
        if not isinstance(item, dict):
            return False
            
        if 'messages' not in item:
            return False
            
        messages = item['messages']
        if not isinstance(messages, list) or len(messages) < 2:
            return False
            
        required_roles = ['user', 'assistant']
        message_roles = [msg.get('role') for msg in messages]
        
        return all(role in message_roles for role in required_roles)
