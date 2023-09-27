from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field, validator
import regex as re

class UserProfileSchema(BaseModel):
    name: str = Field(..., example="John Doe", description="Name of the user(it would be seen by other divers). Only letters allowed", max_length=100, min_length=3)
    is_diver: bool = Field(..., example=True, description="Boolean value that indicates if the user is a diver or not")
    amount_of_dives: int = Field(None, example=100, description="Amount of dives the user has done. Only numbers allowed.", ge=0, le=20000)
    country: str = Field(None, example="Nigeria", description="Country of the user. Only letters allowed. Country is not validated.", max_length=100, min_length=3)
    profile_photo: str = Field(None, example="link_to_profile_photo", description="Link to the user's profile photo. This field is not validated", max_length=250, min_length=10)
    telegram_id: str = Field(None, example="645595220", description="Telegram ID of the user. Only numbers allowed.\nThis field is unique", max_length=20, min_length=5)

    @validator("*")
    def validate_fields(cls, value, field):
        # Check if the field name is "name" or "country" and validate accordingly
        if field.name in ["name", "country"]:
            # Regex pattern that allows only letters, spaces, and hyphens
            if not re.match(r'^[\p{L} -]+$', value, re.UNICODE):
                raise ValueError(f"{field.name} must consist of letters, spaces, or hyphens only")
        return value

    class Config:
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "John Doe",
                "is_diver": True,
                "amount_of_dives": 100,
                "country": "Nigeria",
                "profile_photo": "link_to_profile_photo",
                "telegram_id": "645595220"
            }
        }


class UpdateUserProfileSchema(BaseModel):
    name: str = Field(None, example="John Doe", description="Name of the user(it would be seen by other divers). Only letters allowed", max_length=100, min_length=3)
    is_diver: bool = Field(None, example=True, description="Boolean value that indicates if the user is a diver or not")
    amount_of_dives: int = Field(None, example=100, description="Amount of dives the user has done. Only numbers allowed.", ge=0, le=20000)
    country: str = Field(None, example="Nigeria", description="Country of the user. Only letters allowed. Country is not validated.", max_length=100, min_length=3)
    profile_photo: str = Field(None, example="link_to_profile_photo", description="Link to the user's profile photo. This field is not validated", max_length=250, min_length=10)
    telegram_id: str = Field(None, example="645595220", description="Telegram ID of the user. Only numbers allowed.\nThis field is unique", max_length=20, min_length=5)

    @validator("*")
    def validate_fields(cls, value, field):
        # Check if the field name is "name" or "country" and validate accordingly
        if field.name in ["name", "country"]:
            # Regex pattern that allows only letters, spaces, and hyphens
            if not re.match(r'^[\p{L} -]+$', value, re.UNICODE):
                raise ValueError(f"{field.name} must consist of letters, spaces, or hyphens only")
        return value

    class Config:
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "John Doe",
                "is_diver": True,
                "amount_of_dives": 100,
                "country": "Nigeria",
                "profile_photo": "link_to_profile_photo",
                "telegram_id": "645595220"
            }
        }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}