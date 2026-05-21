from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(title="REVEAL")

app.mount("/static", StaticFiles(directory="backend/static"), name="static")

templates = Jinja2Templates(directory="backend/templates")


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
