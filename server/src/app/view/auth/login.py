from fastapi import APIRouter
from app.core.security import FormData ,AuthHelper
from app.core.exception import APIException
from app.controller.auth.auth_controller import AuthController
from app.core.database import DB
from app.schema.auth import LoginResponse
from fastapi import status


router = APIRouter()# the parent has defined prefix and tags, so no need to define here


@router.post(
    "/login",
    summary="Login and get access token",
    status_code=status.HTTP_200_OK,
    response_model=LoginResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Invalid credentials"
        },
		status.HTTP_500_INTERNAL_SERVER_ERROR: {
			"description": "Internal server error"
		}
    }
)
async def login(form_data:FormData, db: DB):
	"""
	Endpoint for user login.

	Returns access and refresh tokens upon successful authentication.

	Curl example:

	curl -X POST "http://localhost:8000/auth/login" \
	-H "accept: application/json" \
	-H "Content-Type: application/x-www-form-urlencoded" \
	-d "username=test@example.com&password=secret"

	"""
	email = form_data.validated_email
	password = form_data.password

	user = await AuthController.login(email, password, db)
	access_token = AuthHelper.create_access_token(user.id)
	refresh_token = AuthHelper.create_refresh_token(user.id)

	return LoginResponse(
		user_id=user.id,
		role=user.role,
		access_token=access_token, 
		refresh_token=refresh_token,
		token_type="bearer"
		)