# app/user_service.py
import logging
from fastapi import HTTPException
from app.db import mongo_client
from bson.objectid import ObjectId


logger = logging.getLogger(__name__)


class UserService:
    """
    UserService class to handle operations related to users such as
    inserting a new user, fetching balance, withdrawing, depositing, and deleting users.
    """

    @staticmethod
    async def insert_user(user_data: dict):
        """
        Insert a new user into the database. If the user already exists, it raises an HTTPException.

        Args:
            user_data (dict): The data of the user to insert.

        Raises:
            HTTPException: If the user already exists, a 400 error is raised.
        """
        try:
            # Check if user already exists
            existing_user = await mongo_client.get_users_collection().find_one({"username": user_data["username"]})
            if existing_user:
                logger.warning(f"User with username {user_data['username']} already exists.")
                raise HTTPException(status_code=400, detail="User already exists")

            # Insert the new user into the collection
            await mongo_client.get_users_collection().insert_one(user_data)
            logger.info(f"User with username {user_data['username']} successfully created.")
        except Exception as e:
            logger.error(f"Error inserting user {user_data['username']}: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

    @staticmethod
    async def get_balance(username: str):
        """
        Get the balance of a user by username. If the user does not exist, it raises an HTTPException.

        Args:
            username (str): The username of the user whose balance is being fetched.

        Returns:
            float: The balance of the user.

        Raises:
            HTTPException: If the user is not found, a 404 error is raised.
        """
        try:
            user = await mongo_client.get_users_collection().find_one({"username": username})
            if not user:
                logger.warning(f"User with username {username} not found.")
                raise HTTPException(status_code=404, detail="User not found")

            logger.info(f"Fetched balance for user {username}: {user['balance']}")
            return user["balance"]
        except Exception as e:
            logger.error(f"Error fetching balance for user {username}: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

    @staticmethod
    async def withdraw(username: str, amount: float):
        """
        Withdraw an amount from the user's balance. If the user does not have sufficient funds or doesn't exist,
        an HTTPException is raised.

        Args:
            username (str): The username of the user withdrawing funds.
            amount (float): The amount to withdraw.

        Returns:
            float: The new balance after the withdrawal.

        Raises:
            HTTPException: If the user does not exist or has insufficient funds, appropriate error is raised.
        """
        try:
            user = await mongo_client.get_users_collection().find_one({"username": username})
            if not user:
                logger.warning(f"User with username {username} not found.")
                raise HTTPException(status_code=404, detail="User not found")
            if user["balance"] < amount:
                logger.warning(f"User {username} has insufficient funds for withdrawal of {amount}.")
                raise HTTPException(status_code=400, detail="Insufficient funds")

            new_balance = user["balance"] - amount
            await mongo_client.get_users_collection().update_one({"username": username},
                                                                 {"$set": {"balance": new_balance}})
            logger.info(f"Withdrew {amount} from user {username}, new balance: {new_balance}")
            return new_balance
        except Exception as e:
            logger.error(f"Error withdrawing {amount} from user {username}: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

    @staticmethod
    async def deposit(username: str, money: float):
        """
        Deposit an amount into the user's balance. If the user does not exist, an HTTPException is raised.

        Args:
            username (str): The username of the user depositing funds.
            money (float): The amount to deposit.

        Returns:
            float: The new balance after the deposit.

        Raises:
            HTTPException: If the user does not exist, a 404 error is raised.
        """
        try:
            user = await mongo_client.get_users_collection().find_one({"username": username})
            if not user:
                logger.warning(f"User with username {username} not found.")
                raise HTTPException(status_code=404, detail="User not found")

            new_balance = user["balance"] + money
            await mongo_client.get_users_collection().update_one({"username": username},
                                                                 {"$set": {"balance": new_balance}})
            logger.info(f"Deposited {money} into user {username}'s account, new balance: {new_balance}")
            return new_balance
        except Exception as e:
            logger.error(f"Error depositing {money} into user {username}: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

    @staticmethod
    async def delete_user(username: str):
        """
        Delete a user from the database. If the user does not exist, it raises an HTTPException.

        Args:
            username (str): The username of the user to delete.

        Raises:
            HTTPException: If the user does not exist, a 404 error is raised.
        """
        try:
            result = await mongo_client.get_users_collection().delete_one({"username": username})
            if result.deleted_count == 0:
                logger.warning(f"Attempted to delete user {username}, but they do not exist.")
                raise HTTPException(status_code=404, detail="User not found")

            logger.info(f"User {username} successfully deleted.")
        except Exception as e:
            logger.error(f"Error deleting user {username}: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
