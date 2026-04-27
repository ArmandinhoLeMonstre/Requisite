from fastapi import APIRouter, Depends, status

from typing import Annotated

from app.init_db import get_db 
from sqlalchemy.orm import Session

from app.schemas.group_schemas import GroupCreate, GroupResponse
from app.services.group_services import create_group, select_group
from app.services.user_services import CurrentUser


router = APIRouter()

@router.post("", status_code=status.HTTP_201_CREATED, response_model=GroupResponse)
def post_new_group(current_user: CurrentUser, db: Annotated[Session, Depends(get_db)]):
    return create_group(current_user, db)

@router.get("/{group_id}", response_model=GroupResponse)
def get_group(group_id: int, current_user: CurrentUser,  db: Annotated[Session, Depends(get_db)]):
    return select_group(group_id, current_user, db)
