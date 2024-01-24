from fastapi import FastAPI
from app.routers import scraping_router

app = FastAPI()

app.include_router(scraping_router.router)