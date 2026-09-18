from schemas.review import Review as ReviewSchema
from models.setup import Review as ReviewDB, User as UserDB
from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from database.dependencies import db_dependencies
from utils.auth import get_current_user

reviewrouter = APIRouter(prefix="/review", tags=["Review"])


# Create a new customer review (Protected)
@reviewrouter.post("/post/", status_code=status.HTTP_201_CREATED)
async def create_review(
    review: ReviewSchema,
    db: db_dependencies,
    current_user: str = Depends(get_current_user),
):
    try:
        user_id = int(current_user)
        user = db.query(UserDB).filter(UserDB.id == user_id).first()
        customer_name = review.customer_name or (
            user.fullName if user else "Verified Buyer"
        )

        rvw = review.model_dump()
        rvw["customer_name"] = customer_name

        customer_data = ReviewDB(**rvw)
        db.add(customer_data)
        db.commit()
        db.refresh(customer_data)
        return {"message": "New customer review created!", "data": customer_data}
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Exception occurred!", "detail": str(e)},
        )


# List all customer reviews
@reviewrouter.get("/list-all-review/", status_code=status.HTTP_200_OK)
async def list_all_review(db: db_dependencies):
    try:
        db_review = db.query(ReviewDB).all()
        return {
            "message": "Customer reviews listed successfully :)",
            "count": len(db_review),
            "data": db_review,
        }
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Exception occurred!", "detail": str(e)},
        )


# List customer reviews for a specific product
@reviewrouter.get("/product/{product_id}/", status_code=status.HTTP_200_OK)
async def list_product_reviews(product_id: int, db: db_dependencies):
    try:
        reviews = db.query(ReviewDB).filter(ReviewDB.product == product_id).all()
        return {
            "message": "Product reviews listed successfully",
            "product_id": product_id,
            "count": len(reviews),
            "data": reviews,
        }
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Exception occurred!", "detail": str(e)},
        )
