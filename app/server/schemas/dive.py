from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field, validator
import regex as re

class DiveSchema(BaseModel):
    max_depth: float = Field(..., example=30.0, description="Maximum depth of the dive. Only numbers allowed.", ge=0, le=350)
    duration: float = Field(..., example=45.0, description="Duration of the dive in minutes. Only numbers allowed.", ge=0)
    date: str = Field(..., example="2021-01-01", description="Date of the dive. Only dates in the format YYYY-MM-DD are allowed")
    location: str = Field(..., example="White Knight", description="Location of the dive site, where the dive took place. Only letters allowed", max_length=150)
    visibility: str  = Field(None, example="10m", description="Average visibility of the water during the dive. Only letters and numbers allowed", max_length=50)
    water_temperature: float = Field(None, example=27.0, description="Average water temperature during the dive in Celcius. Only numbers allowed.", ge=-40, le=40)
    dive_type: str = Field(..., example="Boat or Shore", description="Type of dive. Only letters allowed", max_length=50, min_length=3)
    dive_center: str = Field(..., example="Pyramids Dive Centre", description="Name of the dive center. Only letters allowed", max_length=150, min_length=3)
    dive_buddy: str = Field(..., example="John Doe", description="Name of the dive buddy. Only letters allowed", max_length=150, min_length=3)
    description: str = Field(None, example="This was a very nice dive. You can describe animals you have seen during the dive or skills you learned", description="Description of the dive. Only letters allowed", max_length=800)
    wetsuit_type: str = Field(None, example="Full or Shorty", description="Type of wetsuit used during the dive. Only letters allowed", max_length=70)
    wetsuit_thickness: str = Field(None, example="3mm", description="Thickness of the wetsuit used during the dive. Only letters and numbers allowed", max_length=50)
    weight: float = Field(..., example=5.0, description="Weight used during the dive. Only numbers allowed.", ge=0, le=50)
    air_temperature: float = Field(None, example=27.0, description="Average air temperature during the dive in Celcius. Only numbers allowed.", ge=-50, le=50)
    air_pressure: float = Field(None, example=1013.0, description="Average air pressure during the dive in hPa. Only numbers allowed.", ge=0, le=2000)
    current: str = Field(None, example="Weak or Strong", description="Current during the dive. Only letters allowed", max_length=50)
    dive_number: int = Field(..., example=1, description="Number of the dive. Only numbers allowed.", ge=1, le=20000)
    telegram_id: str = Field(..., example="645595220", description="Telegram ID of the user. Only numbers allowed.\nThis field is unique")

    @validator("*")
    def validate_fields(cls, value, field):
        # Check if the field name is in ones that should contain only letters and validate accordingly
        if field.name in ["location", "dive_type", "dive_center", "dive_buddy", "current"]:
            # Regex pattern that allows only letters, spaces, and hyphens
            if not re.match(r'^[\p{L} -]+$', value, re.UNICODE):
                raise ValueError(f"{field.name} must consist of letters, spaces, or hyphens only")
        return value
    
    class Config:
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "max_depth": 30.0,
                "duration": 45.0,
                "date": "2021-01-01",
                "location": "White Knight",
                "visibility": "10m",
                "water_temperature": 27.0,
                "dive_type": "Boat or Shore",
                "dive_center": "Pyramids Dive Centre",
                "dive_buddy": "John Doe",
                "description": "This was a very nice dive. You can describe animals you have seen during the dive or skills you learned",
                "wetsuit_type": "Full or Shorty",
                "wetsuit_thickness": "3mm",
                "weight": 5.0,
                "air_temperature": 27.0,
                "air_pressure": 1013.0,
                "current": "Weak or Strong",
                "dive_number": 1,
                "telegram_id": "645595220",
            }
        }
    
