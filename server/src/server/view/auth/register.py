from fastapi import APIRouter,status

from server.controller.auth.auth_controller import AuthController
from server.core.database import DB
from server.models.user import User
from server.schema.auth import RegisterRequest, RegisterResponse


router = APIRouter()# the parent has defined prefix and tags, so no need to define here


@router.post(
	"/register",
	summary="Register a new user",
	status_code=status.HTTP_201_CREATED,
	response_model=RegisterResponse,
	responses={
		status.HTTP_409_CONFLICT: {
			"description": "Conflict - UserName Or Email already exists"
		},
		status.HTTP_500_INTERNAL_SERVER_ERROR: {
			"description": "Internal Server Error - An unexpected error occurred during the registration process"
		}
	}
)
async def register(data: RegisterRequest,db: DB):
	user :User = await AuthController.register(data=data, db=db)
	return RegisterResponse(
		user_id=user.id,
		message="User registered successfully"
	)

