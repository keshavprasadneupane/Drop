from utils.hashPassword import hash_password, comparePassword
from utils.auth import create_access_token, get_current_user
from fastapi import status, APIRouter, Depends
from fastapi.responses import JSONResponse
from database.settings import Base
from models.setup import User
from schemas.auth import UserSignup, UserLogin
from database.dependencies import db_dependencies

usersrouter = APIRouter(prefix="/users", tags=["User Authentication"])


# Create a new user (Signup)
@usersrouter.post("/post/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserSignup, db: db_dependencies):
    try:
        user_data = user.model_dump()
        existing_username = (
            db.query(User).filter(User.username == user.username).first()
        )
        existing_email = db.query(User).filter(User.email == user.email).first()

        if existing_email:
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content={"message": "Email already registered"},
            )

        if existing_username:
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content={"message": "Username already taken"},
            )

        hashed_password = hash_password(user_data["password"])
        db_user = User(
            fullName=user.fullName,
            username=user.username,
            email=user.email,
            password=hashed_password,
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        access_token = create_access_token({"sub": str(db_user.id)})

        user_payload = {
            "id": db_user.id,
            "fullName": db_user.fullName,
            "email": db_user.email,
            "username": db_user.username,
        }

        return {
            "message": "User added successfully :)",
            "data": user_payload,
            "user": user_payload,
            "access_token": access_token,
            "tokens": {"accessToken": access_token},
        }
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Exception occurred!", "detail": str(e)},
        )


# Log in an existing account from the database
@usersrouter.post("/login/", status_code=status.HTTP_200_OK)
async def login(user: UserLogin, db: db_dependencies):
    try:
        db_user = db.query(User).filter(User.email == user.email).first()

        if not db_user:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"message": "Email not found!"},
            )

        entered_password = user.password
        db_password = db_user.password
        match_password = comparePassword(entered_password, db_password)

        if not match_password:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "message": "Your password does not match with the account registered with the entered email. Try again!"
                },
            )

        access_token = create_access_token({"sub": str(db_user.id)})
        user_payload = {
            "id": db_user.id,
            "fullName": db_user.fullName,
            "email": db_user.email,
            "username": db_user.username,
        }
        return {
            "message": "Login Successful :)",
            "access_token": access_token,
            "user": user_payload,
        }

    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Exception occurred!", "detail": str(e)},
        )


# Get profile of currently logged-in user
@usersrouter.get("/me/", status_code=status.HTTP_200_OK)
async def get_my_profile(
    db: db_dependencies, current_user: str = Depends(get_current_user)
):
    try:
        user_id = int(current_user)
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"message": "User profile not found"},
            )
        return {
            "message": "Profile retrieved successfully",
            "user": {
                "id": db_user.id,
                "fullName": db_user.fullName,
                "email": db_user.email,
                "username": db_user.username,
            },
        }
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Failed to retrieve profile", "detail": str(e)},
        )


# List all the users detail (Protected)
@usersrouter.get("/get/", status_code=status.HTTP_200_OK)
async def list_user(db: db_dependencies, current_user: str = Depends(get_current_user)):
    try:
        db_user = db.query(User).all()
        return {
            "message": "Users list successfully listed :)",
            "data": [
                {
                    "id": u.id,
                    "fullName": u.fullName,
                    "email": u.email,
                    "username": u.username,
                }
                for u in db_user
            ],
        }
    except Exception as e:
        db.rollback()
        return {"message": "Exception occurred!", "detail": str(e)}


# Fetch specific user detail
@usersrouter.get("/fetch/{userid}", status_code=status.HTTP_200_OK)
async def fetch_user(userid: int, db: db_dependencies):
    try:
        db_user = db.query(User).filter(User.id == userid).first()
        if db_user is None:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"message": "User not found!"},
            )
        return {
            "message": "User fetched successfully :)",
            "data": {
                "id": db_user.id,
                "fullName": db_user.fullName,
                "email": db_user.email,
                "username": db_user.username,
            },
        }
    except Exception as e:
        db.rollback()
        return {"message": "Exception occurred!", "detail": str(e)}


# Update user data based on user id (Protected)
@usersrouter.put("/update/{userid}", status_code=status.HTTP_200_OK)
async def update_user(
    userid: int,
    user: UserSignup,
    db: db_dependencies,
    current_user: str = Depends(get_current_user),
):
    try:
        if int(current_user) != userid:
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={"message": "You are not authorized to edit this profile"},
            )

        db_user = db.query(User).filter(User.id == userid).first()
        if db_user is None:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"message": "User not found!"},
            )

        db_user.fullName = user.fullName
        db_user.email = user.email
        db_user.username = user.username
        if user.password:
            db_user.password = hash_password(user.password)

        db.commit()
        db.refresh(db_user)
        return {
            "message": "User data updated successfully :)",
            "data": {
                "id": db_user.id,
                "fullName": db_user.fullName,
                "email": db_user.email,
                "username": db_user.username,
            },
        }
    except Exception as e:
        db.rollback()
        return {"message": "Exception occurred!", "detail": str(e)}


# Delete user data (Protected)
@usersrouter.delete("/delete/{userid}", status_code=status.HTTP_200_OK)
async def delete_user(
    userid: int, db: db_dependencies, current_user: str = Depends(get_current_user)
):
    try:
        if int(current_user) != userid:
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={"message": "You are not authorized to delete this profile"},
            )
        db_user = db.query(User).filter(User.id == userid).first()
        if db_user is None:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"message": "User not found!"},
            )
        db.delete(db_user)
        db.commit()
        return {"message": "User successfully deleted :)"}
    except Exception as e:
        db.rollback()
        return {"message": "Exception occurred!", "detail": str(e)}
