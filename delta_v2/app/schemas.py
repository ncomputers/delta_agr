from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class APIKeyCreate(BaseModel):
    api_key: str
    api_secret: str

class TradeRuleCreate(BaseModel):
    loss_threshold: float
    quantity: float
    profit_target: float
