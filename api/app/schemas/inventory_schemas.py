from pydantic import BaseModel, Field

class ObjectRequest(BaseModel):
	title: str = Field(min_length=1, max_length=150)
	object_type: str = Field(min_length=1, max_length=20)
	object_specs: str = Field(min_length=1, max_length=100)
	quantity: int = Field(ge=0)

class InventoryItem(ObjectRequest):
	model_config = {"from_attributes": True}