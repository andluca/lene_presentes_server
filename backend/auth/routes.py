from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from .jwt import create_access_token
from users.crud import get_user_by_email
from utils.hash_password import verify_password

auth_router = APIRouter(prefix="/auth", tags=["auth"])

def authenticate_user(email: str, password: str):
    user = get_user_by_email(email)
    if not user:
        return None
    password_hash = user['password_hash']
    if verify_password(password, password_hash):
        return {"email": user['email'], "role": user['role']}
    return None

@auth_router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if user:
        token = create_access_token({"sub": user["email"]})
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")
