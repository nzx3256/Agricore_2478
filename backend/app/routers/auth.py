from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import UserRole
from app.models.user import User
from app.dependencies import get_db, require_role
from app.schemas.user_schemas import Token, UserCreate, UserRead
from app.security import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])

#next step is to define our login endpoint, which will accept a username and password
# verify the credetials, and return our JWT access token IF the credentials are valid.
@router.post("/token", response_model=Token)
async def login(
    #we will use the OAuth2PasswordRequestForm dependency to extract the username and password
    #from the request body. Note that this is sent as form data, NOT JSON thanks to  the Depends()
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
) -> Token:
    #our db call to select our user
    result = await db.execute(select(User).where(User.username == form_data.username))
    user = result.scalar_one_or_none()

    #check to verify if the password is correct
    if user is None or not verify_password(user.hashed_password, form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    #set our access token
    access_token = create_access_token(data={"sub": user.username, "role": user.role.value})
    return Token(access_token=access_token, token_type="bearer")

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(
    payload: UserCreate,
    db: AsyncSession = Depends(get_db), 
    _ = Depends(require_role(UserRole.FARM_OPERATORS_ADMIN))
) -> User:
    result = await db.execute(select(User).where(User.username == payload.username))
    user: User | None = result.scalar_one_or_none()
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Username {user.username} is taken"
        )
    user = User(
        username=payload.username, 
        hashed_password=hash_password(payload.password), 
        role=payload.role, is_active=True
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
