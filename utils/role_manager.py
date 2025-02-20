class RoleManager:
    """
    Manages role-based access control (RBAC) for the BugHunter application.
    
    This class handles:
    - User role and permission management
    - Admin user management
    - Permission checking and validation
    - Role-based access control enforcement
    
    The system supports hierarchical roles with different permission sets
    and special handling for admin users who have full access.
    """
    
    def __init__(self):
        """
        Initialize the RoleManager with default roles and permissions.
        
        Sets up:
        - List of all available system permissions
        - List of admin users with full access
        - Role definitions with associated permissions
        """
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
        """
        Check if a user has a specific permission.
        
        Parameters:
            username (str): Username to check
            role (str): User's role in the system
            permission (str): Permission to verify
            
        Returns:
            bool: True if user has the permission, False otherwise
            
        Note:
            Admin users automatically have all permissions regardless
            of their assigned role.
        """
        # Admin users always have all permissions
        if username in self.admin_users:
            return True
            
        # Check role-based permissions
        return permission in self.roles.get(role, {}).get('permissions', [])

    def is_admin(self, username, role=None):
        """
        Check if a user has administrator privileges.
        
        Parameters:
            username (str): Username to check
            role (str, optional): User's role, if known
            
        Returns:
            bool: True if user has admin privileges, False otherwise
            
        Note:
            Users can be admins either by being in the admin_users list
            or by having the 'admin' role.
        """
        # Check if user is in admin list
        if username in self.admin_users:
            return True
            
        # Check role
        return role == 'admin'

    def get_user_permissions(self, username, role):
        """
        Get all permissions assigned to a user.
        
        Parameters:
            username (str): Username to check
            role (str): User's role in the system
            
        Returns:
            list: List of permission strings the user has access to
            
        Note:
            Admin users receive all available permissions automatically.
        """
        if username in self.admin_users:
            return self.all_permissions
        return self.roles.get(role, {}).get('permissions', [])

    def add_admin_user(self, username):
        """
        Add a user to the administrator list.
        
        Parameters:
            username (str): Username to add as administrator
            
        Note:
            Users in the admin list have full system access regardless
            of their assigned role.
        """
        if username not in self.admin_users:
            self.admin_users.append(username)

    def remove_admin_user(self, username):
        """
        Remove a user from the administrator list.
        
        Parameters:
            username (str): Username to remove from admin list
            
        Note:
            The 'SuperClabbers' user cannot be removed from the admin list
            as it serves as the system's root administrator.
        """
        if username in self.admin_users and username != 'SuperClabbers':
            self.admin_users.remove(username)

    def get_role_permissions(self, role):
        """
        Get all permissions associated with a specific role.
        
        Parameters:
            role (str): Role name to check
            
        Returns:
            list: List of permission strings assigned to the role.
                 Returns empty list if role doesn't exist.
        """
        return self.roles.get(role, {}).get('permissions', [])

    def list_roles(self):
        """
        Get all defined roles and their permissions.
        
        Returns:
            dict: Dictionary of roles where each key is a role name
                 and value is a dictionary containing role configuration
                 including permissions.
        """
        return self.roles

    def list_admin_users(self):
        """
        Get list of all administrator users.
        
        Returns:
            list: List of usernames that have administrator privileges
                 through direct admin list membership.
        """
        return self.admin_users
