from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from backend.routes.upload_routes import router as upload_router
from backend.routes.function_routes import (
    router as function_router,
)
from backend.routes.ai_routes import (
    router as ai_router,
)

app = FastAPI(title="REVEAL")

origins = [
    "https://reveal-eugpxspie-victor-s-projects-1827.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="backend/static"), name="static")

templates = Jinja2Templates(directory="backend/templates")

app.include_router(upload_router)
app.include_router(function_router)
app.include_router(ai_router)


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request},
    )
