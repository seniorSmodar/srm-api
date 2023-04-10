from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import session
from database.schemas import *
from models import user
from utils import utils

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

router = APIRouter()

@router.post("/login")
def token(request: user.userDTO, db: session = Depends(utils.get_db)):
    user = db.query(User).filter(User.username == request.username).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="user not found"
        )
    if not utils.verifyPassword(request.password, user.password_hash):
        raise HTTPException(
            status_code=406,
            detail="invalid password"
        )
    payload = {
        "id":f"{user.id}"
    }
    accses_token = utils.create_token(payload)
    return accses_token

@router.post("/register")
def create_user(request: user.user, db: session = Depends(utils.get_db)):
    new_user = User(
        username = request.username,
        password_hash = utils.getPasswordHash(request.password),
        first_name = request.first_name,
        last_name = request.last_name
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

