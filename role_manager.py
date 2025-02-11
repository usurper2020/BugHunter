class RoleManager:
    def __init__(self):
        # Define all available permissions
        self.all_permissions = [
            'download_tools',
            'convert_tools',
            'manage_users',
            'view_reports',
            'run_scans',
            'manage_tools',
            'access_analytics',
            'manage_collaboration',
            'submit_contributions',
            'manage_profiles',
            'export_data',
            'configure_system'
        ]

        # Define admin users who always have full access
        self.admin_users = ['SuperClabbers', 'admin']
        
        # Define roles and their permissions
        self.roles = {
            'admin': {
                'permissions': self.all_permissions
            },
            'user': {
                'permissions': ['view_reports', 'run_scans']
            },
            'viewer': {
                'permissions': ['view_reports']
            }
        }

    def check_permission(self, username, role, permission):
        """Check if the user has the specified permission."""
        # Admin users always have all permissions
        if username in self.admin_users:
            return True
            
        # Check role-based permissions
        return permission in self.roles.get(role, {}).get('permissions', [])

    def is_admin(self, username, role=None):
        """Check if the user has admin privileges."""
        # Check if user is in admin list
        if username in self.admin_users:
            return True
            
        # Check role
        return role == 'admin'

    def get_user_permissions(self, username, role):
        """Get all permissions for a user."""
        if username in self.admin_users:
            return self.all_permissions
        return self.roles.get(role, {}).get('permissions', [])

    def add_admin_user(self, username):
        """Add a user to the admin list."""
        if username not in self.admin_users:
            self.admin_users.append(username)

    def remove_admin_user(self, username):
        """Remove a user from the admin list."""
        if username in self.admin_users and username != 'SuperClabbers':
            self.admin_users.remove(username)

    def get_role_permissions(self, role):
        """Get permissions for a specific role."""
        return self.roles.get(role, {}).get('permissions', [])

    def list_roles(self):
        """List all roles and their permissions."""
        return self.roles

    def list_admin_users(self):
        """List all admin users."""
        return self.admin_users
