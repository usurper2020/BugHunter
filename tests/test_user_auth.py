import unittest
import json
import os
from unittest.mock import patch, mock_open
from services.user_auth import UserAuth

class TestUserAuth(unittest.TestCase):
    def setUp(self):
        """Set up test cases"""
        self.auth = UserAuth()
        self.test_user = {
            'username': 'testuser',
            'password': 'Test@123',
            'role': 'user'
        }
        self.test_admin = {
            'username': 'admin',
            'password': 'Admin@123',
            'role': 'admin'
        }

    @patch('builtins.open', new_callable=mock_open, read_data='{}')
    def test_user_registration(self, mock_file):
        """Test user registration functionality"""
        result = self.auth.register_user(
            self.test_user['username'],
            self.test_user['password'],
            self.test_user['role']
        )
        
        self.assertEqual(result['status'], 'success')
        self.assertIn('message', result)
        mock_file.assert_called()

    @patch('builtins.open', new_callable=mock_open)
    def test_duplicate_registration(self, mock_file):
        """Test registration with existing username"""
        mock_file.return_value.read.return_value = json.dumps({
            'testuser': {
                'password': 'hashedpassword',
                'role': 'user',
                'created_at': '2024-01-01T00:00:00'
            }
        })
        
        result = self.auth.register_user(
            self.test_user['username'],
            self.test_user['password']
        )
        
        self.assertEqual(result['status'], 'error')
        self.assertIn('message', result)
        self.assertIn('exists', result['message'].lower())

    def test_password_validation(self):
        """Test password validation rules"""
        weak_passwords = ['short', '12345678', 'password', 'abcdefgh']
        
        for password in weak_passwords:
            result = self.auth.register_user('testuser', password)
            self.assertEqual(result['status'], 'error')
            self.assertIn('password', result['message'].lower())

    @patch('builtins.open', new_callable=mock_open)
    def test_user_login(self, mock_file):
        """Test user login functionality"""
        # Mock stored user data with hashed password
        stored_password = self.auth.hash_password(self.test_user['password'])
        mock_file.return_value.read.return_value = json.dumps({
            'testuser': {
                'password': stored_password,
                'role': 'user',
                'created_at': '2024-01-01T00:00:00'
            }
        })
        
        result = self.auth.login(
            self.test_user['username'],
            self.test_user['password']
        )
        
        self.assertEqual(result['status'], 'success')
        self.assertIn('token', result)

    def test_invalid_login(self):
        """Test login with invalid credentials"""
        result = self.auth.login('nonexistent', 'wrongpassword')
        self.assertEqual(result['status'], 'error')
        self.assertIn('invalid', result['message'].lower())

    def test_token_verification(self):
        """Test JWT token verification"""
        # Generate a valid token first
        token_result = self.auth.login(
            self.test_user['username'],
            self.test_user['password']
        )
        
        if token_result['status'] == 'success':
            token = token_result['token']
            verify_result = self.auth.verify_token(token)
            
            self.assertEqual(verify_result['status'], 'success')
            self.assertIn('payload', verify_result)
            self.assertEqual(
                verify_result['payload']['username'],
                self.test_user['username']
            )

    def test_invalid_token(self):
        """Test verification of invalid token"""
        result = self.auth.verify_token('invalid.token.here')
        self.assertEqual(result['status'], 'error')
        self.assertIn('invalid', result['message'].lower())

    @patch('builtins.open', new_callable=mock_open)
    def test_password_change(self, mock_file):
        """Test password change functionality"""
        # Mock stored user data
        stored_password = self.auth.hash_password(self.test_user['password'])
        mock_file.return_value.read.return_value = json.dumps({
            'testuser': {
                'password': stored_password,
                'role': 'user',
                'created_at': '2024-01-01T00:00:00'
            }
        })
        
        result = self.auth.change_password(
            self.test_user['username'],
            self.test_user['password'],
            'NewPassword@123'
        )
        
        self.assertEqual(result['status'], 'success')
        mock_file.assert_called()

    @patch('builtins.open', new_callable=mock_open)
    def test_admin_privileges(self, mock_file):
        """Test admin role privileges"""
        mock_file.return_value.read.return_value = json.dumps({
            'admin': {
                'password': self.auth.hash_password(self.test_admin['password']),
                'role': 'admin',
                'created_at': '2024-01-01T00:00:00'
            }
        })
        
        # Test admin login
        login_result = self.auth.login(
            self.test_admin['username'],
            self.test_admin['password']
        )
        
        self.assertEqual(login_result['status'], 'success')
        self.assertTrue(self.auth.is_admin(self.test_admin['username']))

    def test_role_validation(self):
        """Test role validation"""
        invalid_roles = ['superuser', 'moderator', '']
        
        for role in invalid_roles:
            result = self.auth.register_user(
                'testuser',
                'Test@123',
                role
            )
            self.assertEqual(result['status'], 'error')
            self.assertIn('role', result['message'].lower())

if __name__ == '__main__':
    unittest.main()
