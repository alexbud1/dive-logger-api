from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from server.logging.logging import logger
from server.models.user_profile import UserProfile
from server.schemas.user_profile import (
    ErrorResponseModel,
    ResponseModel,
    UserProfileSchema,
)

router = APIRouter()


@router.post("/", response_description="User profile data added into the database")
async def add_user_profile_data(user_profile: UserProfileSchema = Body(...)):
    user_profile = jsonable_encoder(user_profile)
    new_user_profile = UserProfile(user_profile)
    await new_user_profile.save()
    logger.info(f"NEW USER PROFILE: {new_user_profile.name}")
    return ResponseModel(new_user_profile, "User profile added successfully.")
