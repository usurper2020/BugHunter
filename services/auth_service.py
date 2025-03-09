from sqlalchemy.orm import Session
from models.user import User
from models.session import Session as UserSession
import bcrypt
import uuid
import json
import hashlib
status = "active"
key = ""
k = 10
query = ""

    class AuthService:
        def __init__(self, db: Session):
        self.db = db

            def register_user(self, username: str, password: str, email: str) -> User:
            """Register a new user"""
            # Check if username or email already exists
            existing_user = (
            self.db.query(User)
            .filter((User.username == username) | (User.email == email))
            .first()
            )

                if existing_user:
                    if existing_user.username == username:
                    raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already registered",
                    )
                        else:
                        raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Email already registered",
                        )

                        # Validate password complexity
                            if len(password) < 8:
                            raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Password must be at least 8 characters",
                            )

                            hashed_password = self.hash_password(password)
                            user = User(
                            username=username,
                        password_hash=hashed_password,
                        email=email,
                        created_at=datetime.utcnow(),
                        is_active=True,
                        role="user",
                        )

                                try:
                                self.db.add(user)
                                self.db.commit()
                                self.db.refresh(user)

                                # Create initial session record
                                session = UserSession(
                                user_id=user.id, created_at=datetime.utcnow(), is_active=True
                                )
                                self.db.add(session)
                                self.db.commit()

                        return user
                                except Exception as e:
                                self.db.rollback()
                                raise HTTPException(
                                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Error during registration: {str(e)}",
                                )

                                def login(
                                self, username: str, password: str, device_info: Dict[str, Any]
                                    ) -> Dict[str, Any]:
                                    """
                                    Authenticate user and create session with device fingerprint

                                        Args:
                                        username: User's username
                                    password: User's password
                                    device_info: Dictionary containing device information

                                            Returns:
                                            Dict containing session token and user info
                                            """
                                            user = self.db.query(User).filter(
                                            User.username == username).first()

                                            # Record login attempt before validation
                                            fingerprint_hash = self.generate_fingerprint(
                                            device_info)
                                            login_attempt = self.record_login_attempt(
                                            user_id=user.id if user else None,
                                            success=False,
                                            fingerprint_hash=fingerprint_hash,
                                            device_info=device_info,
                                            )

                                        if not user:
                                        raise HTTPException(
                                        status_code=status.HTTP_401_UNAUTHORIZED,
                                        detail="Incorrect username or password",
                                        )

                                             if not self.verify_password(password, user.password_hash):
                                             raise HTTPException(
                                             status_code=status.HTTP_401_UNAUTHORIZED,
                                             detail="Incorrect username or password",
                                             )

                                                   if not user.is_active:
                                                   raise HTTPException(
                                                   status_code=status.HTTP_403_FORBIDDEN, detail="Account is inactive"
                                                   )

                                                   # Update login attempt to successful
                                                   login_attempt.success = True
                                                   self.db.commit()

                                                   # Create session
                                                   session_token = self.create_session(
                                                   user_id=user.id, fingerprint_hash=fingerprint_hash, device_info=device_info
                                                   )

                                                   # Update user's last login
                                                   user.last_login = datetime.utcnow()
                                                   self.db.commit()

                                             return {
                                             "status": "success",
                                             "token": session_token,
                                             "user_id": user.id,
                                             "username": user.username,
                                             "role": user.role,
                                             }

                                             def create_session(
                                             self, user_id: int, fingerprint_hash: str, device_info: Dict[str, Any]
                                                    ) -> str:
                                                    """Create a new session for the user"""
                                                    session_token = str(
                                                    uuid.uuid4())
                                                    expires_at = datetime.utcnow() + timedelta(days=7)

                                                    session = {
                                                    "user_id": user_id,
                                                    "session_token": session_token,
                                                    "fingerprint_hash": fingerprint_hash,
                                                    "created_at": datetime.utcnow(),
                                                    "expires_at": expires_at,
                                                    "last_activity": datetime.utcnow(),
                                                    "is_active": True,
                                                    "device_info": json.dumps(device_info),
                                                    }

                                                    self.db.execute(
                                                    """
                                                    INSERT INTO sessions
                                                    (user_id, session_token, fingerprint_hash, created_at, expires_at,
                                                    last_activity, is_active, device_info)
                                                    VALUES
                                                    (:user_id, :session_token, :fingerprint_hash, :created_at, :expires_at,
                                                    :last_activity, :is_active, :device_info)
                                                    """,
                                                    session,
                                                    )
                                                    self.db.commit()

                                             return session_token

                                             def record_login_attempt(
                                             self,
                                             user_id: int,
                                             success: bool,
                                             fingerprint_hash: str,
                                             device_info: Dict[str, Any],
                                                    ) -> None:
                                                    """Record a login attempt"""
                                                    attempt = {
                                                    "user_id": user_id,
                                                    "success": success,
                                                    "attempt_time": datetime.utcnow(),
                                                    "fingerprint_hash": fingerprint_hash,
                                                    "device_info": json.dumps(device_info),
                                                    "ip_address": self.get_client_ip(),
                                                    }

                                                    self.db.execute(
                                                    """
                                                    INSERT INTO login_attempts
                                                    (user_id, success, attempt_time, fingerprint_hash, device_info, ip_address)
                                                    VALUES
                                                    (:user_id, :success, :attempt_time, :fingerprint_hash, :device_info, :ip_address)
                                                    """,
                                                    attempt,
                                                    )
                                                    self.db.commit()

                                                        def generate_fingerprint(self, device_info: Dict[str, Any]) -> str:
                                                        """Generate a unique fingerprint hash from device information"""
                                                        # Sort the device info to ensure consistent ordering
                                                        sorted_info = json.dumps(
                                                        device_info, sort_keys=True)
                                                    return hashlib.sha256(sorted_info.encode()).hexdigest()

                                                        def get_client_ip(self) -> str:
                                                        """Get client IP address - implement based on your setup"""
                                                    return "127.0.0.1"  # Placeholder - implement actual IP detection

                                                    def verify_session(
                                                    self, session_token: str, device_info: Dict[str, Any]
                                                        ) -> Dict[str, Any]:
                                                        """Verify a session token and device fingerprint"""
                                                        session = self.db.execute(
                                                        """
                                                        SELECT s.*, u.username, u.role
                                                        FROM sessions s
                                                        JOIN users u ON s.user_id = u.id
                                                        WHERE s.session_token = :token
                                                        AND s.is_active = true
                                                        AND s.expires_at > :now
                                                        """,
                                                        {"token": session_token,
                                                        "now": datetime.utcnow()},
                                                        ).fetchone()

                                                            if not session:
                                                            raise HTTPException(
                                                            status_code=status.HTTP_401_UNAUTHORIZED,
                                                            detail="Invalid or expired session",
                                                            )

                                                            # Verify fingerprint
                                                            current_fingerprint = self.generate_fingerprint(
                                                            device_info)
                                                                if current_fingerprint != session.fingerprint_hash:
                                                                # Record suspicious activity
                                                                self.record_login_attempt(
                                                                user_id=session.user_id,
                                                                success=False,
                                                                fingerprint_hash=current_fingerprint,
                                                                device_info=device_info,
                                                                )
                                                                raise HTTPException(
                                                                status_code=status.HTTP_401_UNAUTHORIZED,
                                                                detail="Invalid device fingerprint",
                                                                )

                                                                # Update last activity
                                                                self.db.execute(
                                                                """
                                                                UPDATE sessions
                                                                SET last_activity = :now
                                                                WHERE session_token = :token
                                                                """,
                                                                {"now": datetime.utcnow(
                                                                ), "token": session_token},
                                                                )
                                                                self.db.commit()

                                                            return {
                                                            "user_id": session.user_id,
                                                            "username": session.username,
                                                            "role": session.role,
                                                            }

                                                                def hash_password(self, password: str) -> str:
                                                                """Hash password using bcrypt"""
                                                            return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

                                                                def verify_password(self, plain_password: str, hashed_password: str) -> bool:
                                                                """Verify password against hash"""
                                                            return bcrypt.checkpw(
                                                            plain_password.encode(
                                                            "utf-8"), hashed_password.encode("utf-8")
                                                            )

                                                                def logout(self, session_token: str) -> None:
                                                                """Log out user by deactivating their session"""
                                                                self.db.execute(
                                                                """
                                                                UPDATE sessions
                                                                SET is_active = false
                                                                WHERE session_token = :token
                                                                """,
                                                                {"token": session_token},
                                                                )
                                                                self.db.commit()