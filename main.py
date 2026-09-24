from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Clothes
from schemas import ClothesCreate, ClothesResponse


# Create the FastAPI application
app = FastAPI()


# Health check endpoint
@app.get("/health")
def health():
    return {"status": "ok"}


# GET all clothes
@app.get("/clothes", response_model=list[ClothesResponse])
def get_clothes(db: Session = Depends(get_db)):
    # Get all clothes from the database
    clothes_list = db.query(Clothes).all()

    # Return the database records
    return clothes_list


# GET one clothing item by ID
@app.get("/clothes/{clothing_id}", response_model=ClothesResponse)
def get_clothing(
    clothing_id: int,
    db: Session = Depends(get_db)
):
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

    return clothing


# POST - Add new clothes
@app.post("/clothes", response_model=ClothesResponse)
def create_clothes(
    clothes_data: ClothesCreate,
    db: Session = Depends(get_db)
):
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

    return new_clothes


# PUT - Update one clothing item
@app.put("/clothes/{clothing_id}", response_model=ClothesResponse)
def update_clothing(
    clothing_id: int,
    clothes_data: ClothesCreate,
    db: Session = Depends(get_db)
):
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

    return clothing


# DELETE - Delete one clothing item
@app.delete("/clothes/{clothing_id}")
def delete_clothing(
    clothing_id: int,
    db: Session = Depends(get_db)
):
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