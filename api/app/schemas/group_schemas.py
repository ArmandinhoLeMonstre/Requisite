from pydantic import BaseModel, ConfigDict
from app.schemas.user_schemas import UserPublic


class GroupBase(BaseModel):
	pass


class GroupCreate(GroupBase):
	pass


class GroupResponse(GroupBase):
	model_config = ConfigDict(from_attributes=True)

	id: int
	code: str
	manager_id: int
	users: list["UserPublic"]
	