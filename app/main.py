from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routers.movies_router import router as movies_router

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(movies_router)

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})