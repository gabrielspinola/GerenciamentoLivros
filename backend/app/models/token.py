from pydantic import BaseModel

class UserRegister(BaseModel):
    login: str
    password: str

class UserLogin(BaseModel):
    login: str
    password: str

class UserInDB(BaseModel):
    login: str
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
 