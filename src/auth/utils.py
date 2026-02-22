from passlib.context import CryptContext
import hashlib
from datetime import timedelta, datetime
from src.config import Config
from jose import jwt
import uuid
import logging
from jose.exceptions import ExpiredSignatureError, JWTError


ACCESS_TOKEN_EXPIRY = 3600


passwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)

def generate_passwd_hash(password: str) -> str:
    hash = passwd_context.hash(password)

    return hash

def verify_password(password: str, hash: str) -> bool:
    return passwd_context.verify(password, hash)

def create_access_token(user_data: dict, expiry: timedelta = None, refresh: bool = False):
    payload = {}

    payload['user'] = user_data
    payload['exp'] = datetime.now() + (expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY))
    payload['jti'] = str(uuid.uuid4())
    payload['refresh'] = refresh
    token = jwt.encode(
        payload,
        Config.JWT_SECRET,
        algorithm=Config.JWT_ALGORITHM
    )

    return token


def decode_token(token: str) -> dict:
    try:
        token_data = jwt.decode(
                token,
                Config.JWT_SECRET,
                algorithms= Config.JWT_ALGORITHM
            )
        return token_data
    except ExpiredSignatureError as e:
        logging.info("JWT expired: %s", e)
        return None

    except JWTError as e:
        logging.info("Invalid JWT: %s", e)
        return None

    


