import logging
from motor.motor_asyncio import AsyncIOMotorClient
from app.load_config import config


logger = logging.getLogger(__name__)


class MongoDBClient:
    """
    A class to manage the connection to MongoDB using Motor (AsyncIO MongoDB client).
    This class initializes the connection to MongoDB and provides access to collections.
    """

    def __init__(self):
        """
        Initialize the MongoDBClient instance.
        - Connect to the MongoDB database using Motor AsyncIOMotorClient.
        - Retrieve the database and collections using configuration settings.
        """
        try:
            # MongoDB connection setup using Motor AsyncIOMotorClient
            self.client = AsyncIOMotorClient(config["mongodb"]["uri"])
            self.db = self.client[config["mongodb"]["database"]]
            self.users_collection = self.db[config["mongodb"]["users_collection"]]

            # Log successful connection
            logger.info(f"Successfully connected to MongoDB database: {config['mongodb']['database']}")
        except Exception as e:
            logger.error(f"Error connecting to MongoDB: {e}")
            raise

    def get_users_collection(self):
        """
        Returns the MongoDB users collection.
        This method can be used to interact with the users collection.

        Returns:
            collection: The users collection from MongoDB.
        """
        return self.users_collection


# Create an instance of the MongoDBClient
mongo_client = MongoDBClient()

