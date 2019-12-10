from fastapi import FastAPI, Form, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from dotenv import load_dotenv
import os

# importing auth and modules
from helpers.Authentication import Authentication
from helpers.Hash import Hash
from models.User import User

# importing database class
from database.Database import Database

load_dotenv()  # importing credentials

main = Starlette()
app = FastAPI()  # Use eg. `@app.route()` to configure this.
blog = FastAPI()  # Use eg. `@blog.route()` to configure this.

main.host('localhost', app)
main.host('api.localhost', blog)

# setting up app object and templating engine
app.mount("/static", StaticFiles(directory="../frontend/public"), name="public")

templates = Jinja2Templates(directory="../frontend/templates")

auth = Authentication(os.getenv("JWT_SECRET"))
hash = Hash()

db = Database(os.getenv("DB_URI"))

def get_current_user(request: Request):
    if auth_token := request.cookies.get("Authorization"):
        if token := auth_token[8:-1]:
            if current_user := jwt.decode(token, self.secret, algorithm='HS256'):
                if not current_user["disabled"]:
                    return current_user
                return  # disabled user
        return  # token isnt right format
    return  # no token

@app.get("/")
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "user": "vancer", "username": "vancerbtw"})


@app.get("/login")
def present_login(request: Request, redirect="https://blazerepo.com"):
    return templates.TemplateResponse("login.html", {"redirect": redirect, "request": request})


@app.post("/auth/login")
def authenticate_local(*, request: Request, email: str = Form(...), password: str = Form(...),
                       redirect="https://blazerepo.com"):
    if token := auth.login(email, password, db):
        if type(token) == str:
            print(redirect)
            response = RedirectResponse(url=f"{'/account'}")
            response.set_cookie(
                "Authorization",
                value=f"Bearer {token}",
                domain="localtest.me",
                httponly=True,
                max_age=1800,
                expires=1800,
            )
            return response
        raise HTTPException(status_code=401, detail=f'{token["error"]}')
    raise HTTPException(status_code=401, detail="Token could not be created")


@app.post("/register")
async def register_local(request: Request, name: str = Form(...), email: str = Form(...), password: str = Form(...),
                         password2: str = Form(...), redirect="https://blazerepo.com"):
    if user := auth.register_check(name, email, password, password2, db):
        if isinstance(user, User):
            db.add_user(user)
            return RedirectResponse(url=f"/login?showSignUp=true&success=User Successfully Registered")
        raise HTTPException(status_code=401, detail=f"{user['error']}")
    raise HTTPException(status_code=401, detail=f"{user['error']}")


@app.get("/account")
def present_account(request: Request, current_user: User = Depends(get_current_user)):
    print(current_user)
    print(request.cookies.get("Authorization"))
    return {
        "user": "test"
    }
