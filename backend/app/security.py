from datetime import datetime, timedelta, timezone
import os
import bcrypt
import jwt

SECRET_KEY = os.environ.get("SECRET_KEY", "<replace-with-a-real-secret-key>")

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30

def hash_password(plain_password: str) -> str:
    hashed = bcrypt.hashpw(
        password=plain_password.encode("utf-8"),
        salt=bcrypt.gensalt()
    )
    return hashed.decode("utf-8")

def verify_password(hashed_password: str, plain_password:str) -> bool:
    return bcrypt.checkpw(
        password=plain_password.encode("utf-8"), 
        hashed_password=hashed_password.encode("utf-8")
    )

def create_access_token(data:dict, expire_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expire_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode["exp"] = expire
    return jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        return None
