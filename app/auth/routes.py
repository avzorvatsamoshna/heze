#from fastapi import APIRouter, Depends, Form, HTTPException, Request, Cookie
#from fastapi.templating import Jinja2Templates
#from starlette.responses import RedirectResponse, HTMLResponse, JSONResponse
#from sqlalchemy.ext.asyncio import AsyncSession
#from sqlalchemy.future import select
#from pydantic import BaseModel
#from passlib.context import CryptContext
#import folium
#import random
#from auth.database import get_async_session, User
#HARDCODED_USER = {
#    "username": "admin",
#    "password": "admin",
#}
#
#pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#active_users = {}
#
#templates = Jinja2Templates(directory="templates")
#auth_routes = APIRouter()
#user_routes = APIRouter()
#map_routes = APIRouter()
#
#
#
#class UserCreate(BaseModel):
#    username: str
#    password: str
#    is_user: bool
#    is_developer: bool
#    is_admin: bool
#
#def verify_password(plain_password, hashed_password):
#    return pwd_context.verify(plain_password, hashed_password)
#
#
#def get_password_hash(password):
#    return pwd_context.hash(password)
#
#
#def get_current_user(request: Request):
#    username = request.cookies.get("username")
#    if username in active_users:
#        return username
#    else:
#        raise HTTPException(status_code=401, detail="User not logged in")
#
#
#async def get_user_by_username(session: AsyncSession, username: str):
#    result = await session.execute(select(User).where(User.username == username))
#    return result.scalars().first()
#@user_routes.get("/register", response_class=HTMLResponse)
#async def main_page(request: Request):
#    return templates.TemplateResponse("login_v_2.html", {"request": request})
#
#async def create_user(session: AsyncSession, username: str, hashed_password: str, is_user: bool, is_admin: bool , is_developer: bool,
#                      ):
#    new_user = User(username=username, hashed_password=hashed_password, is_user=is_user, is_admin=is_admin, is_developer=is_developer)
#    session.add(new_user)
#    await session.commit()
#    await session.refresh(new_user)
#    return new_user
#
#@auth_routes.get("/login", response_class=HTMLResponse)
#async def login_form(request: Request):
#    username = request.cookies.get("username")
#    if username in active_users:
#        return RedirectResponse(url="/main_page")
#    return templates.TemplateResponse("login.html", {"request": request})
#
#
#
#@auth_routes.post("/register", response_class=JSONResponse)
#async def register(
#    username: str = Form(...),
#    password: str = Form(...),
#    is_user: bool = Form(False),
#    is_developer: bool = Form(False),
#    is_admin: bool = Form(False),
#    session: AsyncSession = Depends(get_async_session)
#):
#    db_user = await get_user_by_username(session, username)
#    if db_user:
#        raise HTTPException(status_code=400, detail="Username already exists")
#
#    hashed_password = get_password_hash(password)
#    await create_user(session, username, hashed_password, is_user, is_developer, is_admin)
#
#    return {"message": "User registered successfully"}
#
#
#@auth_routes.post("/login")
#async def login(username: str = Form(...),password: str = Form(...),session: AsyncSession = Depends(get_async_session),):
#    user = await get_user_by_username(session, username)
#    if user and verify_password(password, user.hashed_password):
#        if user.username in active_users:
#            raise HTTPException(status_code=400, detail="You are already logged in")
#        response = RedirectResponse(url="/success_login", status_code=302)
#        response.set_cookie(key="username", value=user.username)
#        active_users[user.username] = True
#        return response
#    else:
#        raise HTTPException(status_code=400, detail="Invalid username or password")
#
#
#@auth_routes.get("/user_name")
#async def get_user_name(username: str = Cookie(None)):
#    if username:
#        return {"username": username}
#    else:
#        raise HTTPException(status_code=401, detail="User not logged in")
#
#
#@auth_routes.get("/logout")
#async def logout(response: JSONResponse, username: str = Cookie(None)):
#    if username in active_users:
#        del active_users[username]
#        response.delete_cookie("username")
#        return RedirectResponse(url="/login")
#    else:
#        return RedirectResponse(url="/login")
#
#
#@auth_routes.get("/success_login", response_class=HTMLResponse)
#def redirect():
#    return RedirectResponse('/main_page')
#
#
#@user_routes.get("/main_page", response_class=HTMLResponse)
#async def main_page(request: Request, username: str = Depends(get_current_user)):
#    return templates.TemplateResponse("main_page.html", {"request": request, "username": username})
#
#
#def generate_random_coordinates():
#    return [random.uniform(-90, 90), random.uniform(-180, 180)]
#
#
#@map_routes.get("/map", response_class=HTMLResponse)
#async def map():
#    m = folium.Map(location=[0, 0], zoom_start=1)
#    map_html = m.get_root().render()
#    return map_html
#
#
#@map_routes.get("/update_marker")
#async def update_marker():
#    new_coordinates = generate_random_coordinates()
#    return {"lat": new_coordinates[0], "lng": new_coordinates[1]}
#
from fastapi import APIRouter, Depends, Form, HTTPException, Request, Cookie
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.context import CryptContext
import folium
import random
from auth.database import get_async_session, User
from starlette.templating import Jinja2Templates

