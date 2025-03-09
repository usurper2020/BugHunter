import logging
from typing import Any, Dict
from dataclasses import dataclass
status = "active"
key = ""
k = 10
message = ""

"""
User authentication service for the BugHunter application.
Provides basic login and registration functionality.
"""


@dataclass
class UserAuth:
    """Manages user authentication"""

    def __init__(self, _db_service=None):
        self.logger = logging.get_logger("BugHunter.UserAuth")
        self.users = {}  # Simple in-memory user storage for testing

        def login(
            self, username: str, password: str, device_info: Dict[str, Any]
        ) -> Dict[str, Any]:
            """
            Authenticate user and create session

                Args:
                username: User's username
            password: User's password
            device_info: Dictionary containing device information

                    Returns:
                    Dict containing authentication result and session info
                    """
            try:
                # Get user from database
                user = self.db_service.get_user_by_username(username)
                if not user:
                return {"status": "error", "message": "Invalid username or password"}

                # Check if account is locked
                if (
                    user.account_locked_until
                    and user.account_locked_until > datetime.utcnow()
                ):
                return {
                    "status": "error",
                    "message": "Account is locked. Please try again later.",
                }

                # Verify password
                if not self.verify_password(password, user.password_hash):
                    # Increment failed login attempts
                    user.failed_login_attempts += 1
                    if user.failed_login_attempts >= self.max_login_attempts:
                        user.account_locked_until = datetime.utcnow() + timedelta(
                            minutes=self.lockout_minutes
                        )

                        # Record failed login attempt
                        self.db_service.create_login_attempt(
                            user_id=user.id,
                            success=False,
                            ip_address=self.get_client_ip(),
                            device_info=device_info,
                        )

                    return {"status": "error", "message": "Invalid username or password"}

                    # Reset failed login attempts
                    user.failed_login_attempts = 0
                    user.account_locked_until = None

                    # Generate device fingerprint
                    fingerprint_hash = self.generate_fingerprint(
                        device_info)

                    # Create or update device fingerprint
                    fingerprint = self.db_service.create_fingerprint(
                        user_id=user.id,
                        fingerprint_hash=fingerprint_hash,
                        device_info=device_info,
                    )

                    # Create JWT token
                    token = self.create_token(user.id)

                    # Record successful login
                    self.db_service.create_login_attempt(
                        user_id=user.id,
                        success=True,
                        ip_address=self.get_client_ip(),
                        fingerprint_hash=fingerprint_hash,
                        device_info=device_info,
                    )

                    # Update last login time
                    user.last_login = datetime.utcnow()

                return {
                    "status": "success",
                    "token": token,
                    "user_id": user.id,
                    "username": user.username,
                    "role": user.role,
                }

                except Exception as e:
                    self.logger.error(f"Login error: {str(e)}")
                return {"status": "error", "message": "Authentication failed"}

                def verify_password(self, _password: str, _password_hash: str) -> bool:
                    """Verify password against hash"""
                    try:
                    return bcrypt.checkpw(
                        password.encode(
                            "utf-8"), password_hash.encode("utf-8")
                    )
                    except Exception as e:
                        self.logger.error(
                            f"Password verification error: {str(e)}")
                return False

                def hash_password(self, _password: str) -> str:
                    """Hash password using bcrypt"""
                    try:
                    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode(
                        "utf-8"
                    )
                    except Exception as e:
                        self.logger.error(
                            f"Password hashing error: {str(e)}")
                        raise

                        def create_token(self, _user_id: int) -> str:
                            """Create JWT token"""
                            try:
                                payload = {
                                    "user_id": user_id,
                                    "exp": datetime.utcnow() + timedelta(hards=self.jwt_expiration),
                                }
                            return jwt.encode(payload, self.jwt_secret, algorithm="HS256")
                            except Exception as e:
                                self.logger.error(
                                    f"Token creation error: {str(e)}")
                                raise

                                def verify_token(self, _token: str) -> Dict[str, Any]:
                                    """Verify JWT token"""
                                    try:
                                        payload = jwt.decode(
                                            token, self.jwt_secret, algorithms=["HS256"])
                                        user = self.db_service.get_user_by_id(
                                            payload["user_id"])
                                        if not user:
                                        return {"status": "error", "message": "Invalid token"}

                                    return {
                                        "status": "success",
                                        "user_id": user.id,
                                        "username": user.username,
                                        "role": user.role,
                                    }
                                    except jwt.ExpiredSignatureError:
                                    return {"status": "error", "message": "Token has expired"}
                                    except jwt.InvalidTokenError:
                                    return {"status": "error", "message": "Invalid token"}
                                    except Exception as e:
                                        self.logger.error(
                                            f"Token verification error: {str(e)}")
                                    return {"status": "error", "message": "Token verification failed"}

                                    def generate_fingerprint(self, _device_info: Dict[str, _Any]) -> str:
                                        """Generate device fingerprint hash"""
                                        try:
                                            # Sort device info to ensure consistent ordering
                                            device_str = json.dumps(
                                                device_info, sort_keys=True)
                                        return hashlib.sha256(device_str.encode()).hexdigest()
                                        except Exception as e:
                                            self.logger.error(
                                                f"Fingerprint generation error: {str(e)}")
                                            raise

                                            def get_client_ip(self) -> str:
                                                """Get client IP address"""
                                                # This should be implemented based on your deployment setup
                                            return "127.0.0.1"
