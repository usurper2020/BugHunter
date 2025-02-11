import logging
import jwt
import datetime
import os

class UserAuth:
    def __init__(self):
        self.logged_in = False
        self.username = None
        self.token = None
        self.logger = logging.getLogger('BugHunter.UserAuth')
        self.secret_key = os.getenv('JWT_SECRET_KEY', 'your-secret-key-here')

    def login(self, username, password):
        """
        Authenticate user and generate token
        Returns: dict with status and token if successful
        """
        try:
            # TODO: Implement actual authentication
            # For now, accept any non-empty credentials
            if username and password:
                self.logged_in = True
                self.username = username
                
                # Generate JWT token
                token_data = {
                    'username': username,
                    'role': 'user',
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
                }
                self.token = jwt.encode(token_data, self.secret_key, algorithm='HS256')
                
                return {
                    'status': 'success',
                    'token': self.token,
                    'message': 'Login successful'
                }
                
            return {
                'status': 'error',
                'message': 'Invalid credentials'
            }
            
        except Exception as e:
            self.logger.error(f"Login error: {e}")
            return {
                'status': 'error',
                'message': str(e)
            }

    def verify_token(self, token):
        """
        Verify JWT token
        Returns: dict with status and payload if successful
        """
        try:
            if not token:
                return {
                    'status': 'error',
                    'message': 'No token provided'
                }
                
            # Verify and decode token
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            
            return {
                'status': 'success',
                'payload': payload,
                'message': 'Token verified'
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
        except Exception as e:
            self.logger.error(f"Token verification error: {e}")
            return {
                'status': 'error',
                'message': str(e)
            }

    def logout(self):
        """Logout current user"""
        try:
            self.logged_in = False
            self.username = None
            self.token = None
            return {
                'status': 'success',
                'message': 'Logout successful'
            }
        except Exception as e:
            self.logger.error(f"Logout error: {e}")
            return {
                'status': 'error',
                'message': str(e)
            }
