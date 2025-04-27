import pytest
from app import crud


@pytest.mark.asyncio
async def test_insert_and_get_balance():
    username = "test_user"
    user_data = {"username": username, "password": "testpass", "balance": 100.0}

    await crud.insert_user(user_data)
    balance = await crud.get_balance(username)
    assert balance == 100.0


@pytest.mark.asyncio
async def test_withdraw_and_deposit():
    username = "test_user"

    new_balance = await crud.withdraw(username, 50.0)
    assert new_balance == 50.0

    new_balance = await crud.deposit(username, 25.0)
    assert new_balance == 75.0


@pytest.mark.asyncio
async def test_delete_user():
    username = "test_user"
    await crud.delete_user(username)
    with pytest.raises(Exception):
        await crud.get_balance(username)
