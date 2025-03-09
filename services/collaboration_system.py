import os
import json
from datetime import datetime
from typing import Dict, List, Optional
import uuid

class CollaborationSystem:
    """Manages collaboration features between users"""
    
    def __init__(self):
        self.data_dir = os.path.join('data', 'collaboration')
        self.projects_dir = os.path.join(self.data_dir, 'projects')
        self.messages_dir = os.path.join(self.data_dir, 'messages')
        self.ensure_directories()
        
    def ensure_directories(self):
        """Ensure required directories exist"""
        os.makedirs(self.projects_dir, exist_ok=True)
        os.makedirs(self.messages_dir, exist_ok=True)
        
    def create_project(
        self,
        name: str,
        description: str,
        owner: str,
        members: List[str] = None
    ) -> Dict:
        """Create a new collaboration project"""
        try:
            project_id = str(uuid.uuid4())
            project = {
                "id": project_id,
                "name": name,
                "description": description,
                "owner": owner,
                "members": members or [],
                "created_at": str(datetime.now()),
                "updated_at": str(datetime.now()),
                "status": "active"
            }
            
            self._save_project(project_id, project)
            
            return {
                "status": "success",
                "message": "Project created successfully",
                "project_id": project_id
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
            
    def get_project(self, project_id: str) -> Dict:
        """Get project details"""
        try:
            project = self._load_project(project_id)
            if not project:
                return {
                    "status": "error",
                    "message": "Project not found"
                }
                
            return {
                "status": "success",
                "project": project
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
            
    def update_project(
        self,
        project_id: str,
        updates: Dict
    ) -> Dict:
        """Update project details"""
        try:
            project = self._load_project(project_id)
            if not project:
                return {
                    "status": "error",
                    "message": "Project not found"
                }
                
            # Update fields
            for key, value in updates.items():
                if key in ["name", "description", "status"]:
                    project[key] = value
                    
            project["updated_at"] = str(datetime.now())
            self._save_project(project_id, project)
            
            return {
                "status": "success",
                "message": "Project updated successfully"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
            
    def add_member(
        self,
        project_id: str,
        username: str,
        role: str = "member"
    ) -> Dict:
        """Add a member to a project"""
        try:
            project = self._load_project(project_id)
            if not project:
                return {
                    "status": "error",
                    "message": "Project not found"
                }
                
            if username in project["members"]:
                return {
                    "status": "error",
                    "message": "User is already a member"
                }
                
            project["members"].append(username)
            project["updated_at"] = str(datetime.now())
            self._save_project(project_id, project)
            
            return {
                "status": "success",
                "message": "Member added successfully"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
            
    def remove_member(
        self,
        project_id: str,
        username: str
    ) -> Dict:
        """Remove a member from a project"""
        try:
            project = self._load_project(project_id)
            if not project:
                return {
                    "status": "error",
                    "message": "Project not found"
                }
                
            if username not in project["members"]:
                return {
                    "status": "error",
                    "message": "User is not a member"
                }
                
            project["members"].remove(username)
            project["updated_at"] = str(datetime.now())
            self._save_project(project_id, project)
            
            return {
                "status": "success",
                "message": "Member removed successfully"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
            
    def send_message(
        self,
        project_id: str,
        sender: str,
        content: str,
        message_type: str = "text"
    ) -> Dict:
        """Send a message in a project"""
        try:
            project = self._load_project(project_id)
            if not project:
                return {
                    "status": "error",
                    "message": "Project not found"
                }
                
            if sender not in project["members"] and sender != project["owner"]:
                return {
                    "status": "error",
                    "message": "User is not authorized to send messages"
                }
                
            message = {
                "id": str(uuid.uuid4()),
                "project_id": project_id,
                "sender": sender,
                "content": content,
                "type": message_type,
                "timestamp": str(datetime.now())
            }
            
            self._save_message(message)
            
            return {
                "status": "success",
                "message": "Message sent successfully",
                "message_id": message["id"]
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
            
    def get_messages(
        self,
        project_id: str,
        limit: int = 50,
        before: Optional[str] = None
    ) -> Dict:
        """Get messages from a project"""
        try:
            messages = []
            message_files = sorted(
                [f for f in os.listdir(self.messages_dir) if f.endswith('.json')],
                reverse=True
            )
            
            for filename in message_files:
                if len(messages) >= limit:
                    break
                    
                with open(os.path.join(self.messages_dir, filename)) as f:
                    message = json.load(f)
                    
                if message["project_id"] != project_id:
                    continue
                    
                if before and message["timestamp"] >= before:
                    continue
                    
                messages.append(message)
                
            return {
                "status": "success",
                "messages": messages
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
            
    def _save_project(self, project_id: str, project: Dict):
        """Save project data to file"""
        with open(os.path.join(self.projects_dir, f"{project_id}.json"), 'w') as f:
            json.dump(project, f, indent=2)
            
    def _load_project(self, project_id: str) -> Optional[Dict]:
        """Load project data from file"""
        try:
            with open(os.path.join(self.projects_dir, f"{project_id}.json")) as f:
                return json.load(f)
        except FileNotFoundError:
            return None
            
    def _save_message(self, message: Dict):
        """Save message data to file"""
        filename = f"{message['timestamp'].replace(':', '-')}_{message['id']}.json"
        with open(os.path.join(self.messages_dir, filename), 'w') as f:
            json.dump(message, f, indent=2)
