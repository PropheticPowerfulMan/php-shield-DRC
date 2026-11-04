"""Session-cookie authentication with no public account registration."""
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import CurrentUser, LoginRequest
from app.security import verify_password

router = APIRouter(prefix="/auth", tags=["authentication"])

def _public_user(user: User) -> CurrentUser:
    return CurrentUser(id=user.id, email=user.email, roles=[role.name for role in user.roles])

@router.post("/login", response_model=CurrentUser)
def login(body: LoginRequest, request: Request, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == body.email))
    if user is None or not user.is_active or not verify_password(body.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Identifiants invalides.")
    request.session.clear()
    request.session["user_id"] = str(user.id)
    return _public_user(user)

@router.get("/me", response_model=CurrentUser)
def current_user(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session absente.")
    try:
        user = db.get(User, UUID(user_id))
    except ValueError:
        user = None
    if user is None or not user.is_active:
        request.session.clear()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session invalide.")
    return _public_user(user)

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(request: Request):
    request.session.clear()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
