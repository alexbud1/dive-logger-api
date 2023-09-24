from server.database.database import database
from fastapi import HTTPException, status
from pymongo.errors import DuplicateKeyError
from server.logging.logging import logger

class UserProfile:
    name: str
    is_diver: bool
    amount_of_dives: int = None
    country: str = None
    profile_photo: str = None
    telegram_id: int = None

    def __init__(self, data_dict) -> None:
        self.name = data_dict.get("name")
        self.is_diver = data_dict.get("is_diver")
        self.amount_of_dives = data_dict.get("amount_of_dives", None)
        self.country = data_dict.get("country", None)
        self.profile_photo = data_dict.get("profile_photo", None)
        self.telegram_id = data_dict.get("telegram_id", None)

    def __repr__(self) -> str:
        return f"<UserProfile {self.name}>"

    def to_json(self) -> dict:
        return {
            attr: getattr(self, attr)
            for attr in dir(self)
            if not callable(getattr(self, attr)) and not attr.startswith("__")
        }

    async def save(self):
        try:
            await database.user_profiles.insert_one(self.to_json())
            logger.info(f"User {self.name} saved successfully")
            return self
        except DuplicateKeyError:
            logger.error(f"User {self.name} already exists in the database")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="User already exists."
            )
        except Exception as e:
            logger.error(f"Error saving user {self.name} to the database: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )
    
    @staticmethod
    async def get_document_by_parameter(parameter, value):
        try:
            document = await database.user_profiles.find_one({parameter: value})
            if document is None:
                logger.error(f"User with {parameter} {value} not found in the database")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"User with {parameter} {value} not found",
                )
            else:
                logger.info(f"User {document['name']} retrieved successfully")
                return document
            
        except HTTPException as e:
            raise e    
        
        except Exception as e:
            logger.error(f"Error retrieving user by {parameter}, value: {value} from the database: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )
