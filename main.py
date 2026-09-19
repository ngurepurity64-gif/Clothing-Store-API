from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Numeric
from sqlalchemy.orm import declarative_base, sessionmaker

# Create the FastAPI application
app = FastAPI()

# PostgreSQL database connection
# Keep your existing PostgreSQL password here
DATABASE_URL = "postgresql+psycopg://postgres:4455ttyy@localhost:5432/clothingstore"

# Create the database engine
engine = create_engine(DATABASE_URL)

# Create the base class for SQLAlchemy models
Base = declarative_base()

# Create a database session
SessionLocal = sessionmaker(bind=engine)


# Pydantic model for creating and updating clothes
class ClothesCreate(BaseModel):
    name: str
    size: str
    quantity: int
    price: float


# SQLAlchemy model for the clothes table
class Clothes(Base):
    __tablename__ = "clothes"

    clothing_id = Column(Integer, primary_key=True)
    name = Column(String)
    size = Column(String)
    quantity = Column(Integer)
    price = Column(Numeric)


# Health check endpoint
@app.get("/health")
def health():
    return {"status": "ok"}


# GET all clothes
@app.get("/clothes")
def get_clothes():
    # Open a database session
    db = SessionLocal()

    try:
        # Get all clothes from the database
        clothes_list = db.query(Clothes).all()

        # Return all clothes
        return [
            {
                "clothing_id": item.clothing_id,
                "name": item.name,
                "size": item.size,
                "quantity": item.quantity,
                "price": item.price
            }
            for item in clothes_list
        ]

    finally:
        # Close the database session
        db.close()


# GET one clothing item by ID
@app.get("/clothes/{clothing_id}")
def get_clothing(clothing_id: int):
    # Open a database session
    db = SessionLocal()

    try:
        # Find the clothing item
        clothing = db.query(Clothes).filter(
            Clothes.clothing_id == clothing_id
        ).first()

        # Return 404 if it does not exist
        if clothing is None:
            raise HTTPException(
                status_code=404,
                detail="Clothing item not found"
            )

        # Return the clothing item
        return {
            "clothing_id": clothing.clothing_id,
            "name": clothing.name,
            "size": clothing.size,
            "quantity": clothing.quantity,
            "price": clothing.price
        }

    finally:
        # Close the database session
        db.close()


# POST - Add new clothes
@app.post("/clothes")
def create_clothes(clothes_data: ClothesCreate):
    # Open a database session
    db = SessionLocal()

    try:
        # Create a new clothing record
        new_clothes = Clothes(
            name=clothes_data.name,
            size=clothes_data.size,
            quantity=clothes_data.quantity,
            price=clothes_data.price
        )

        # Add the record
        db.add(new_clothes)

        # Save it to PostgreSQL
        db.commit()

        # Get the generated ID
        db.refresh(new_clothes)

        # Return the new record
        return {
            "clothing_id": new_clothes.clothing_id,
            "name": new_clothes.name,
            "size": new_clothes.size,
            "quantity": new_clothes.quantity,
            "price": new_clothes.price
        }

    finally:
        # Close the database session
        db.close()


# PUT - Update one clothing item
@app.put("/clothes/{clothing_id}")
def update_clothing(clothing_id: int, clothes_data: ClothesCreate):
    # Open a database session
    db = SessionLocal()

    try:
        # Find the clothing item
        clothing = db.query(Clothes).filter(
            Clothes.clothing_id == clothing_id
        ).first()

        # Return 404 if it does not exist
        if clothing is None:
            raise HTTPException(
                status_code=404,
                detail="Clothing item not found"
            )

        # Update the clothing details
        clothing.name = clothes_data.name
        clothing.size = clothes_data.size
        clothing.quantity = clothes_data.quantity
        clothing.price = clothes_data.price

        # Save the changes
        db.commit()

        # Refresh the record
        db.refresh(clothing)

        # Return the updated record
        return {
            "clothing_id": clothing.clothing_id,
            "name": clothing.name,
            "size": clothing.size,
            "quantity": clothing.quantity,
            "price": clothing.price
        }

    finally:
        # Close the database session
        db.close()


# DELETE - Delete one clothing item
@app.delete("/clothes/{clothing_id}")
def delete_clothing(clothing_id: int):
    # Open a database session
    db = SessionLocal()

    try:
        # Find the clothing item
        clothing = db.query(Clothes).filter(
            Clothes.clothing_id == clothing_id
        ).first()

        # Return 404 if it does not exist
        if clothing is None:
            raise HTTPException(
                status_code=404,
                detail="Clothing item not found"
            )

        # Delete the clothing item
        db.delete(clothing)

        # Save the change
        db.commit()

        # Return confirmation
        return {
            "message": "Clothing item deleted successfully"
        }

    finally:
        # Close the database session
        db.close()