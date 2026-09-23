from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.orm import declarative_base

# Create the base class for SQLAlchemy models
Base = declarative_base()


# SQLAlchemy model for the clothes table
class Clothes(Base):
    __tablename__ = "clothes"

    clothing_id = Column(Integer, primary_key=True)
    name = Column(String)
    size = Column(String)
    quantity = Column(Integer)
    price = Column(Numeric)