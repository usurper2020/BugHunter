import json
import hashlib
import os
from datetime import datetime, timedelta
import jwt

class UserAuth:
    def __init__(self):
        self.users_file = 'data/users.json'
        self.secret_key = 'your-secret-key'  # In production, this should be stored securely
        self.create_users_directory()

    def create_users_directory(self):
        """Create the data directory if it doesn't exist"""
        os.makedirs(os.path.dirname(self.users_file), exist_ok=True)
        if not os.path.exists(self.users_file):
            with open(self.users_file, 'w') as f:
                json.dump({}, f)

    def hash_password(self, password):
        """Hash a password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, username, password, role='user'):
        """Register a new user"""
        try:
            with open(self.users_file, 'r') as f:
                users = json.load(f)

            if username in users:
                return {
                    'status': 'error',
                    'message': 'Username already exists'
                }

            users[username] = {
                'password': self.hash_password(password),
                'role': role,
                'created_at': datetime.now().isoformat()
            }

            with open(self.users_file, 'w') as f:
                json.dump(users, f)

            return {
                'status': 'success',
                'message': 'User registered successfully'
            }

        except Exception as e:
            return {
                'status': 'error',
                'message': f'Registration failed: {str(e)}'
            }

    def login(self, username, password):
        """Login a user and return a JWT token"""
        try:
            with open(self.users_file, 'r') as f:
                users = json.load(f)

            if username not in users:
                return {
                    'status': 'error',
                    'message': 'Invalid username or password'
                }

            if users[username]['password'] != self.hash_password(password):
                return {
                    'status': 'error',
                    'message': 'Invalid username or password'
                }

            # Generate JWT token
            token = jwt.encode({
                'username': username,
                'role': users[username]['role'],
                'exp': datetime.utcnow() + timedelta(days=1)
            }, self.secret_key, algorithm='HS256')

            return {
                'status': 'success',
                'message': 'Login successful',
                'token': token
            }

        except Exception as e:
            return {
                'status': 'error',
                'message': f'Login failed: {str(e)}'
            }

    def verify_token(self, token):
        """Verify a JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return {
                'status': 'success',
                'payload': payload
            }
        except jwt.ExpiredSignatureError:
            return {
                'status': 'error',
                'message': 'Token has expired'
            }
        except jwt.InvalidTokenError:
            return {
                'status': 'error',
                'message': 'Invalid token'
            }

    def change_password(self, username, old_password, new_password):
        """Change a user's password"""
        try:
            with open(self.users_file, 'r') as f:
                users = json.load(f)

            if username not in users:
                return {
                    'status': 'error',
                    'message': 'User not found'
                }

            if users[username]['password'] != self.hash_password(old_password):
                return {
                    'status': 'error',
                    'message': 'Invalid password'
                }

            users[username]['password'] = self.hash_password(new_password)
            users[username]['updated_at'] = datetime.now().isoformat()

            with open(self.users_file, 'w') as f:
                json.dump(users, f)

            return {
                'status': 'success',
                'message': 'Password changed successfully'
            }

        except Exception as e:
            return {
                'status': 'error',
                'message': f'Password change failed: {str(e)}'
            }

    def get_user_role(self, username):
        """Get a user's role"""
        try:
            with open(self.users_file, 'r') as f:
                users = json.load(f)

            if username not in users:
                return None

            return users[username]['role']

        except Exception:
            return None

    def is_admin(self, username):
        """Check if a user is an admin"""
        return self.get_user_role(username) == 'admin'
