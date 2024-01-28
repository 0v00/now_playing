from fastapi import APIRouter, HTTPException, Request
from fastapi.templating import Jinja2Templates
from app.database.db_utils import get_movies_with_showtimes

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/get-movies")
async def get_movies(request: Request):
    try:
        movies_data = get_movies_with_showtimes()
        print("Movies Data:", movies_data)
        return templates.TemplateResponse("movies_list.html", {"request": request, "movies": movies_data})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))