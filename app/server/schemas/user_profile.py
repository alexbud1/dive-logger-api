from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserProfileSchema(BaseModel):
    name: str
    is_diver: bool
    amount_of_dives: int = None
    country: str = None
    profile_photo: str = None

    class Config:
        schema_extra = {
            "example": {
                "name": "John Doe",
                "is_diver": True,
                "amount_of_dives": 100,
                "country": "Nigeria",
                "profile_photo": "link_to_profile_photo",
            }
        }


class UpdateStudentModel(BaseModel):
    fullname: Optional[str]
    email: Optional[EmailStr]
    course_of_study: Optional[str]
    year: Optional[int]
    gpa: Optional[float]

    class Config:
        schema_extra = {
            "example": {
                "fullname": "John Doe",
                "email": "jdoe@x.edu.ng",
                "course_of_study": "Water resources and environmental engineering",
                "year": 4,
                "gpa": "4.0",
            }
        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
