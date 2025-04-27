from app.logger import logger
from fastapi import HTTPException
from pymongo.errors import PyMongoError
from app.db import mongo_client

logger = logger.get_logger()


class UserService:
    """
    Service class for user-related operations such as creating, fetching balance,
    withdrawing, depositing, and deleting users.
    """

    @classmethod
    async def insert_user(cls, user_data: dict):
        """
        Insert a new user into the database. If the user already exists, raise an HTTPException.

        Args:
            user_data (dict): Data for the user to insert.

        Raises:
            HTTPException: 400 if user already exists, 500 for server error.
        """
        collection = mongo_client.get_users_collection()
        try:
            existing_user = await collection.find_one({"username": user_data["username"]})
            if existing_user:
                logger.info(f"User '{user_data['username']}' already exists.")
                raise HTTPException(status_code=400, detail="User already exists")

            await collection.insert_one(user_data)
            logger.info(f"User '{user_data['username']}' successfully created.")
        except PyMongoError as e:
            logger.error(f"Database error inserting user '{user_data['username']}': {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
        except Exception as e:
            logger.error(f"Unexpected error inserting user '{user_data['username']}': {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

    @classmethod
    async def get_balance(cls, username: str) -> float:
        """
        Get the balance of a user by username.

        Args:
            username (str): Username to fetch balance for.

        Returns:
            float: User's balance.

        Raises:
            HTTPException: 404 if user not found, 500 for server error.
        """
        collection = mongo_client.get_users_collection()
        try:
            user = await collection.find_one({"username": username})
            if not user:
                logger.info(f"User '{username}' not found.")
                raise HTTPException(status_code=404, detail="User not found")

            balance = user.get("balance", 0.0)
            logger.info(f"Fetched balance for user '{username}': {balance}")
            return balance
        except PyMongoError as e:
            logger.error(f"Database error fetching balance for '{username}': {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
        except Exception as e:
            logger.error(f"Unexpected error fetching balance for '{username}': {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

    @classmethod
    async def withdraw(cls, username: str, amount: float) -> float:
        """
        Withdraw an amount from a user's balance.

        Args:
            username (str): Username withdrawing funds.
            amount (float): Amount to withdraw.

        Returns:
            float: New balance after withdrawal.

        Raises:
            HTTPException: 404 if user not found, 400 if insufficient funds, 500 for server error.
        """
        collection = mongo_client.get_users_collection()
        try:
            user = await collection.find_one({"username": username})
            if not user:
                logger.info(f"User '{username}' not found.")
                raise HTTPException(status_code=404, detail="User not found")

            current_balance = user.get("balance", 0.0)
            if current_balance < amount:
                logger.info(f"User '{username}' has insufficient funds for withdrawal of {amount}.")
                raise HTTPException(status_code=400, detail="Insufficient funds")

            new_balance = current_balance - amount
            await collection.update_one({"username": username}, {"$set": {"balance": new_balance}})
            logger.info(f"Withdrew {amount} from user '{username}', new balance: {new_balance}")
            return new_balance
        except PyMongoError as e:
            logger.error(f"Database error withdrawing from '{username}': {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
        except Exception as e:
            logger.error(f"Unexpected error withdrawing from '{username}': {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

    @classmethod
    async def deposit(cls, username: str, amount: float) -> float:
        """
        Deposit an amount into a user's balance.

        Args:
            username (str): Username depositing funds.
            amount (float): Amount to deposit.

        Returns:
            float: New balance after deposit.

        Raises:
            HTTPException: 404 if user not found, 500 for server error.
        """
        collection = mongo_client.get_users_collection()
        try:
            user = await collection.find_one({"username": username})
            if not user:
                logger.info(f"User '{username}' not found.")
                raise HTTPException(status_code=404, detail="User not found")

            new_balance = user.get("balance", 0.0) + amount
            await collection.update_one({"username": username}, {"$set": {"balance": new_balance}})
            logger.info(f"Deposited {amount} into user '{username}' account, new balance: {new_balance}")
            return new_balance
        except PyMongoError as e:
            logger.error(f"Database error depositing into '{username}': {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
        except Exception as e:
            logger.error(f"Unexpected error depositing into '{username}': {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

    @classmethod
    async def delete_user(cls, username: str):
        """
        Delete a user from the database.

        Args:
            username (str): Username to delete.

        Raises:
            HTTPException: 404 if user not found, 500 for server error.
        """
        collection = mongo_client.get_users_collection()
        try:
            result = await collection.delete_one({"username": username})
            if result.deleted_count == 0:
                logger.info(f"Attempted to delete user '{username}', but user does not exist.")
                raise HTTPException(status_code=404, detail="User not found")

            logger.info(f"User '{username}' successfully deleted.")
        except PyMongoError as e:
            logger.error(f"Database error deleting user '{username}': {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
        except Exception as e:
            logger.error(f"Unexpected error deleting user '{username}': {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
