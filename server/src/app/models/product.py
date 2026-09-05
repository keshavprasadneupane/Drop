from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING
from sqlalchemy import (
	Integer, String, ForeignKey, DateTime, UniqueConstraint,
	func,Numeric
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

if TYPE_CHECKING: # to avoid circular import issues, only import User for type checking
	from app.models.user import User
	from app.models.product_image import ProductImage
	from app.models.clothes import Cloth
	from app.models.review import Review

class ProductConstraintsName(str,Enum):
	"""
	Using an Enum for constraint names ensures consistency and avoids hardcoding strings throughout the codebase.
	And Useful for Database Error Resolving, especially when handling unique constraint violations or foreign key errors.
	This do creates a verbose and more boilerplate code, but it is a good practice for maintainability and clarity.
	"""
	UNIQUE_PRODUCT_NAME = "uq_products_name"
	FK_PRODUCTS_USER_ID = "fk_products_user_id"


class Product(Base):
	__tablename__ = "products"
	__table_args__ = (
		UniqueConstraint("name", name=ProductConstraintsName.UNIQUE_PRODUCT_NAME.value),
	)

	id:Mapped[int] = mapped_column(Integer, primary_key=True)
	user_id:Mapped[int] = mapped_column(Integer, ForeignKey(
		"users.id",name=ProductConstraintsName.FK_PRODUCTS_USER_ID.value, ondelete="CASCADE"), nullable=False)
	
	name:Mapped[str] = mapped_column(String(255), nullable=False,)
	description:Mapped[str] = mapped_column(String(255), nullable=True,)
	price:Mapped[float] = mapped_column(Numeric(10, 2), nullable=False) # always NPR convert to other on frontend.
	
	created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
	updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now())

	# Relationships
	user: Mapped["User"] = relationship("User", back_populates="products")
	product_images: Mapped[list["ProductImage"]] = relationship(
		"ProductImage", back_populates="product", cascade="all, delete-orphan",passive_deletes=True
	)
	# for now assuming one product can have only one cloth, but in future it can be one to many relationship.
	cloth: Mapped["Cloth"] = relationship("Cloth", back_populates="product", cascade="all, delete-orphan",passive_deletes=True)
	reviews: Mapped[list["Review"]] = relationship("Review", back_populates="product", cascade="all, delete-orphan",passive_deletes=True)