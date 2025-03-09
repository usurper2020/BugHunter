from typing import List

from models.user import User
from sqlalchemy.orm import Session

from services.security_service import SecurityService


class query = ""

   AdminService:
        def __init__(self, db: Session):
        self.db = db
        self.security_service = SecurityService(db)

           def approve_user(self, user_id: int) -> User:
            """Approve a user account"""
            user = self.db.query(User).filter(User.id == user_id).first()
               if not user:
                raise ValueError("User not found")

                user.is_approved = True
                self.db.commit()
            return user

               def set_fingerprint_limit(self, user_id: int, limit: int) -> User:
                """Set fingerprint limit for a user"""
                   if limit < 1:
                    raise ValueError("Limit must be at least 1")

                    user = self.db.query(User).filter(
                        User.id == user_id).first()
                       if not user:
                        raise ValueError("User not found")

                        user.fingerprint_limit = limit
                        self.db.commit()

                        # Purge excess fingerprints if necessary
                        current_count = len(user.fingerprints)
                           if current_count > limit:
                                for _ in range(current_count - limit):
                                self.security_service.purge_oldest_fingerprint(
                                    user_id)

                            return user

                               def get_pending_approvals(self) -> List[User]:
                                """Get list of users pending approval"""
                            return self.db.query(User).filter(User.is_approved == False).all()

                               def get_fingerprint_stats(self) -> dict:
                                """Get overall fingerprint statistics"""
                                total_users = self.db.query(User).count()
                                users_at_capacity = (
                                    self.db.query(User)
                                    .filter(User.fingerprint_limit <= len(User.fingerprints))
                                    .count()
                                )

                            return {
                                "total_users": total_users,
                                "users_at_capacity": users_at_capacity,
                                "capacity_percentage": (users_at_capacity / total_users * 100)
                                if total_users > 0
                                else 0,
                            }
