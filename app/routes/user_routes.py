from fastapi import APIRouter, Depends, HTTPException,Request
from sqlalchemy.orm import Session
from app.core.config import ALGORITHM, SECRET_KEY
from app.core.jwt import create_access_token
from app.schemas.user import UserCreate, RefreshRequest
from app.services.auth_service import authenticate_user
from app.services.user_service import create_user
from app.core.deps import get_db, get_current_user, require_admin
from app.core.rate_limiter import is_rate_limited
from jose import jwt, JWTError
from app.core.token_blacklist import blacklist
from fastapi.security import HTTPBearer


security = HTTPBearer()
router = APIRouter()


@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    new_user = create_user(db, user)
    if not new_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return {"message" : "user created successfully"}

@router.post("/login")
def login( request: Request, credentials: UserCreate, db: Session = Depends(get_db)):
    ip = request.client.host
    if is_rate_limited(ip):
        raise HTTPException(status_code=429, detail="Too many login attempts. Please try again later.")
    token= authenticate_user(db, credentials.email, credentials.password)

    if not token:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return token

@router.get("/protected")
def protected_route(user: dict = Depends(get_current_user)):
    return {"message": f"Hello {user['email']}, you are authenticated!"}


@router.get("/admin")
def admin_panel(user: dict = Depends(require_admin)):
    return {"message": f"Welcome Admin {user['email']}"}


@router.post("/refresh")
def refresh_token(refresh_request: RefreshRequest):
    try:
        payload = jwt.decode(refresh_request.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        
        new_access_token = create_access_token({"sub": email})
        return {"access_token": new_access_token, "token_type": "bearer"}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token or token expired")


@router.post("/logout")
def logout(token=Depends(security)):
    blacklist.add(token.credentials)
    return {"message": "Successfully logged out"}
