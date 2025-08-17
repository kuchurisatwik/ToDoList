from pydantic import BaseModel,EmailStr,ConfigDict,Field
from datetime import datetime
from typing import Annotated ,Optional




class User(BaseModel):
    username : str 
    email: EmailStr
    password: str = Field(...,min_length = 8, max_length = 100)

class ResponseToUser(BaseModel):
    id: int
    username: str
    email:EmailStr
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class UserLogin(User):
    pass


class Task(BaseModel):
    title : str = Field(...,min_length= 1, max_length = 50)
    description: str = Field(...,min_length= 10, max_length = 2000)
    status : str        
    deadline: int
    user_id: int
    

class ResponseToTask(BaseModel):
    id: int
    title : str
    description: str
    status : str       
    deadline: datetime
    created_at: datetime  
    user_id: int          

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    # use user_id to match the payload key
    user_id: Optional[int] = None