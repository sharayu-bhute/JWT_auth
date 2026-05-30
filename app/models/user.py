from sqlalchemy import Boolean, Column, DateTime, Integer, String
from app.models.base import Base
from datetime import datetime, timezone

class User(Base):
    __tablename__="users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String, default="user")
    failed_attempts = Column(Integer, default=0)
    is_locked = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))