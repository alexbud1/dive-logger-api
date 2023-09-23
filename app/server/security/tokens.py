import datetime
import hashlib
import os
from datetime import datetime, timedelta
from os.path import dirname, join

import jwt
from dotenv import load_dotenv
from fastapi import Header, HTTPException
from jwt.exceptions import PyJWTError
from server.database.database import database

dotenv_path = join(dirname(__file__), "../..", ".env")
load_dotenv(dotenv_path)

ALGORITHM = os.environ.get("JWT_ALGORITHM")
SECRET_KEY = os.environ.get("JWT_SECRET")


def create_non_expiring_token(user_id: str) -> str:
    # Expiration time to a distant future date (100 years from now)
    expire = datetime.utcnow() + timedelta(
        days=36525
    )  # 365.25 days per year on average

    to_encode = {"sub": user_id, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def verify_token(token: str = Header(None)) -> dict | HTTPException:
    if token is None:
        raise HTTPException(status_code=403, detail="Token is missing")

    await check_is_token_active(token)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except PyJWTError:
        raise HTTPException(status_code=403, detail="Invalid token")


def hash_token(token: str) -> str:
    # Create a SHA-256 hash object
    sha256 = hashlib.sha256()

    # Update the hash object with the token bytes
    sha256.update(token.encode("utf-8"))

    # Get the hexadecimal representation of the hashed token
    hashed_token = sha256.hexdigest()

    return hashed_token


# Check if the token is active in the database
async def check_is_token_active(token: str) -> bool | HTTPException:
    if token is None:
        raise HTTPException(status_code=403, detail="Token is missing")

    hashed_token = hash_token(token)
    token_found = await database.tokens.find_one({"hashed_token": hashed_token})

    if token_found is None:
        raise HTTPException(status_code=403, detail="Token is invalid")
    elif token_found["is_active"] is True and token_found["hashed_token"] == hashed_token:
        return True
    else:
        raise HTTPException(status_code=403, detail="Token is not active")
