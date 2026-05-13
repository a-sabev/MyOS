from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone
from app.config import settings
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.auth.models import User
from app.auth.schemas import UserCreate
from app.exceptions import UserAlreadyExistsError, InvalidCredentialsError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    to_encode["exp"] = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

async def create_user(db: AsyncSession, user_data: UserCreate) -> User:
    result = await db.execute(select(User).where(User.email == user_data.email))
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise UserAlreadyExistsError("User with this email is already registerd")
    
    user = User(
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        fullname=user_data.fullname
    )
    
    db.add(user)
    await db.flush()
    await db.refresh(user)
    return user

async def login_user(db: AsyncSession, email: str, password: str) -> dict:
    user =  await get_user_by_email(db, email)
    
    if not user:
        raise InvalidCredentialsError("Invalid credentials")
    
    if not verify_password(password, user.hashed_password):
        raise InvalidCredentialsError("Invalid credentials")
    
    token = create_access_token({"sub": str(user.id)})
    
    return {
        "access_token": token,
        "token_type": "bearer"
    }

async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()

