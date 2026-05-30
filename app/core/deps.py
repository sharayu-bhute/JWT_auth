from app.core.database import SessionLocal
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer
from app.core.config import SECRET_KEY, ALGORITHM
from app.core.token_blacklist import blacklist

security = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token : str= Depends(security)):
    try:
        if token.credentials in blacklist:
            raise HTTPException(status_code=401, detail="Token revoked")
        payload= jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        role = payload.get("role")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        
        return {"email": email, "role": role}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token or token expired")

def require_admin(user=Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user