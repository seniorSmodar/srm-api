from pydantic import BaseModel
from datetime import datetime

class clint(BaseModel):
    first_name: str
    middle_name: str
    last_name: str
    source: str
    is_potentincial:bool
    email: str
    phone: str
    address: str

class advice(BaseModel):
    title: str
    description: str

class topic(BaseModel):
    service_id: int
    client_id: int
    title: str
    description: str
    status: str
    created_date: datetime