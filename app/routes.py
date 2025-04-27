import logging
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.models import UserCreate
from app import crud
from secrets import compare_digest

router = APIRouter()
security = HTTPBasic()
logger = logging.getLogger(__name__)


async def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    """
    Authenticate a user using HTTP basic credentials.

    Args:
        credentials (HTTPBasicCredentials): The credentials sent by the client.

    Returns:
        str: The username if authentication is successful.

    Raises:
        HTTPException: If authentication fails, a 401 Unauthorized error is raised.
    """
    username = credentials.username
    password = credentials.password
    if not compare_digest(username, password):
        logger.warning(f"Failed authentication attempt for username: {username}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication")

    logger.info(f"User {username} authenticated successfully.")
    return username


@router.post("/bank/accounts/insert")
async def create_user(user: UserCreate):
    """
    Create a new user account.

    Args:
        user (UserCreate): The data of the user to create.

    Returns:
        dict: A success message after the user is created.

    Raises:
        HTTPException: If the user already exists, a 400 error is raised.
    """
    try:
        await crud.insert_user(user.dict())
        logger.info(f"User {user.username} created successfully.")
        return {"message": "User created successfully"}
    except Exception as e:
        logger.error(f"Error creating user {user.username}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/bank/accounts/get_balance")
async def read_balance(username: str = Depends(authenticate)):
    """
    Get the balance of the authenticated user.

    Args:
        username (str): The username of the authenticated user.

    Returns:
        dict: The user's balance information.

    Raises:
        HTTPException: If the user does not exist, a 404 error is raised.
    """
    try:
        balance = await crud.get_balance(username)
        logger.info(f"Fetched balance for user {username}: {balance}")
        return {"username": username, "balance": balance}
    except HTTPException as e:
        logger.warning(f"Error fetching balance for user {username}: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error fetching balance for user {username}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.put("/account/withdraw")
async def withdraw_money(amount: float, username: str = Depends(authenticate)):
    """
    Withdraw money from the authenticated user's account.

    Args:
        amount (float): The amount to withdraw.
        username (str): The username of the authenticated user.

    Returns:
        dict: A success message with the new balance.

    Raises:
        HTTPException: If the user does not have sufficient funds, a 400 error is raised.
    """
    try:
        new_balance = await crud.withdraw(username, amount)
        logger.info(f"User {username} withdrew {amount}, new balance: {new_balance}")
        return {"message": "Withdraw successful", "new_balance": new_balance}
    except HTTPException as e:
        logger.warning(f"Error withdrawing {amount} from user {username}: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error withdrawing {amount} from user {username}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.put("/account/{money}/deposit")
async def deposit_money(money: float, username: str = Depends(authenticate)):
    """
    Deposit money into the authenticated user's account.

    Args:
        money (float): The amount to deposit.
        username (str): The username of the authenticated user.

    Returns:
        dict: A success message with the new balance.

    Raises:
        HTTPException: If the user does not exist, a 404 error is raised.
    """
    try:
        new_balance = await crud.deposit(username, money)
        logger.info(f"User {username} deposited {money}, new balance: {new_balance}")
        return {"message": "Deposit successful", "new_balance": new_balance}
    except HTTPException as e:
        logger.warning(f"Error depositing {money} into user {username}'s account: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error depositing {money} into user {username}'s account: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/bank/accounts/delete")
async def delete_account(username: str = Depends(authenticate)):
    """
    Delete the authenticated user's account.

    Args:
        username (str): The username of the authenticated user.

    Returns:
        dict: A success message after the account is deleted.

    Raises:
        HTTPException: If the user does not exist, a 404 error is raised.
    """
    try:
        await crud.delete_user(username)
        logger.info(f"User {username} deleted successfully.")
        return {"message": "User deleted successfully"}
    except HTTPException as e:
        logger.warning(f"Error deleting user {username}: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error deleting user {username}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
