"""
RevokedToken model - stores blacklisted JWT tokens
"""
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base


class RevokedToken(Base):
    """
    RevokedToken model for storing blacklisted JWT tokens.

    When a user logs out, their token is added here to prevent reuse.
    """
    __tablename__ = "revoked_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token_jti = Column(String(255), unique=True, index=True, nullable=False)
    revoked_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<RevokedToken(jti='{self.token_jti}', revoked_at='{self.revoked_at}')>"
