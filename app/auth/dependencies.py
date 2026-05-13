from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError

from app.config import settings
from app.database import get_db
from app.auth.models import User
from app.auth.service import get_user_by_email
from app.exceptions import InvalidCredentialsError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise InvalidCredentialsError("Invalid token")
    except JWTError:
        raise InvalidCredentialsError("Invalid token")

    result = await db.execute(
        __import__('sqlalchemy').select(User).where(User.id == int(user_id))
    )
    user = result.scalar_one_or_none()

    if user is None:
        raise InvalidCredentialsError("User not found")

    return user