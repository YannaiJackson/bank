from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str
    balance: float


class UserAuth(BaseModel):
    username: str
    password: str
