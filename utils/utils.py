import jwt
from database.engine import SessionLocal
from sqlalchemy.orm import session
from database.schemas import *
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"], 
    deprecated="auto"
    )

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def employee_from_org(db: session, user_id: int, org_id: int) -> dict:
    user = db.query(User).filter(User.id == user_id).first()
    employee = {}
    for empl in user.employee:
        employee = empl.__dict__
        if employee['org_id'] == org_id:
            break
    return employee

def verifyPassword(plain_password, hashedPassword) -> bool:
    return pwd_context.verify(plain_password, hashedPassword)

def getPasswordHash(password) -> str:
    return pwd_context.hash(password)

def create_token(payload:dict) -> str:
    token = jwt.encode(
        payload= payload,
        key= "SECRET"
    )
    return token

def encode_token(token:str) -> dict:
    pyload = jwt.decode(
        jwt=token,
        key="SECRET",
        algorithms="HS256"
    )
    return pyload