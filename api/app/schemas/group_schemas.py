from pydantic import BaseModel, ConfigDict
from app.schemas.user_schemas import UserResponse


class GroupBase(BaseModel):
	manager_id: int


class GroupCreate(GroupBase):
	pass


class GroupResponse(GroupBase):
	model_config = ConfigDict(from_attributes=True)

	id: int
	code: str
	users: list["UserResponse"]
	