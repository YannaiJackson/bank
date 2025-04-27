from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.db import mongo_client
from app.crud import UserService
from secrets import compare_digest
from app.models import UserCreate, UserAuth
from app.logger import logger


router = APIRouter()
logger = logger.get_logger()
security = HTTPBasic()


async def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    """
    Authenticate a user by checking the username and password against the database.

    Args:
        credentials (HTTPBasicCredentials): The credentials sent by the client.

    Returns:
        str: The username if authentication is successful.

    Raises:
        HTTPException: If authentication fails, a 401 Unauthorized error is raised.
    """
    username = credentials.username
    password = credentials.password

    try:
        user = await mongo_client.get_users_collection().find_one({"username": username})
        if user and compare_digest(user["password"], password):
            logger.info(f"User {username} authenticated successfully.")
            return username

        logger.warning(f"Failed authentication attempt for username: {username}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    except Exception as e:
        logger.error(f"Error during authentication: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/bank/accounts/insert")
async def create_user(user: UserCreate):
    """
    Create a new user account.
    """
    try:
        await UserService.insert_user(user.dict())
        logger.info(f"User '{user.username}' created successfully.")
        return {"message": "User created successfully"}
    except HTTPException as e:
        logger.warning(f"Error creating user '{user.username}': {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error creating user '{user.username}': {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/bank/accounts/get_balance")
async def read_balance(username: str = Depends(authenticate)):
    """
    Get the balance of the authenticated user.
    """
    try:
        balance = await UserService.get_balance(username)
        logger.info(f"Fetched balance for user '{username}': {balance}")
        return {"username": username, "balance": balance}
    except HTTPException as e:
        logger.warning(f"Error fetching balance for user '{username}': {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error fetching balance for user '{username}': {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.put("/bank/accounts/withdraw")
async def withdraw_money(amount: float, username: str = Depends(authenticate)):
    """
    Withdraw money from the authenticated user's account.
    """
    try:
        new_balance = await UserService.withdraw(username, amount)
        logger.info(f"User '{username}' withdrew {amount}, new balance: {new_balance}")
        return {"message": "Withdraw successful", "new_balance": new_balance}
    except HTTPException as e:
        logger.warning(f"Error withdrawing {amount} from user '{username}': {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error withdrawing {amount} from user '{username}': {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.put("/bank/accounts/deposit")
async def deposit_money(amount: float, username: str = Depends(authenticate)):
    """
    Deposit money into the authenticated user's account.
    """
    try:
        new_balance = await UserService.deposit(username, amount)
        logger.info(f"User '{username}' deposited {amount}, new balance: {new_balance}")
        return {"message": "Deposit successful", "new_balance": new_balance}
    except HTTPException as e:
        logger.warning(f"Error depositing {amount} into user '{username}''s account: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error depositing {amount} into user '{username}''s account: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/bank/accounts/delete")
async def delete_account(username: str = Depends(authenticate)):
    """
    Delete the authenticated user's account.
    """
    try:
        await UserService.delete_user(username)
        logger.info(f"User '{username}' deleted successfully.")
        return {"message": "User deleted successfully"}
    except HTTPException as e:
        logger.warning(f"Error deleting user '{username}': {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error deleting user '{username}': {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
