import os
import json
from datetime import datetime
from typing import Dict, List, Optional

class Collaboration:
    """Handles collaboration features between users"""
    
    def __init__(self):
        self.data_dir = os.path.join('data', 'collaboration')
        self.ensure_directories()
        
    def ensure_directories(self):
        """Ensure required directories exist"""
        os.makedirs(self.data_dir, exist_ok=True)
        
    def create_collaboration(
        self,
        project_id: str,
        user_id: str,
        role: str
    ) -> Dict:
        """Create a new collaboration entry"""
        try:
            collaboration_id = str(uuid.uuid4())
            collaboration = {
                "id": collaboration_id,
                "project_id": project_id,
                "user_id": user_id,
                "role": role,
                "created_at": str(datetime.now())
            }
            
            self._save_collaboration(collaboration_id, collaboration)
            
            return {
                "status": "success",
                "message": "Collaboration created successfully"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
            
    def get_collaborations(self, project_id: str) -> Dict:
        """Get all collaborations for a project"""
        try:
            collaborations = []
            for filename in os.listdir(self.data_dir):
                if not filename.endswith('.json'):
                    continue
                    
                with open(os.path.join(self.data_dir, filename)) as f:
                    collaboration = json.load(f)
                    if collaboration["project_id"] == project_id:
                        collaborations.append(collaboration)
                        
            return {
                "status": "success",
                "collaborations": collaborations
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
            
    def _save_collaboration(self, collaboration_id: str, collaboration: Dict):
        """Save collaboration data to file"""
        with open(os.path.join(self.data_dir, f"{collaboration_id}.json"), 'w') as f:
            json.dump(collaboration, f, indent=2)
            
    def _load_collaboration(self, collaboration_id: str) -> Optional[Dict]:
        """Load collaboration data from file"""
        try:
            with open(os.path.join(self.data_dir, f"{collaboration_id}.json")) as f:
                return json.load(f)
        except FileNotFoundError:
            return None
