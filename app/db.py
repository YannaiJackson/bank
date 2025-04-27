from app.logger import logger
from motor.motor_asyncio import AsyncIOMotorClient
from app.load_config import config


logger = logger.get_logger()


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
            logger.info("Attempting to load configuration for mongoDB...")
            # Ensure config is properly loaded
            self.config = config

            # Get the MongoDB URI and database from the config
            mongodb_config = self.config.get("mongodb")
            mongo_uri = mongodb_config.get("uri")
            database_name = mongodb_config.get("database")
            users_collection_name = mongodb_config.get("users_collection")

            if not mongo_uri or not database_name or not users_collection_name:
                raise ValueError("MongoDB configuration missing required fields: uri, database, or users_collection")
            logger.info("MongoDB configuration loaded successfully.")

            logger.info("Connection to Database...")
            # MongoDB connection setup using Motor AsyncIOMotorClient
            self.mongo_client = AsyncIOMotorClient(mongo_uri)
            self.db = self.mongo_client[database_name]
            self.users_collection = self.db[users_collection_name]
            logger.info(f"Successfully connected to MongoDB database: {database_name}")

        except Exception as e:
            # Log error if MongoDB connection fails
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
