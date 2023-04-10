from pydantic import BaseModel

class user(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str

class contact(BaseModel):
    title: str
    description: str

class userDTO(BaseModel):
    username: str
    password: str

