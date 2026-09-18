import asyncio
from database.settings import SessionLocal
from models.setup import User, Product as ProductDB, Review as ReviewDB
from schemas.payments import Payment as PaymentSchema
from schemas.products import Product as ProductSchema, Gender
from schemas.review import Review as ReviewSchema
from schemas.auth import UserLogin
from views.products import list_all_products, get_product_by_id
from views.review import list_all_review
from views.payments import create_payment, list_my_payments
from views.users import get_my_profile, login
from starlette.requests import Request
from starlette.datastructures import Headers

async def run_tests():
    db = SessionLocal()
    print("--- 1. Testing list_all_products ---")
    res = await list_all_products(db=db, gender=None, category=None)
    assert res["count"] > 0, "No products found!"
    print(f"Products in DB: {res['count']}")

    print("\n--- 2. Testing list_all_products (gender=female) ---")
    res_female = await list_all_products(db=db, gender="female", category=None)
    print(f"Women products: {res_female['count']}")
    assert res_female["count"] > 0

    print("\n--- 3. Testing get_product_by_id ---")
    first_id = res["data"][0].id
    single_res = await get_product_by_id(product_id=first_id, db=db)
    print(f"Retrieved single product: {single_res['data'].itemname} ({single_res['data'].price})")

    print("\n--- 4. Testing list_all_review ---")
    rev_res = await list_all_review(db=db)
    print(f"Customer reviews in DB: {rev_res['count']}")
    assert rev_res["count"] > 0

    print("\n--- 5. Testing users & auth ---")
    user = db.query(User).first()
    print(f"Testing with user: {user.fullName} (id={user.id})")
    profile_res = await get_my_profile(db=db, current_user=str(user.id))
    print(f"Profile: {profile_res['user']}")
    assert profile_res["user"]["email"] == user.email

    print("\n--- 6. Testing create_payment (Authenticated) ---")
    scope = {
        "type": "http",
        "method": "POST",
        "headers": [(b"origin", b"http://localhost:5173")],
    }
    dummy_req = Request(scope)
    pymnt = PaymentSchema(
        product=first_id,
        product_name="Test Product",
        cost=85.0,
        quantity=1,
        fullname="Nischal Test",
        email_address=user.email,
        shipping_address="123 Fashion Way",
        city="Paris",
        postal_code=75001,
        payment_method="Credit Card"
    )

    payment_res = await create_payment(
        pymnt=pymnt,
        request=dummy_req,
        db=db,
        current_user=user.id
    )
    print(f"Payment result message: {payment_res.get('message')}")
    print(f"Created Payment ID: {payment_res.get('payment_id')}")
    print(f"Checkout URL: {payment_res.get('url')[:50]}...")
    assert payment_res.get("payment_id") is not None

    print("\n--- 7. Testing list_my_payments ---")
    my_payments = await list_my_payments(db=db, current_user=user.id)
    print(f"User payments count: {len(my_payments['data'])}")
    assert len(my_payments['data']) > 0

    db.close()
    print("\nALL BACKEND TESTS PASSED DIRECTLY AGAINST NEON POSTGRES DATABASE!")

if __name__ == "__main__":
    asyncio.run(run_tests())

