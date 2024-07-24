from passlib.context import CryptContext
from fastapi import HTTPException, Request, Cookie
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
active_users = {}

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_current_user(request: Request):
    username = request.cookies.get("username")
    if username in active_users:
        return username
    else:
        raise HTTPException(status_code=401, detail="User not logged in")

async def get_user_by_username(session: AsyncSession, username: str):
    result = await session.execute(select(User).where(User.username == username))
    return result.scalars().first()

async def create_user(session: AsyncSession, username: str, hashed_password: str):
    new_user = User(username=username, hashed_password=hashed_password)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user
