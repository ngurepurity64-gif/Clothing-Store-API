from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String, Numeric
from sqlalchemy.orm import declarative_base, sessionmaker

# Create the FastAPI application
app = FastAPI()

# PostgreSQL database connection
DATABASE_URL = "postgresql+psycopg://postgres:4455ttyy@localhost:5432/clothingstore"

# Create the database engine
engine = create_engine(DATABASE_URL)

# Create the base class for SQLAlchemy models
Base = declarative_base()

# Create a database session
SessionLocal = sessionmaker(bind=engine)


# Define the clothes table
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


# Get all clothes from the database
@app.get("/clothes")
def get_clothes():
    # Open a database session
    db = SessionLocal()

    try:
        # Get all records from the clothes table
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