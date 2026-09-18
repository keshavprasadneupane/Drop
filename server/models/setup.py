from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    JSON,
    ForeignKey,
    TIMESTAMP,
    Float,
    Text,
)
from database.settings import Base
from sqlalchemy.sql import func
from pydantic import BaseModel


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    fullName = Column(String(50))
    email = Column(String(50), unique=True)
    username = Column(String(50), unique=True)
    password = Column(String)


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    itemname = Column(String(150))
    description = Column(Text)
    availability = Column(String(100))
    gender = Column(String(100))
    images = Column(JSON)
    price = Column(String(100))
    ratings = Column(Float)
    available_sizes = Column(JSON)
    details_and_care = Column(JSON)
    shipping_and_return = Column(JSON)


class Review(Base):
    __tablename__ = "customerReview"

    id = Column(Integer, primary_key=True, index=True)
    product = Column(Integer, ForeignKey("products.id"), nullable=False)
    customer_name = Column(String(50))
    customer_rating = Column(Integer)
    review_timing = Column(TIMESTAMP, server_default=func.now())
    customer_review = Column(String(1000))


class Payments(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    product = Column(Integer, ForeignKey("products.id"), nullable=True)
    cost = Column(Float)
    quantity = Column(Integer)
    fullname = Column(String(50))
    email_address = Column(String(100))
    shipping_address = Column(String(100))
    city = Column(String(50))
    postal_code = Column(Integer)
    payment_method = Column(String(50))
