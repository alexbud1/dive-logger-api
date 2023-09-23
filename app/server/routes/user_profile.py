from fastapi import APIRouter, Body, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from server.logging.logging import logger
from server.models.user_profile import UserProfile
from server.schemas.user_profile import (
    ErrorResponseModel,
    ResponseModel,
    UserProfileSchema,
)

router = APIRouter()


from fastapi import status

@router.post("/", response_description="User profile data added into the database", status_code=status.HTTP_201_CREATED, response_model=UserProfileSchema)
async def add_user_profile_data(user_profile: UserProfileSchema = Body(...)):
    """
    Saving user profile data into database and returning the saved data.
    """
    user_profile = jsonable_encoder(user_profile)
    new_user_profile = UserProfile(user_profile)
    await new_user_profile.save()
    logger.info(f"NEW USER PROFILE: {new_user_profile.name}")
    # return ResponseModel(new_user_profile, "User profile added successfully.")
    return JSONResponse(content=new_user_profile.to_json(), status_code=status.HTTP_201_CREATED)
