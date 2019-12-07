from fastapi import FastAPI
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response, PlainTextResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from starlette.authentication import (
    AuthenticationBackend, AuthenticationError, SimpleUser, UnauthenticatedUser,
    AuthCredentials
)
from starlette import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
import base64
import binascii
#models
#from models.User import User


class BasicAuthBackend(AuthenticationBackend):
    async def authenticate(self, request):
        if "Authorization" not in request.headers:
            return

        auth = request.headers["Authorization"]
        try:
            scheme, credentials = auth.split()
            if scheme.lower() != 'basic':
                return
            decoded = base64.b64decode(credentials).decode("ascii")
        except (ValueError, UnicodeDecodeError, binascii.Error) as exc:
            raise AuthenticationError('Invalid basic auth credentials')

        username, _, password = decoded.partition(":")
        # TODO: You'd want to verify the username and password here.
        return AuthCredentials(["authenticated"]), SimpleUser(username)


async def homepage(request):
    if request.user.is_authenticated:
        return PlainTextResponse('Hello, ' + request.user.display_name)
    return PlainTextResponse('Hello, you')

routes = [
    Route("/", endpoint=homepage)
]

middleware = [
    Middleware(AuthenticationMiddleware, backend=BasicAuthBackend())
]

app = Starlette(routes=routes, middleware=middleware)
main = Starlette()
app = FastAPI()  # Use eg. `@app.route()` to configure this.
blog = FastAPI()  # Use eg. `@blog.route()` to configure this.

main.host('localhost', app)
main.host('api.localhost', blog)

#setting up app object and templating engine
app.mount("/static", StaticFiles(directory="../frontend/public"), name="public")

templates = Jinja2Templates(directory="../frontend/templates")

@app.get("/")
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "user": "vancer", "username": "vancerbtw"})


@app.get("/login")
def present_login(request: Request, redirect="https://blazerepo.com"):
    return RedirectResponse(url='/')
    # return templates.TemplateResponse("login.html", {"redirect": redirect, "request": request})
