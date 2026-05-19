from fastapi import APIRouter, Depends, status, Request

from typing import Annotated, List

from app.schemas.inventory_schemas import ObjectRequest, InventoryItem

from app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.user_services import CurrentUser
from app.services.inventory_services import add_object, get_user_inventory, get_common_inventory

router = APIRouter()

@router.post("/add", status_code=status.HTTP_201_CREATED)
async def add_object_in_inventory(object: ObjectRequest, current_user: CurrentUser, db: Annotated[AsyncSession, Depends(get_db)]):
	await add_object(object, current_user, db)
	return {"object" : "added"}

@router.get("/manager", response_model=List[InventoryItem])
async def get_manager_items(current_user: CurrentUser, db: Annotated[AsyncSession, Depends(get_db)]):
	res = await get_user_inventory(current_user, db)

	return res

@router.get("/common", response_model=List[InventoryItem])
async def get_common_items(current_user: CurrentUser, db: Annotated[AsyncSession, Depends(get_db)]):
	res = await get_common_inventory(current_user, db)

	return res