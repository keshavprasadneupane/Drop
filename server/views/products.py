from typing import Optional
from fastapi import status, APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from schemas.products import Product as ProductSchema
from models.setup import Product as ProductDB
from database.dependencies import db_dependencies
from utils.auth import get_current_user

productsrouter = APIRouter(prefix="/products", tags=["Products"])


# Create a new product (Protected)
@productsrouter.post("/post/", status_code=status.HTTP_201_CREATED)
async def add_new_product(
    prod: ProductSchema,
    db: db_dependencies,
    current_user: str = Depends(get_current_user),
):
    try:
        prod_data = prod.model_dump()
        existing = (
            db.query(ProductDB).filter(ProductDB.itemname == prod.itemname).first()
        )
        if existing:
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content={
                    "message": "Product name with the entered title already exists! Please select a new name."
                },
            )

        new_prod = ProductDB(**prod_data)
        db.add(new_prod)
        db.commit()
        db.refresh(new_prod)
        return {"message": "Product created successfully :)", "data": new_prod}

    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Exception occurred!", "detail": str(e)},
        )


# List all products (with optional gender and category filters)
@productsrouter.get("/list-all-products/", status_code=status.HTTP_200_OK)
async def list_all_products(
    db: db_dependencies,
    gender: Optional[str] = Query(None, description="Filter by gender: male or female"),
    category: Optional[str] = Query(None, description="Filter by category"),
):
    try:
        query = db.query(ProductDB)
        if gender:
            query = query.filter(ProductDB.gender.ilike(f"%{gender}%"))
        if category and category.lower() != "all":
            query = query.filter(ProductDB.itemname.ilike(f"%{category}%"))

        db_products = query.all()
        return {
            "message": "Products retrieved successfully",
            "count": len(db_products),
            "data": db_products,
        }
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Exception occurred!", "detail": str(e)},
        )


# Fetch specific product by ID
@productsrouter.get("/{product_id}/", status_code=status.HTTP_200_OK)
async def get_product_by_id(product_id: int, db: db_dependencies):
    try:
        product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
        if not product:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"message": "Product not found"},
            )
        return {"message": "Product retrieved successfully", "data": product}
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Exception occurred!", "detail": str(e)},
        )
