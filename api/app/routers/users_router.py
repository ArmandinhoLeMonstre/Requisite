from fastapi import APIRouter, Depends, status

from typing import Annotated

from app.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user_schemas import UserCreate, UserPublic, UserUpdate, UserPrivate, Token
from app.services.user_services import create_user, select_user, patch_user, delete_user, get_current_user, CurrentUser
from app.services.token_services import log_for_access_token
from app.services.group_services import join_group

from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserPrivate)
async def post_new_user(user: UserCreate, db:Annotated[AsyncSession, Depends(get_db)]):
    return await create_user(user, db)

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
):
    return await log_for_access_token(form_data, db)

@router.get("/me", response_model=UserPrivate)
async def current_user(user : CurrentUser):
    return user

@router.get("/{user_id}", response_model=UserPublic)
async def get_user(current_user: CurrentUser, user_id: int, db:Annotated[AsyncSession, Depends(get_db)]):
    return await select_user(current_user, user_id, db)

@router.patch("/{user_id}", response_model=UserPrivate)
async def update_user(current_user: CurrentUser, user_id:int, new_data: UserUpdate, db: Annotated[AsyncSession, Depends(get_db)]):
    return await patch_user(current_user, user_id, new_data, db)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def del_user(current_user: CurrentUser, user_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    return await delete_user(current_user, user_id, db)

@router.patch("/{user_id}/group", response_model=UserPrivate)
async def change_group(current_user: CurrentUser,
                 db: Annotated[AsyncSession,Depends(get_db)],
                 code: str):
    await join_group(current_user, code, db)
    return current_user