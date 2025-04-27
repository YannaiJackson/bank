from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.models import UserCreate
from app import crud
from secrets import compare_digest

router = APIRouter()
security = HTTPBasic()


# Dummy authentication function
async def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    password = credentials.password
    if not compare_digest(username, password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication")
    return username


@router.post("/bank/accounts/insert")
async def create_user(user: UserCreate):
    await crud.insert_user(user.dict())
    return {"message": "User created successfully"}


@router.get("/bank/accounts/get_balance")
async def read_balance(username: str = Depends(authenticate)):
    balance = await crud.get_balance(username)
    return {"username": username, "balance": balance}


@router.put("/account/withdraw")
async def withdraw_money(amount: float, username: str = Depends(authenticate)):
    new_balance = await crud.withdraw(username, amount)
    return {"message": "Withdraw successful", "new_balance": new_balance}


@router.put("/account/{money}/deposit")
async def deposit_money(money: float, username: str = Depends(authenticate)):
    new_balance = await crud.deposit(username, money)
    return {"message": "Deposit successful", "new_balance": new_balance}


@router.delete("/bank/accounts/delete")
async def delete_account(username: str = Depends(authenticate)):
    await crud.delete_user(username)
    return {"message": "User deleted successfully"}
