from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING
from app.models.product import Product, ProductConstraintsName
from sqlalchemy import (
	Integer, String, ForeignKey, DateTime, UniqueConstraint,
	func,Numeric
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

class ClothSize(str,Enum):
	SMALL = "S"
	MEDIUM = "M"
	LARGE = "L"
	EXTRA_LARGE = "XL"
	EXXTRA_LARGE = "XXL"
	EXTREME_LARGE = "XXXL"

class ClothConstraintsName(str,Enum):
	"""
	Using an Enum for constraint names ensures consistency and avoids hardcoding strings throughout the codebase.
	And Useful for Database Error Resolving, especially when handling unique constraint violations or foreign key errors.
	This do creates a verbose and more boilerplate code, but it is a good practice for maintainability and clarity.
	"""
	FK_CLOTHES_PRODUCT_ID = "fk_clothes_product_id"


class Cloth(Base):
	__tablename__ = "clothes"

	id:Mapped[int] = mapped_column(Integer, primary_key=True)
	product_id:Mapped[int] = mapped_column(Integer, ForeignKey(
		"products.id",name=ClothConstraintsName.FK_CLOTHES_PRODUCT_ID.value, ondelete="CASCADE"), nullable=False)
	
	size:Mapped[str] = mapped_column(String(10), nullable=False, default=ClothSize.MEDIUM.value) 

	created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
	updated_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

	# Relationships
	product:Mapped[Product] = relationship("Product", back_populates="cloth")


