from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from app.routers.scraping_router import router as scraping_router

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.include_router(scraping_router)

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})