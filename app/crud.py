from app.db import users_collection
from fastapi import HTTPException
from bson.objectid import ObjectId


async def insert_user(user_data: dict):
    existing_user = await users_collection.find_one({"username": user_data["username"]})
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    await users_collection.insert_one(user_data)


async def get_balance(username: str):
    user = await users_collection.find_one({"username": username})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user["balance"]


async def withdraw(username: str, amount: float):
    user = await users_collection.find_one({"username": username})
    if not user or user["balance"] < amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")
    new_balance = user["balance"] - amount
    await users_collection.update_one({"username": username}, {"$set": {"balance": new_balance}})
    return new_balance


async def deposit(username: str, money: float):
    user = await users_collection.find_one({"username": username})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    new_balance = user["balance"] + money
    await users_collection.update_one({"username": username}, {"$set": {"balance": new_balance}})
    return new_balance


async def delete_user(username: str):
    result = await users_collection.delete_one({"username": username})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
