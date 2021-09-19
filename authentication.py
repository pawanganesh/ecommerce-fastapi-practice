import jwt
from fastapi import status
from fastapi.exceptions import HTTPException
from passlib.context import CryptContext
from dotenv import dotenv_values
from models import User


config_credentials = dotenv_values(".env")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


async def verify_token(token: str):
    try:
        payload = jwt.decode(token, config_credentials["SECRET_KEY"], algorithms=['HS256'])
        user = await User.get(id = payload.get("id"))
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"}
            )
    return user
