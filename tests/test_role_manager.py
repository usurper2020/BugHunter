import unittest
from role_manager import RoleManager

class TestRoleManager(unittest.TestCase):
    def setUp(self):
        """Set up test cases"""
        self.role_manager = RoleManager()
        self.test_roles = {
            'admin': ['scan_targets', 'manage_tools', 'manage_users'],
            'user': ['scan_targets', 'view_reports'],
            'guest': ['view_reports']
        }

    def test_role_initialization(self):
        """Test role manager initialization"""
        self.assertIsNotNone(self.role_manager.roles)
        self.assertIn('admin', self.role_manager.roles)
        self.assertIn('user', self.role_manager.roles)
        self.assertIn('guest', self.role_manager.roles)

    def test_get_permissions(self):
        """Test getting permissions for roles"""
        admin_permissions = self.role_manager.get_permissions('admin')
        user_permissions = self.role_manager.get_permissions('user')
        guest_permissions = self.role_manager.get_permissions('guest')

        # Admin permissions
        self.assertIn('scan_targets', admin_permissions)
        self.assertIn('manage_tools', admin_permissions)
        self.assertIn('manage_users', admin_permissions)

        # User permissions
        self.assertIn('scan_targets', user_permissions)
        self.assertIn('view_reports', user_permissions)
        self.assertNotIn('manage_users', user_permissions)

        # Guest permissions
        self.assertIn('view_reports', guest_permissions)
        self.assertNotIn('scan_targets', guest_permissions)
        self.assertNotIn('manage_tools', guest_permissions)

    def test_has_permission(self):
        """Test permission checking for roles"""
        # Admin permissions
        self.assertTrue(self.role_manager.has_permission('admin', 'manage_users'))
        self.assertTrue(self.role_manager.has_permission('admin', 'scan_targets'))
        self.assertTrue(self.role_manager.has_permission('admin', 'view_reports'))

        # User permissions
        self.assertTrue(self.role_manager.has_permission('user', 'scan_targets'))
        self.assertTrue(self.role_manager.has_permission('user', 'view_reports'))
        self.assertFalse(self.role_manager.has_permission('user', 'manage_users'))

        # Guest permissions
        self.assertTrue(self.role_manager.has_permission('guest', 'view_reports'))
        self.assertFalse(self.role_manager.has_permission('guest', 'scan_targets'))
        self.assertFalse(self.role_manager.has_permission('guest', 'manage_tools'))

    def test_check_permission(self):
        """Test permission validation"""
        # Valid role and permission
        self.assertTrue(
            self.role_manager.check_permission('admin', 'manage_users'))
        
        # Invalid role
        self.assertFalse(
            self.role_manager.check_permission('invalid_role', 'view_reports'))
        
        # Invalid permission
        self.assertFalse(
            self.role_manager.check_permission('user', 'invalid_permission'))
        
        # None values
        self.assertFalse(self.role_manager.check_permission(None, 'view_reports'))
        self.assertFalse(self.role_manager.check_permission('user', None))

    def test_get_available_features(self):
        """Test getting available features for roles"""
        admin_features = self.role_manager.get_available_features('admin')
        user_features = self.role_manager.get_available_features('user')
        guest_features = self.role_manager.get_available_features('guest')

        # Admin features
        self.assertIn('scan_targets', admin_features)
        self.assertIn('manage_tools', admin_features)
        self.assertIn('manage_users', admin_features)

        # User features
        self.assertIn('scan_targets', user_features)
        self.assertIn('view_reports', user_features)
        self.assertNotIn('manage_users', user_features)

        # Guest features
        self.assertIn('view_reports', guest_features)
        self.assertNotIn('manage_tools', guest_features)

    def test_is_admin(self):
        """Test admin role checking"""
        self.assertTrue(self.role_manager.is_admin('admin'))
        self.assertFalse(self.role_manager.is_admin('user'))
        self.assertFalse(self.role_manager.is_admin('guest'))
        self.assertFalse(self.role_manager.is_admin('invalid_role'))

    def test_can_manage_users(self):
        """Test user management permission"""
        self.assertTrue(self.role_manager.can_manage_users('admin'))
        self.assertFalse(self.role_manager.can_manage_users('user'))
        self.assertFalse(self.role_manager.can_manage_users('guest'))

    def test_can_manage_tools(self):
        """Test tool management permission"""
        self.assertTrue(self.role_manager.can_manage_tools('admin'))
        self.assertFalse(self.role_manager.can_manage_tools('user'))
        self.assertFalse(self.role_manager.can_manage_tools('guest'))

    def test_can_view_reports(self):
        """Test report viewing permission"""
        self.assertTrue(self.role_manager.can_view_reports('admin'))
        self.assertTrue(self.role_manager.can_view_reports('user'))
        self.assertTrue(self.role_manager.can_view_reports('guest'))

    def test_can_scan_targets(self):
        """Test scanning permission"""
        self.assertTrue(self.role_manager.can_scan_targets('admin'))
        self.assertTrue(self.role_manager.can_scan_targets('user'))
        self.assertFalse(self.role_manager.can_scan_targets('guest'))

    def test_can_train_ai(self):
        """Test AI training permission"""
        self.assertTrue(self.role_manager.can_train_ai('admin'))
        self.assertFalse(self.role_manager.can_train_ai('user'))
        self.assertFalse(self.role_manager.can_train_ai('guest'))

    def test_can_manage_scope(self):
        """Test scope management permission"""
        self.assertTrue(self.role_manager.can_manage_scope('admin'))
        self.assertFalse(self.role_manager.can_manage_scope('user'))
        self.assertFalse(self.role_manager.can_manage_scope('guest'))

    def test_invalid_role_handling(self):
        """Test handling of invalid roles"""
        self.assertEqual(
            self.role_manager.get_permissions('invalid_role'),
            self.role_manager.get_permissions('guest')
        )
        self.assertFalse(self.role_manager.has_permission('invalid_role', 'view_reports'))

    def test_permission_inheritance(self):
        """Test permission inheritance between roles"""
        # Admin should have all user permissions
        user_permissions = self.role_manager.get_permissions('user')
        admin_permissions = self.role_manager.get_permissions('admin')
        
        for permission in user_permissions:
            self.assertIn(permission, admin_permissions)

        # User should have all guest permissions
        guest_permissions = self.role_manager.get_permissions('guest')
        for permission in guest_permissions:
            self.assertIn(permission, user_permissions)

if __name__ == '__main__':
    unittest.main()
