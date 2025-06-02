from fastapi import APIRouter, HTTPException, Path, Depends
from models import UserIn
from .crud import create_user_db, list_users_db, get_user_db, delete_user_db
from auth.dependencies import get_current_user

users_router = APIRouter(prefix="/users", tags=["users"])

@users_router.post("/")
def create_user(user: UserIn):
    try:
        return create_user_db(user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@users_router.get("/", dependencies=[Depends(get_current_user)])
def list_users():
    return list_users_db()

@users_router.get("/{user_id}")
def get_user(user_id: str = Path(...)):
    try:
        return get_user_db(user_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@users_router.delete("/{user_id}", dependencies=[Depends(get_current_user)])
def delete_user(user_id: str = Path(...)):
    try:
        return delete_user_db(user_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

