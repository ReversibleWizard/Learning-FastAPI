from fastapi import Depends, HTTPException, status, Path, APIRouter
from typing import Annotated

from sqlalchemy import Numeric
from sqlalchemy.orm import Session
from ..models import Todos, User
from ..database import sessionLocal
from pydantic import BaseModel, Field
from .auth import get_current_user
from passlib.context import CryptContext

router = APIRouter(
    prefix="/user",
    tags=["user"]
)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)

class PhoneNumber(BaseModel):
    password: str
    new_phone_number: str

@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(User).filter(User.id == user.get("id")).first()

@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency,
                          user_verification: UserVerification):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_model = db.query(User).filter(User.id == user.get('id')).first()

    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail='Error on password change')
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()

@router.put("/phone_number", status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(user: user_dependency, db: db_dependency, phn_number: PhoneNumber):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_model = db.query(User).filter(User.id == user.get('id')).first()

    if not bcrypt_context.verify(phn_number.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail='Error on password change')
    user_model.phone_number = phn_number.new_phone_number
    db.add(user_model)
    db.commit()