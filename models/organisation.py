from pydantic import BaseModel

class organisation(BaseModel):
    name: str
    description: str

class role(BaseModel):
    title: str
    delete: bool
    write: bool

class employee(BaseModel):
    title: str
    write: bool
    chek: bool
    delete: bool

class service(BaseModel):
    title: str
    description: str


