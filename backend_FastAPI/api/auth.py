from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import User
from db.session import get_session, create_schema_if_not_exists, create_tables_in_schema
from core.security import get_password_hash, verify_password
from core.jwt import create_access_token
from schemas.auth_schemas import UserCreate, UserLogin, Token
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
async def register(user: UserCreate, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(User).where(User.username == user.username))
    db_user = result.scalar_one_or_none()

    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists")



    new_user = User(
        username=user.username,
        hashed_password=get_password_hash(user.password),
        institute_code=user.institute_code,
        role=user.role
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    await create_schema_if_not_exists(user.institute_code)
    await create_tables_in_schema(user.institute_code)

    return {"message": "Registration successful. Please login."}



@router.post("/login", response_model=Token)
async def login(user: UserLogin, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(User).where(User.username == user.username))
    db_user = result.scalar_one_or_none()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({
        "sub": db_user.username,
        "institute_code": db_user.institute_code,
        "role": db_user.role
    }, expires_delta=timedelta(minutes=30))
    return {"access_token": access_token}
