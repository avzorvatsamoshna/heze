from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse
from auth.routes import auth_routes, user_routes, map_routes

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/templates", StaticFiles(directory="templates"), name="templates")

app.include_router(auth_routes)
app.include_router(user_routes)
app.include_router(map_routes)

@app.get("/")
def helloworld():
    return RedirectResponse(url="/login")
