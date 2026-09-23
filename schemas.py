from pydantic import BaseModel


# Pydantic model for creating and updating clothes
class ClothesCreate(BaseModel):
    name: str
    size: str
    quantity: int
    price: float