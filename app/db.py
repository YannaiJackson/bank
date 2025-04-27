from motor.motor_asyncio import AsyncIOMotorClient
from app.load_config import config


mongo_client = AsyncIOMotorClient(config["mongodb"]["uri"])
db = mongo_client[config["mongodb"]["database"]]
users_collection = db[config["mongodb"]["users_collection"]]
