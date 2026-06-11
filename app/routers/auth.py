from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.db.session import get_db
from app.models.user import User
from app.auth.utils import hash_password, verify_password
from app.auth.jwt import create_access_token
from app.schemas.auth import RegisterRequest
from app.auth.dependencies import get_current_user

router = APIRouter()

@router.post('/login')
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Неверные учетные данные")

    access_token = create_access_token(data={"sub": str(user.id), "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post('/register')
def register(request: RegisterRequest, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.username == request.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Пользователь уже существует")

    user = User(
        username=request.username,
        password_hash=hash_password(request.password),
        role="user"
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "Пользователь зарегистрирован"}

@router.get('/me')
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user



    