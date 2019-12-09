from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from helpers.Authentication import Authentication
import jwt
from jwt import PyJWTError
#from models.User import User

main = Starlette()
app = FastAPI()  # Use eg. `@app.route()` to configure this.
blog = FastAPI()  # Use eg. `@blog.route()` to configure this.

main.host('localhost', app)
main.host('api.localhost', blog)

# setting up app object and templating engine
app.mount("/static", StaticFiles(directory="../frontend/public"), name="public")

templates = Jinja2Templates(directory="../frontend/templates")

@app.get("/")
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "user": "vancer", "username": "vancerbtw"})


@app.get("/login")
def present_login(request: Request, redirect="https://blazerepo.com"):
    return RedirectResponse(url='/')
    # return templates.TemplateResponse("login.html", {"redirect": redirect, "request": request})
