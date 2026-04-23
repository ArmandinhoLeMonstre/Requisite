from fastapi import APIRouter, Depends, status

from typing import Annotated

from app.init_db import get_db 
from sqlalchemy.orm import Session

from app.schemas.user_schemas import UserCreate, UserPublic, UserUpdate
from app.services.user_services import create_user, select_user, patch_user, delete_user


router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserPublic)
def post_new_user(user: UserCreate, db:Annotated[Session, Depends(get_db)]):
    return create_user(user, db)

@router.get("/{user_id}", response_model=UserPublic)
def get_user(user_id: int, db:Annotated[Session, Depends(get_db)]):
    return select_user(user_id, db)

@router.patch("/{user_id}", response_model=UserPublic)
def update_user(user_id:int, new_data: UserUpdate, db: Annotated[Session, Depends(get_db)]):
    return patch_user(user_id, new_data, db)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def del_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    return  delete_user(user_id, db)