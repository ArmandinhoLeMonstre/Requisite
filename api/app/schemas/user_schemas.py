from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
from app.models.user_model import UserRole
from typing import Optional, Annotated
from app.schemas.ticket_schemas import TicketResponse


class UserBase(BaseModel):
	name: str = Field(min_length=1, max_length=50)
	email: EmailStr = Field(max_length=120)
	role: UserRole


class UserCreate(UserBase):
	password: str = Field()

	@field_validator('password')
	@classmethod
	def validate_password(cls, v):
		if len(v) < 4:
			raise ValueError('Password Incorrect')
		return v

	
class UserUpdate(UserBase):
	model_config = ConfigDict(from_attributes=True, )

	name: str | None = Field(default=None, min_length=1, max_length=50)
	email: EmailStr | None = Field(default=None, max_length=120)
	role: UserRole | None = Field(default=None)
	group_code: int | None = Field(default=None)


class UserPublic(BaseModel):
	model_config = ConfigDict(from_attributes=True)

	id: int
	name: str
	role: UserRole
	group_id: Optional[int] = None
	tickets: list[TicketResponse]


class UserPrivate(UserPublic):
	email: EmailStr


class UserGroup(BaseModel):
	model_config = ConfigDict(from_attributes=True)

	id: int
	name: str
	role: UserRole
	group_id: Optional[int] = None


class Token(BaseModel):
	access_token: str
	token_type: str	
