from sqlalchemy import Column, Integer, String, JSON, Float
from app.database import Base

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    credit_score = Column(Float, nullable=True)
    explanation = Column(JSON, nullable=True)
