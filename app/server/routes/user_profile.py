from fastapi import APIRouter, Body, Response, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from server.logging.logging import logger
from server.models.user_profile import UserProfile
from server.schemas.user_profile import (
    UserProfileSchema,
    UpdateUserProfileSchema
)
from server.security.tokens import verify_token
from fastapi import status
import json
from server.database.database import database

router = APIRouter()


@router.post(
    "/",
    response_description="User profile data added into the database",
    status_code=status.HTTP_201_CREATED,
    response_model=UserProfileSchema,
)
async def add_user_profile_data(
    user_profile: UserProfileSchema = Body(...),
    token: str = Depends(verify_token),
):
    """
    Saving user profile data into database and returning the saved data.
    """
    user_profile = jsonable_encoder(user_profile)
    new_user_profile = UserProfile(user_profile)
    await new_user_profile.save()
    logger.info(f"NEW USER PROFILE: {new_user_profile.name}")
    return JSONResponse(
        content=new_user_profile.to_json(), status_code=status.HTTP_201_CREATED
    )


@router.get('/{telegram_id}', response_description="User profile data retrieved by telegram_id", response_model=UserProfileSchema, status_code=status.HTTP_200_OK)
async def get_user_profile_data(telegram_id: int, token: str = Depends(verify_token)):
    """
    Retrieving user profile data from database by telegram_id.
    """
    user_profile = await UserProfile.get_document_by_parameter("telegram_id", str(telegram_id))
    if user_profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User profile with telegram_id {telegram_id} not found",
        )
    user_profile["_id"] = str(user_profile["_id"])
    return JSONResponse(
        content=user_profile, status_code=status.HTTP_200_OK
    )

@router.patch('/{telegram_id}', response_description="User profile data updated by telegram_id", response_model=UserProfileSchema, status_code=status.HTTP_200_OK)
async def update_user_profile_data(telegram_id: int, user_profile: UpdateUserProfileSchema = Body(...), token: str = Depends(verify_token)):
    """
    Updating user profile data in database by telegram_id.
    """
    telegram_id = str(telegram_id)
    input_data = {key: value for key, value in user_profile.dict().items() if value is not None}

    # check if any fields should be updated
    if len(input_data) >= 1:
        update_result = await UserProfile.patch(telegram_id, input_data)
        if update_result.modified_count == 1:
            if (
                updated_user_profile := await UserProfile.get_document_by_parameter("telegram_id", telegram_id)
            ) is not None:
                return updated_user_profile

    if (existing_user_profile := await UserProfile.get_document_by_parameter("telegram_id", telegram_id)) is not None:
        return existing_user_profile

    raise HTTPException(status_code=404, detail=f"UserProfile with telegram_id: {telegram_id} not found")