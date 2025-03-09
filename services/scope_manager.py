import os
import json
from typing import Dict, List, Optional
from datetime import datetime

class ScopeManager:
    """Manages target scope for security testing"""
    
    def __init__(self):
        self.scope_file = os.path.join('data', 'scope.json')
        self.ensure_files()
        self.load_scope()
        
    def ensure_files(self):
        """Ensure required files exist"""
        os.makedirs(os.path.dirname(self.scope_file), exist_ok=True)
        if not os.path.exists(self.scope_file):
            self.save_scope({
                "targets": [],
                "exclusions": [],
                "last_updated": str(datetime.now())
            })
            
    def load_scope(self) -> Dict:
        """Load scope from file"""
        try:
            with open(self.scope_file, 'r') as f:
                self.scope = json.load(f)
            return self.scope
        except Exception as e:
            print(f"Error loading scope: {e}")
            self.scope = {
                "targets": [],
                "exclusions": [],
                "last_updated": str(datetime.now())
            }
            return self.scope
            
    def save_scope(self, scope_data: Dict) -> bool:
        """Save scope to file"""
        try:
            with open(self.scope_file, 'w') as f:
                json.dump(scope_data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving scope: {e}")
            return False
            
    def add_target(self, target: str, target_type: str = "url") -> Dict:
        """Add a target to scope"""
        try:
            if target in [t['target'] for t in self.scope['targets']]:
                return {
                    "status": "error",
                    "message": "Target already in scope"
                }
                
            self.scope['targets'].append({
                "target": target,
                "type": target_type,
                "added": str(datetime.now())
            })
            
            self.scope['last_updated'] = str(datetime.now())
            self.save_scope(self.scope)
            
            return {
                "status": "success",
                "message": "Target added to scope"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
            
    def remove_target(self, target: str) -> Dict:
        """Remove a target from scope"""
        try:
            initial_count = len(self.scope['targets'])
            self.scope['targets'] = [
                t for t in self.scope['targets'] 
                if t['target'] != target
            ]
            
            if len(self.scope['targets']) == initial_count:
                return {
                    "status": "error",
                    "message": "Target not found in scope"
                }
                
            self.scope['last_updated'] = str(datetime.now())
            self.save_scope(self.scope)
            
            return {
                "status": "success",
                "message": "Target removed from scope"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
            
    def add_exclusion(self, pattern: str) -> Dict:
        """Add an exclusion pattern"""
        try:
            if pattern in self.scope['exclusions']:
                return {
                    "status": "error",
                    "message": "Exclusion pattern already exists"
                }
                
            self.scope['exclusions'].append(pattern)
            self.scope['last_updated'] = str(datetime.now())
            self.save_scope(self.scope)
            
            return {
                "status": "success",
                "message": "Exclusion pattern added"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
            
    def remove_exclusion(self, pattern: str) -> Dict:
        """Remove an exclusion pattern"""
        try:
            if pattern not in self.scope['exclusions']:
                return {
                    "status": "error",
                    "message": "Exclusion pattern not found"
                }
                
            self.scope['exclusions'].remove(pattern)
            self.scope['last_updated'] = str(datetime.now())
            self.save_scope(self.scope)
            
            return {
                "status": "success",
                "message": "Exclusion pattern removed"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
            
    def get_targets(self, target_type: Optional[str] = None) -> List[Dict]:
        """Get all targets, optionally filtered by type"""
        if target_type:
            return [t for t in self.scope['targets'] if t['type'] == target_type]
        return self.scope['targets']
        
    def get_exclusions(self) -> List[str]:
        """Get all exclusion patterns"""
        return self.scope['exclusions']
        
    def is_in_scope(self, target: str) -> bool:
        """Check if a target is in scope"""
        # Check if target matches any exclusion pattern
        for pattern in self.scope['exclusions']:
            if pattern in target:
                return False
                
        # Check if target matches any included target
        for t in self.scope['targets']:
            if t['target'] in target:
                return True
                
        return False
