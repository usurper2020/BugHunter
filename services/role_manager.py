import os
import json
from datetime import datetime
from typing import Dict, List, Optional, Set

class RoleManager:
    """Manages user roles and permissions"""
    
    def __init__(self):
        self.data_dir = os.path.join('data', 'roles')
        self.roles_file = os.path.join(self.data_dir, 'roles.json')
        self.permissions_file = os.path.join(self.data_dir, 'permissions.json')
        self.ensure_files()
        self.load_data()
        
    def ensure_files(self):
        """Ensure required files exist"""
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Create default roles if file doesn't exist
        if not os.path.exists(self.roles_file):
            default_roles = {
                "admin": {
                    "name": "Administrator",
                    "description": "Full system access",
                    "permissions": ["*"],
                    "created_at": str(datetime.now())
                },
                "manager": {
                    "name": "Manager",
                    "description": "Project management access",
                    "permissions": [
                        "view_dashboard",
                        "manage_projects",
                        "manage_users",
                        "view_reports",
                        "create_reports"
                    ],
                    "created_at": str(datetime.now())
                },
                "user": {
                    "name": "User",
                    "description": "Standard user access",
                    "permissions": [
                        "view_dashboard",
                        "view_reports",
                        "submit_scans"
                    ],
                    "created_at": str(datetime.now())
                }
            }
            self._save_roles(default_roles)
            
        # Create default permissions if file doesn't exist
        if not os.path.exists(self.permissions_file):
            default_permissions = {
                "view_dashboard": {
                    "name": "View Dashboard",
                    "description": "Access to view the main dashboard"
                },
                "manage_projects": {
                    "name": "Manage Projects",
                    "description": "Create and manage security projects"
                },
                "manage_users": {
                    "name": "Manage Users",
                    "description": "Add and manage system users"
                },
                "view_reports": {
                    "name": "View Reports",
                    "description": "Access to view security reports"
                },
                "create_reports": {
                    "name": "Create Reports",
                    "description": "Create new security reports"
                },
                "submit_scans": {
                    "name": "Submit Scans",
                    "description": "Submit new security scans"
                },
                "manage_tools": {
                    "name": "Manage Tools",
                    "description": "Install and configure security tools"
                }
            }
            self._save_permissions(default_permissions)
            
    def load_data(self):
        """Load roles and permissions data"""
        with open(self.roles_file) as f:
            self.roles = json.load(f)
            
        with open(self.permissions_file) as f:
            self.permissions = json.load(f)
            
    def create_role(
        self,
        role_id: str,
        name: str,
        description: str,
        permissions: List[str]
    ) -> Dict:
        """Create a new role"""
        try:
            if role_id in self.roles:
                return {
                    "status": "error",
                    "message": "Role ID already exists"
                }
                
            # Validate permissions
            invalid_permissions = [
                p for p in permissions 
                if p != "*" and p not in self.permissions
            ]
            if invalid_permissions:
                return {
                    "status": "error",
                    "message": f"Invalid permissions: {', '.join(invalid_permissions)}"
                }
                
            role = {
                "name": name,
                "description": description,
                "permissions": permissions,
                "created_at": str(datetime.now())
            }
            
            self.roles[role_id] = role
            self._save_roles(self.roles)
            
            return {
                "status": "success",
                "message": "Role created successfully"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
            
    def update_role(
        self,
        role_id: str,
        updates: Dict
    ) -> Dict:
        """Update an existing role"""
        try:
            if role_id not in self.roles:
                return {
                    "status": "error",
                    "message": "Role not found"
                }
                
            role = self.roles[role_id]
            
            # Update fields
            if "name" in updates:
                role["name"] = updates["name"]
            if "description" in updates:
                role["description"] = updates["description"]
            if "permissions" in updates:
                # Validate new permissions
                invalid_permissions = [
                    p for p in updates["permissions"]
                    if p != "*" and p not in self.permissions
                ]
                if invalid_permissions:
                    return {
                        "status": "error",
                        "message": f"Invalid permissions: {', '.join(invalid_permissions)}"
                    }
                role["permissions"] = updates["permissions"]
                
            self._save_roles(self.roles)
            
            return {
                "status": "success",
                "message": "Role updated successfully"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
            
    def delete_role(self, role_id: str) -> Dict:
        """Delete a role"""
        try:
            if role_id not in self.roles:
                return {
                    "status": "error",
                    "message": "Role not found"
                }
                
            if role_id in ["admin", "user"]:
                return {
                    "status": "error",
                    "message": "Cannot delete system roles"
                }
                
            del self.roles[role_id]
            self._save_roles(self.roles)
            
            return {
                "status": "success",
                "message": "Role deleted successfully"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
            
    def get_role(self, role_id: str) -> Dict:
        """Get role details"""
        try:
            if role_id not in self.roles:
                return {
                    "status": "error",
                    "message": "Role not found"
                }
                
            return {
                "status": "success",
                "role": self.roles[role_id]
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
            
    def get_all_roles(self) -> Dict:
        """Get all roles"""
        try:
            return {
                "status": "success",
                "roles": self.roles
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
            
    def get_role_permissions(self, role_id: str) -> Dict:
        """Get permissions for a role"""
        try:
            if role_id not in self.roles:
                return {
                    "status": "error",
                    "message": "Role not found"
                }
                
            role = self.roles[role_id]
            if "*" in role["permissions"]:
                return {
                    "status": "success",
                    "permissions": list(self.permissions.keys())
                }
                
            return {
                "status": "success",
                "permissions": role["permissions"]
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
            
    def has_permission(
        self,
        role_id: str,
        permission: str
    ) -> Dict:
        """Check if a role has a specific permission"""
        try:
            if role_id not in self.roles:
                return {
                    "status": "error",
                    "message": "Role not found"
                }
                
            role = self.roles[role_id]
            has_perm = (
                "*" in role["permissions"] or
                permission in role["permissions"]
            )
            
            return {
                "status": "success",
                "has_permission": has_perm
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
            
    def _save_roles(self, roles: Dict):
        """Save roles to file"""
        with open(self.roles_file, 'w') as f:
            json.dump(roles, f, indent=2)
            
    def _save_permissions(self, permissions: Dict):
        """Save permissions to file"""
        with open(self.permissions_file, 'w') as f:
            json.dump(permissions, f, indent=2)
