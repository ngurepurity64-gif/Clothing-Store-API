from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Numeric
from sqlalchemy.orm import declarative_base, sessionmaker

# Create the FastAPI application
app = FastAPI()

# PostgreSQL database connection
# Replace YOUR_PASSWORD with your existing PostgreSQL password
DATABASE_URL = "postgresql+psycopg://postgres:4455ttyy@localhost:5432/clothingstore"

# Create the database engine
engine = create_engine(DATABASE_URL)

# Create the base class for SQLAlchemy models
Base = declarative_base()

# Create a database session
SessionLocal = sessionmaker(bind=engine)


# Pydantic request model
# FastAPI validates the incoming data before the endpoint runs
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


# Get all clothes
@app.get("/clothes")
def get_clothes():
    # Open a database session
    db = SessionLocal()

    try:
        # Get all records from the clothes table
        clothes_list = db.query(Clothes).all()

        # Return the records
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


# Add new clothes
@app.post("/clothes")
def create_clothes(clothes_data: ClothesCreate):
    # Open a database session
    db = SessionLocal()

    try:
        # Create a new clothes record
        new_clothes = Clothes(
            name=clothes_data.name,
            size=clothes_data.size,
            quantity=clothes_data.quantity,
            price=clothes_data.price
        )

        # Add the record to the session
        db.add(new_clothes)

        # Save the record to PostgreSQL
        db.commit()

        # Get the generated clothing ID
        db.refresh(new_clothes)

        # Return the newly created record
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