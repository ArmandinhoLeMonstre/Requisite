from fastapi import APIRouter, Depends, status

from typing import Annotated

from app.init_db import get_db 
from sqlalchemy.orm import Session

from app.schemas.user_schemas import UserCreate, UserPublic, UserUpdate, UserPrivate, Token
from app.services.user_services import create_user, select_user, patch_user, delete_user, get_current_user
from app.services.token_services import log_for_access_token

from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from app.auth import hash_password, oauth2_scheme, verify_password, create_access_token, verify_access_token
from app.config import settings

router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserPrivate)
def post_new_user(user: UserCreate, db:Annotated[Session, Depends(get_db)]):
    return create_user(user, db)

@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
):
    return log_for_access_token(form_data, db)

@router.get("/me", response_model=UserPrivate)
def current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Annotated[Session, Depends(get_db)]):
    return get_current_user(token, db)

@router.get("/{user_id}", response_model=UserPublic)
def get_user(user_id: int, db:Annotated[Session, Depends(get_db)]):
    return select_user(user_id, db)

@router.patch("/{user_id}", response_model=UserPrivate)
def update_user(user_id:int, new_data: UserUpdate, db: Annotated[Session, Depends(get_db)]):
    return patch_user(user_id, new_data, db)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def del_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    return  delete_user(user_id, db)