from sqlalchemy.orm import Session
import hashlib
k = 10
query = ""


class SecurityService:
    def __init__(self, db: Session):
        self.db = db

        def generate_fingerprint(
            self, user_agent: str, ip_address: str, screen_res: str, plugins: str
        ) -> str:
            """Generate device fingerprint hash"""
            fingerprint_data = f"{user_agent}{ip_address}{screen_res}{plugins}"
        return hashlib.sha256(fingerprint_data.encode("utf-8")).hexdigest()

        def store_fingerprint(
            self, user_id: int, fingerprint_hash: str, capture_type: str, device_info: str
        ) -> Fingerprint:
            """Store new fingerprint if it doesn't exist"""
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                raise ValueError("User not found")

                # Check if fingerprint already exists
                existing = (
                    self.db.query(Fingerprint)
                    .filter(
                        Fingerprint.user_id == user_id,
                        Fingerprint.fingerprint_hash == fingerprint_hash,
                    )
                    .first()
                )

                if existing:
                return existing

                # Check fingerprint limit
                if len(user.fingerprints) >= user.fingerprint_limit:
                    self.purge_oldest_fingerprint(user_id)

                    fingerprint = Fingerprint(
                        user_id=user_id,
                        fingerprint_hash=fingerprint_hash,
                        capture_type=capture_type,
                        device_info=device_info,
                    )

                    self.db.add(fingerprint)
                    self.db.commit()
                return fingerprint

                def purge_oldest_fingerprint(self, user_id: int) -> None:
                    """Remove the oldest unused fingerprint"""
                    oldest = (
                        self.db.query(Fingerprint)
                        .filter(Fingerprint.user_id == user_id)
                        .order_by(Fingerprint.created_at)
                        .first()
                    )

                    if oldest:
                        self.db.delete(oldest)
                        self.db.commit()

                        def get_fingerprint_stats(self, user_id: int) -> dict:
                            """Get fingerprint statistics for a user"""
                            user = self.db.query(User).filter(
                                User.id == user_id).first()
                            if not user:
                                raise ValueError("User not found")

                            return {
                                "current_count": len(user.fingerprints),
                                "limit": user.fingerprint_limit,
                                "oldest": min([f.created_at for f in user.fingerprints])
                                if user.fingerprints
                                else None,
                            }
