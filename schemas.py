from decimal import Decimal
from pydantic import BaseModel, Field


# Pydantic model for creating and updating clothes
class ClothesCreate(BaseModel):
    name: str
    size: str
    quantity: int = Field(ge=0)
    price: Decimal


# Pydantic model for responses
class ClothesResponse(BaseModel):
    clothing_id: int
    name: str
    size: str
    quantity: int
    price: Decimal

    class Config:
        from_attributes = True