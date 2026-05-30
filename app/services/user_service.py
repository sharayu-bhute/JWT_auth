from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password

def create_user(db: Session, user: UserCreate):

    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        return None
    
    hased_password = hash_password(user.password)

    new_user = User(
        email=user.email, 
        password=hased_password)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
