import json
import os
from datetime import datetime

class ContributionSystem:
    def __init__(self):
        self.contributions_file = 'data/contributions.json'
        self.create_contributions_directory()

    def create_contributions_directory(self):
        """Create the data directory if it doesn't exist"""
        os.makedirs('data', exist_ok=True)
        
        # Initialize contributions file
        if not os.path.exists(self.contributions_file):
            with open(self.contributions_file, 'w') as f:
                json.dump([], f)

    def submit_contribution(self, username, tool_name, tool_description, tool_file):
        """Submit a new tool contribution"""
        contribution = {
            'id': str(datetime.now().timestamp()),
            'username': username,
            'tool_name': tool_name,
            'description': tool_description,
            'file': tool_file,
            'submitted_at': datetime.now().isoformat()
        }
        
        try:
            with open(self.contributions_file, 'r') as f:
                contributions = json.load(f)
            contributions.append(contribution)
            with open(self.contributions_file, 'w') as f:
                json.dump(contributions, f)
            return {'status': 'success', 'message': 'Contribution submitted successfully'}
        except Exception as e:
            return {'status': 'error', 'message': f'Failed to submit contribution: {str(e)}'}

    def get_contributions(self):
        """Get all contributions"""
        try:
            with open(self.contributions_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            return []

    def delete_contribution(self, contribution_id):
        """Delete a contribution by ID"""
        try:
            with open(self.contributions_file, 'r') as f:
                contributions = json.load(f)
            
            contributions = [c for c in contributions if c['id'] != contribution_id]
            
            with open(self.contributions_file, 'w') as f:
                json.dump(contributions, f)
            return {'status': 'success', 'message': 'Contribution deleted successfully'}
        except Exception as e:
            return {'status': 'error', 'message': f'Failed to delete contribution: {str(e)}'}
