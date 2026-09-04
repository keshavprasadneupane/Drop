from fastapi import APIRouter
from app.controller.auth.auth_controller import AuthController
from app.view.deps import CustomerUser
from app.core.exception import APIException,ErrorMessage
from app.core.database import DB
from app.schema.auth import MeResponse
from fastapi import status

from app.view.deps import CustomerUser


router = APIRouter()# the parent has defined prefix and tags, so no need to define here

@router.get(
	"/me",
	summary="Get current user information",
	status_code=status.HTTP_200_OK,
	response_model=MeResponse
)
def get_user_basic_info(user: CustomerUser, db: DB):
	"""
	Returns basic information about the currently authenticated user.

	This endpoint is intended for frontend initialization, such as:
	- Determining the user's role
	- Customizing the UI and navigation
	- Controlling access to role-specific features

	Returns:
		MeResponse: Basic information about the authenticated user.
	"""
	try:

		if not user:
			# No additional debug information is needed here.
			# Authentication is handled by the dependency layer.
			# this will never run since the dependency will raise an exception if the user is not authenticated.
			# but just in case, we will raise an Unauthorized exception with a generic message.
			raise APIException.Unauthorized(ErrorMessage.INVALID_CREDENTIALS)

		# No controller is used because this endpoint contains no
		# business logic and simply returns data already provided
		# by the authentication dependency.
		return MeResponse(
			user_id=user.id,
			username=user.username,
			role=user.role
		)

	except APIException.Base as e:
		raise e
	
	except Exception as e:
		raise APIException.InternalServerError(
			message="An error occurred while fetching user information.",
			debug_detail=str(e)
		)
	


@router.delete(
	"/{user_id}",
	summary="Delete a user by ID",
	status_code=status.HTTP_204_NO_CONTENT,
	responses={
		status.HTTP_404_NOT_FOUND: {
			"description": "Not Found - User with the specified ID does not exist"
		},
		status.HTTP_500_INTERNAL_SERVER_ERROR: {
			"description": "Internal Server Error - An unexpected error occurred during the deletion process"
		}	
	}
)
async def delete_user(user_id: int, db: DB):
	await AuthController.delete_user_by_id(user_id=user_id, db=db)
	return None
	