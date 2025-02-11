import os
import json
from typing import Dict, List, Optional
from datetime import datetime

class ScanningProfiles:
    """Manages scanning profiles for vulnerability assessment"""
    
    def __init__(self):
        self.profiles_dir = os.path.join('data', 'scanning_profiles')
        os.makedirs(self.profiles_dir, exist_ok=True)
        self.load_default_profiles()
        
    def load_default_profiles(self):
        """Load default scanning profiles if none exist"""
        if not os.listdir(self.profiles_dir):
            default_profiles = {
                "quick_scan": {
                    "name": "Quick Scan",
                    "description": "Fast scan of common vulnerabilities",
                    "port_scan": {
                        "enabled": True,
                        "ports": "top-100"
                    },
                    "web_scan": {
                        "enabled": True,
                        "depth": 1,
                        "timeout": 300
                    },
                    "ssl_scan": {
                        "enabled": True,
                        "checks": ["basic"]
                    }
                },
                "full_scan": {
                    "name": "Full Scan",
                    "description": "Comprehensive security assessment",
                    "port_scan": {
                        "enabled": True,
                        "ports": "all"
                    },
                    "web_scan": {
                        "enabled": True,
                        "depth": 3,
                        "timeout": 1800
                    },
                    "ssl_scan": {
                        "enabled": True,
                        "checks": ["all"]
                    }
                },
                "stealth_scan": {
                    "name": "Stealth Scan",
                    "description": "Low-footprint security assessment",
                    "port_scan": {
                        "enabled": True,
                        "ports": "top-20",
                        "stealth": True
                    },
                    "web_scan": {
                        "enabled": True,
                        "depth": 1,
                        "timeout": 600,
                        "delay": 2
                    },
                    "ssl_scan": {
                        "enabled": True,
                        "checks": ["basic"]
                    }
                }
            }
            
            for profile_id, profile in default_profiles.items():
                self.save_profile(profile_id, profile)
                
    def get_profile(self, profile_id: str) -> Dict:
        """Get a specific scanning profile"""
        try:
            profile_path = os.path.join(self.profiles_dir, f"{profile_id}.json")
            if not os.path.exists(profile_path):
                return {
                    "status": "error",
                    "message": f"Profile {profile_id} not found"
                }
                
            with open(profile_path, 'r') as f:
                profile = json.load(f)
                
            return {
                "status": "success",
                "profile": profile
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
            
    def get_all_profiles(self) -> Dict:
        """Get all scanning profiles"""
        try:
            profiles = {}
            for filename in os.listdir(self.profiles_dir):
                if filename.endswith('.json'):
                    profile_id = filename[:-5]  # Remove .json extension
                    with open(os.path.join(self.profiles_dir, filename), 'r') as f:
                        profiles[profile_id] = json.load(f)
                        
            return {
                "status": "success",
                "profiles": profiles
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
            
    def create_profile(
        self,
        profile_id: str,
        name: str,
        description: str,
        settings: Dict
    ) -> Dict:
        """Create a new scanning profile"""
        try:
            profile_path = os.path.join(self.profiles_dir, f"{profile_id}.json")
            if os.path.exists(profile_path):
                return {
                    "status": "error",
                    "message": f"Profile {profile_id} already exists"
                }
                
            profile = {
                "name": name,
                "description": description,
                "created": str(datetime.now()),
                "last_modified": str(datetime.now()),
                **settings
            }
            
            self.save_profile(profile_id, profile)
            
            return {
                "status": "success",
                "message": "Profile created successfully"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
            
    def update_profile(
        self,
        profile_id: str,
        settings: Dict
    ) -> Dict:
        """Update an existing scanning profile"""
        try:
            profile_path = os.path.join(self.profiles_dir, f"{profile_id}.json")
            if not os.path.exists(profile_path):
                return {
                    "status": "error",
                    "message": f"Profile {profile_id} not found"
                }
                
            with open(profile_path, 'r') as f:
                profile = json.load(f)
                
            # Update settings
            profile.update(settings)
            profile["last_modified"] = str(datetime.now())
            
            self.save_profile(profile_id, profile)
            
            return {
                "status": "success",
                "message": "Profile updated successfully"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
            
    def delete_profile(self, profile_id: str) -> Dict:
        """Delete a scanning profile"""
        try:
            profile_path = os.path.join(self.profiles_dir, f"{profile_id}.json")
            if not os.path.exists(profile_path):
                return {
                    "status": "error",
                    "message": f"Profile {profile_id} not found"
                }
                
            os.remove(profile_path)
            
            return {
                "status": "success",
                "message": "Profile deleted successfully"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
            
    def save_profile(self, profile_id: str, profile: Dict):
        """Save a profile to file"""
        profile_path = os.path.join(self.profiles_dir, f"{profile_id}.json")
        with open(profile_path, 'w') as f:
            json.dump(profile, f, indent=2)
            
    def validate_profile(self, profile: Dict) -> Dict:
        """Validate a profile's structure and settings"""
        required_fields = ["name", "description"]
        for field in required_fields:
            if field not in profile:
                return {
                    "status": "error",
                    "message": f"Missing required field: {field}"
                }
                
        # Validate scan settings if present
        if "port_scan" in profile:
            if not isinstance(profile["port_scan"], dict):
                return {
                    "status": "error",
                    "message": "port_scan must be a dictionary"
                }
                
        if "web_scan" in profile:
            if not isinstance(profile["web_scan"], dict):
                return {
                    "status": "error",
                    "message": "web_scan must be a dictionary"
                }
                
        if "ssl_scan" in profile:
            if not isinstance(profile["ssl_scan"], dict):
                return {
                    "status": "error",
                    "message": "ssl_scan must be a dictionary"
                }
                
        return {
            "status": "success",
            "message": "Profile validation successful"
        }
