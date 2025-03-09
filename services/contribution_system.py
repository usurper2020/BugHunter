import os
import json
from datetime import datetime
from typing import Dict, List, Optional
import uuid

class ContributionSystem:
    """Manages user contributions and rewards"""
    
    def __init__(self):
        self.data_dir = os.path.join('data', 'contributions')
        self.contributions_dir = os.path.join(self.data_dir, 'contributions')
        self.rewards_dir = os.path.join(self.data_dir, 'rewards')
        self.ensure_directories()
        
    def ensure_directories(self):
        """Ensure required directories exist"""
        os.makedirs(self.contributions_dir, exist_ok=True)
        os.makedirs(self.rewards_dir, exist_ok=True)
        
    def submit_contribution(
        self,
        user: str,
        contribution_type: str,
        content: Dict,
        tags: List[str] = None
    ) -> Dict:
        """Submit a new contribution"""
        try:
            contribution_id = str(uuid.uuid4())
            contribution = {
                "id": contribution_id,
                "user": user,
                "type": contribution_type,
                "content": content,
                "tags": tags or [],
                "status": "pending",
                "submitted_at": str(datetime.now()),
                "points": self._calculate_points(contribution_type, content)
            }
            
            self._save_contribution(contribution_id, contribution)
            
            return {
                "status": "success",
                "message": "Contribution submitted successfully",
                "contribution_id": contribution_id
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
            
    def review_contribution(
        self,
        contribution_id: str,
        reviewer: str,
        approved: bool,
        feedback: str = ""
    ) -> Dict:
        """Review a submitted contribution"""
        try:
            contribution = self._load_contribution(contribution_id)
            if not contribution:
                return {
                    "status": "error",
                    "message": "Contribution not found"
                }
                
            contribution["status"] = "approved" if approved else "rejected"
            contribution["reviewed_by"] = reviewer
            contribution["reviewed_at"] = str(datetime.now())
            contribution["feedback"] = feedback
            
            self._save_contribution(contribution_id, contribution)
            
            if approved:
                self._award_points(contribution["user"], contribution["points"])
                
            return {
                "status": "success",
                "message": "Contribution reviewed successfully"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
            
    def get_user_contributions(
        self,
        user: str,
        status: Optional[str] = None
    ) -> Dict:
        """Get contributions by a specific user"""
        try:
            contributions = []
            for filename in os.listdir(self.contributions_dir):
                if not filename.endswith('.json'):
                    continue
                    
                contribution = self._load_contribution(filename[:-5])
                if contribution["user"] != user:
                    continue
                    
                if status and contribution["status"] != status:
                    continue
                    
                contributions.append(contribution)
                
            return {
                "status": "success",
                "contributions": contributions
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
            
    def get_user_points(self, user: str) -> Dict:
        """Get total points for a user"""
        try:
            points_file = os.path.join(self.rewards_dir, f"{user}_points.json")
            if not os.path.exists(points_file):
                return {
                    "status": "success",
                    "points": 0
                }
                
            with open(points_file) as f:
                data = json.load(f)
                
            return {
                "status": "success",
                "points": data["points"]
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
            
    def get_leaderboard(self, limit: int = 10) -> Dict:
        """Get user leaderboard based on points"""
        try:
            users = []
            for filename in os.listdir(self.rewards_dir):
                if not filename.endswith('_points.json'):
                    continue
                    
                with open(os.path.join(self.rewards_dir, filename)) as f:
                    data = json.load(f)
                    users.append({
                        "user": filename[:-11],  # Remove _points.json
                        "points": data["points"]
                    })
                    
            # Sort by points in descending order
            users.sort(key=lambda x: x["points"], reverse=True)
            
            return {
                "status": "success",
                "leaderboard": users[:limit]
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
            
    def _calculate_points(self, contribution_type: str, content: Dict) -> int:
        """Calculate points for a contribution"""
        base_points = {
            "vulnerability": 100,
            "fix": 50,
            "documentation": 30,
            "feedback": 10
        }
        
        points = base_points.get(contribution_type, 0)
        
        # Adjust points based on content
        if contribution_type == "vulnerability":
            severity = content.get("severity", "low").lower()
            severity_multiplier = {
                "critical": 3.0,
                "high": 2.0,
                "medium": 1.5,
                "low": 1.0
            }
            points *= severity_multiplier.get(severity, 1.0)
            
        return int(points)
        
    def _award_points(self, user: str, points: int):
        """Award points to a user"""
        points_file = os.path.join(self.rewards_dir, f"{user}_points.json")
        
        try:
            with open(points_file) as f:
                data = json.load(f)
                current_points = data["points"]
        except FileNotFoundError:
            current_points = 0
            
        with open(points_file, 'w') as f:
            json.dump({
                "points": current_points + points,
                "last_updated": str(datetime.now())
            }, f, indent=2)
            
    def _save_contribution(self, contribution_id: str, contribution: Dict):
        """Save contribution data to file"""
        with open(os.path.join(self.contributions_dir, f"{contribution_id}.json"), 'w') as f:
            json.dump(contribution, f, indent=2)
            
    def _load_contribution(self, contribution_id: str) -> Optional[Dict]:
        """Load contribution data from file"""
        try:
            with open(os.path.join(self.contributions_dir, f"{contribution_id}.json")) as f:
                return json.load(f)
        except FileNotFoundError:
            return None
