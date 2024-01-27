from fastapi import APIRouter, HTTPException, Request
from fastapi.templating import Jinja2Templates
from app.scraper.scrape import scrape_movies

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/scrape-movies")
async def scrape_movies_endpoint(request: Request):
    try:
        movies_data = await scrape_movies()
        return templates.TemplateResponse("movies_list.html", {"request": request, "movies": movies_data})
        # return movies_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))