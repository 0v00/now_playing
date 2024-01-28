## now playing

Scraping today's movies from my local movie theatre so I can avoid any potential popups/notifications/etc.

- BeautifulSoup4 for scraping
- TMDB's API to get movie details like genre
- occasionally using the Levenshtein distance algorithm to match movie titles - [(read more here)](https://0v00.io/websites-as-non-places-scraping-and-the-levenshtein-distance/)
- store movie info in an sqlite db
- send HTML over the wire using Jinja2 for template rendering and HTMX for dynamic content updates
- a minimalist/neo-brutalist design style

## how to run

1. `python3 -m venv myvenv`
2. `source myvenv/bin/activate`
3. `pip3 install -r requirements.txt`
4. `python3 app/database/db_init.py` to init the db
5. `python3 app/scraper/scrape.py` to run the scraper
4. `uvicorn app.main:app --reload`
5. go to `http://localhost:8000/`

![screenshot](/screenshot.png)