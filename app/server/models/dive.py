from server.database.database import database
from fastapi import HTTPException, status
from pymongo.errors import DuplicateKeyError
from server.logging.logging import logger

class Dive:
    max_depth: float
    duration: float
    date: str
    location: str
    visibility: str = None
    water_temperature: float = None
    dive_type: str
    dive_center: str
    dive_buddy: str
    gas: str = None
    description: str = None
    wetsuit_type: str = None
    wetsuit_thickness: str = None
    weight: float
    air_temperature: float = None
    air_pressure: float = None
    current: str = None
    dive_number: int 
    telegram_id: str

    def __init__(self, data_dict) -> None:
        self.max_depth = data_dict.get("max_depth")
        self.duration = data_dict.get("duration")
        self.date = data_dict.get("date")
        self.location = data_dict.get("location")
        self.visibility = data_dict.get("visibility", None)
        self.water_temperature = data_dict.get("water_temperature", None)
        self.dive_type = data_dict.get("dive_type")
        self.dive_center = data_dict.get("dive_center")
        self.dive_buddy = data_dict.get("dive_buddy")
        self.gas = data_dict.get("gas", None)
        self.description = data_dict.get("description", None)
        self.wetsuit_type = data_dict.get("wetsuit_type", None)
        self.wetsuit_thickness = data_dict.get("wetsuit_thickness", None)
        self.weight = data_dict.get("weight")
        self.air_temperature = data_dict.get("air_temperature", None)
        self.air_pressure = data_dict.get("air_pressure", None)
        self.current = data_dict.get("current", None)
        self.dive_number = data_dict.get("dive_number")
        self.telegram_id = data_dict.get("telegram_id")

    def __repr__(self) -> str:
        return f"<Dive {self.location} {self.date}>"
    
    def to_json(self) -> dict:
        return {
            attr: getattr(self, attr)
            for attr in dir(self)
            if not callable(getattr(self, attr)) and not attr.startswith("__")
        }
    
    async def save(self):
        try:
            await database.dives.insert_one(self.to_json())
            logger.info(f"Dive {self.__repr__} saved successfully")
            return self
        except Exception as e:
            logger.error(f"Error saving dive {self.__repr__} to the database: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    @staticmethod
    async def get_documents_by_field(parameter, value):
        try:
            dives = []
            async for dive in database.dives.find({parameter: value}):
                dives.append(dive)
            return dives
        except Exception as e:
            logger.error(f"Error retrieving dives from the database: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )