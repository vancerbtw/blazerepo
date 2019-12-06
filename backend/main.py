from fastapi import FastAPI
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="../frontend/public"), name="public")
templates = Jinja2Templates(directory="../frontend/templates")


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "user": "vancer", "username": "vancerbtw"})
