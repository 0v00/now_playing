from fastapi import APIRouter, HTTPException
from app.scraper.new_scrape import scrape_movies

router = APIRouter()

@router.get("/scrape-movies", response_model=dict)
async def scrape_movies_endpoint():
    try:
        movies_data = await scrape_movies()
        return movies_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))