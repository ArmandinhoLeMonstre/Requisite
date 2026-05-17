from fastapi import APIRouter, Depends, status, Request

from typing import Annotated

from app.schemas.inventory_schemas import ObjectRequest

from app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.user_services import CurrentUser
from app.services.inventory_services import add_object

router = APIRouter()

@router.post("/add", status_code=status.HTTP_201_CREATED)
async def add_object_in_inventory(object: ObjectRequest, current_user: CurrentUser, db: Annotated[AsyncSession, Depends(get_db)]):
	await add_object(object, current_user, db)
	return {"object" : "added"}