# Жестко закодированный пользователь
HARDCODED_USER = {
    "username": "admin",
    "password": "admin"
}

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
active_users = {}

templates = Jinja2Templates(directory="templates")
auth_routes = APIRouter()
user_routes = APIRouter()
map_routes = APIRouter()

class UserCreate(BaseModel):
    username: str
    password: str
    is_user: bool
    is_developer: bool
    is_admin: bool

# Функция для проверки пароля
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Функция для хеширования пароля
def get_password_hash(password):
    return pwd_context.hash(password)

# Функция для получения текущего пользователя из cookie
def get_current_user(request: Request):
    username = request.cookies.get("username")
    if username in active_users:
        return username
    else:
        raise HTTPException(status_code=401, detail="User not logged in")

# Функция для получения пользователя по имени из базы данных
async def get_user_by_username(session: AsyncSession, username: str):
    result = await session.execute(select(User).where(User.username == username))
    return result.scalars().first()

# Регистрируем новый пользователь
async def create_user(session: AsyncSession, username: str, hashed_password: str, is_user: bool, is_admin: bool, is_developer: bool):
    new_user = User(username=username, hashed_password=hashed_password, is_user=is_user, is_admin=is_admin, is_developer=is_developer)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user

@user_routes.get("/register", response_class=HTMLResponse)
async def main_page(request: Request):
    return templates.TemplateResponse("login_v_2.html", {"request": request})

# Отображение формы входа
@auth_routes.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    username = request.cookies.get("username")
    if username in active_users:
        return RedirectResponse(url="/main_page")
    return templates.TemplateResponse("login.html", {"request": request})

# Регистрация нового пользователя
@auth_routes.post("/register", response_class=JSONResponse)
async def register(
    username: str = Form(...),
    password: str = Form(...),
    is_user: bool = Form(False),
    is_developer: bool = Form(False),
    is_admin: bool = Form(False),
    session: AsyncSession = Depends(get_async_session)
):
    db_user = await get_user_by_username(session, username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = get_password_hash(password)
    await create_user(session, username, hashed_password, is_user, is_developer, is_admin)

    return {"message": "User registered successfully"}

# Вход пользователя
@auth_routes.post("/login")
async def login(
    username: str = Form(...),
    password: str = Form(...),
    session: AsyncSession = Depends(get_async_session)
):
    if username == HARDCODED_USER["username"] and password == HARDCODED_USER["password"]:
        # Добавляем пользователя в active_users
        active_users[username] = True

        response = RedirectResponse(url="/success_login", status_code=302)
        response.set_cookie(key="username", value=username)
        return response
    else:
        raise HTTPException(status_code=400, detail="Invalid username or password")

# Получение имени пользователя из cookie
@auth_routes.get("/user_name")
async def get_user_name(username: str = Cookie(None)):
    if username:
        return {"username": username}
    else:
        raise HTTPException(status_code=401, detail="User not logged in")

# Выход пользователя
@auth_routes.get("/logout")
async def logout(response: JSONResponse, username: str = Cookie(None)):
    if username in active_users:
        del active_users[username]
        response.delete_cookie("username")
        return RedirectResponse(url="/login")
    else:
        return RedirectResponse(url="/login")

# Успешный вход
@auth_routes.get("/success_login", response_class=HTMLResponse)
def redirect():
    return RedirectResponse('/main_page')

# Главная страница пользователя
@user_routes.get("/main_page", response_class=HTMLResponse)
async def main_page(request: Request, username: str = Depends(get_current_user)):
    return templates.TemplateResponse("main_page.html", {"request": request, "username": username})

# Генерация случайных координат
def generate_random_coordinates():
    return [random.uniform(-90, 90), random.uniform(-180, 180)]

# Отображение карты
@map_routes.get("/map", response_class=HTMLResponse)
async def map():
    m = folium.Map(location=[0, 0], zoom_start=1)
    map_html = m.get_root().render()
    return HTMLResponse(content=map_html)

# Обновление маркера на карте
@map_routes.get("/update_marker")
async def update_marker():
    new_coordinates = generate_random_coordinates()
    return {"lat": new_coordinates[0], "lng": new_coordinates[1]}
