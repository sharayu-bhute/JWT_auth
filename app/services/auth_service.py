from sqlalchemy.orm import Session
from app.models.user import User
from fastapi import HTTPException
from app.core.security import verify_password
from app.core.jwt import create_access_token, create_refresh_token
from app.schemas import user

max_failed_attempts = 5

def authenticate_user(db: Session , email: str, password: str):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return None
    if user.is_locked:
        raise HTTPException(status_code=403, detail="Account is locked due to multiple failed login attempts")
    
    if not verify_password(password, user.password):
        user.failed_attempts += 1
        if user.failed_attempts >= max_failed_attempts:
            user.is_locked = True
        db.commit()
        return None

    user.failed_attempts = 0
    db.commit()

    access_token = create_access_token({
    "sub": user.email,
    "role": user.role
    })

    refresh_token = create_refresh_token({
    "sub": user.email
    })
    
    return {
    "access_token": access_token,
    "refresh_token": refresh_token,
    "token_type": "bearer"
    }