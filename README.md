## now playing

Scraping today's movies from my local movie theatre so I can avoid any potential popups/notifications/etc.

- BeautifulSoup4 for scraping
- TMDB's API to get movie details like genre
- occasionally use the Levenshtein distance algorithm to match movie titles
- store movie info in an sqlite db
- send HTML over the wire using Jinja2 for template rendering and HTMX for dynamic content updates
- if a movie has already started, we add `line-through` styling to that showtime
- a minimalist/neo-brutalist design style

## how to run

1. `python3 -m venv myvenv` and `source myvenv/bin/activate`
2. `pip3 install -r requirements.txt`
4. initialize the db: `python3 app/database/db_init.py`
5. run the scrape module: `python3 -m app.scraper.scrape`
4. start the server: `uvicorn app.main:app --reload`
5. go to `http://localhost:8000/`

![screenshot](/screenshot.png)
_*default content when first scraped - no movies have started yet, so none are crossed out*_

![content if a movie has started](/screenshot2.png)
_*crossed out movies if they have already started/finished playing*_

![fallback content if nothing scraped](/screenshot3.png)
_*fallback content if scraper has not yet run in the morning*_
