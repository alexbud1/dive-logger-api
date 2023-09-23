import os
from os.path import dirname, join
import certifi
import motor.motor_asyncio
from dotenv import load_dotenv
from server.logging.logging import logger

dotenv_path = join(dirname(__file__), "../..", ".env")
load_dotenv(dotenv_path)


class Database:
    def __init__(self, connection_url: str, db_name: str) -> None:
        self.connection_url = connection_url
        self.db_name = db_name
        self.client = None
        self.database = None

    async def connect(self) -> None:
        # Connect to the database with SSL enabled
        self.client = motor.motor_asyncio.AsyncIOMotorClient(
            self.connection_url, tlsCAFile=certifi.where()
        )
        self.database = self.client[self.db_name]

        # Get a list of collection names from the database
        collection_names = await self.database.list_collection_names()

        # Dynamically create attributes for collection names
        for collection_name in collection_names:
            setattr(self, collection_name, self.database[collection_name])

    # Close the database connection
    async def close_connection(self) -> None:
        if self.client is None:
            logger.warning("No existing database connection to close")
        self.client.close()
        self.client = None
        logger.info("<------------  MongoDB connection closed  ------------>")

    # Check if the database connection is established.
    def is_connected(self) -> bool:
        return self.client is not None


database = Database(os.environ.get("CONNECTION_URI"), os.environ.get("DATABASE_NAME"))