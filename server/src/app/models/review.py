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
	from app.models.product import Product

class ReviewConstraintsName(str,Enum):
	"""
	Using an Enum for constraint names ensures consistency and avoids hardcoding strings throughout the codebase.
	And Useful for Database Error Resolving, especially when handling unique constraint violations or foreign key errors.
	This do creates a verbose and more boilerplate code, but it is a good practice for maintainability and clarity.
	"""
	UNIQUE_REVIEW_USER_PRODUCT = "uq_reviews_user_product"


class Review(Base):
	__tablename__ = "reviews"
	__table_args__ = (
		UniqueConstraint("user_id", "product_id", name=ReviewConstraintsName.UNIQUE_REVIEW_USER_PRODUCT.value),
	)

	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
	product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
	rating: Mapped[float] = mapped_column(Numeric(2, 1), nullable=False)  # Rating out of 5.0
	comment: Mapped[str] = mapped_column(String(500), nullable=True)

	created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
	updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

	# Relationships
	user: Mapped["User"] = relationship("User", back_populates="reviews")
	product: Mapped["Product"] = relationship("Product", back_populates="reviews")