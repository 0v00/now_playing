## now playing

Scraping today's movies from my local movie theatre so I can avoid any potential popups/notifications/etc.

- BeautifulSoup4 for scraping
- TMDB's API to get movie details like genre
- Occasionally using the Levenshtein distance algorithm to match movie titles - [(read more here)](https://0v00.io/websites-as-non-places-scraping-and-the-levenshtein-distance/)
- Deliver HTML over the wire using Jinja2 for template rendering and HTMX for dynamic content updates
- A simple brutalist design style

## how to run

1. `python3 -m venv myvenv`
2. `source myvenv/bin/activate`
3. `pip3 install -r requirements.txt`
4. `uvicorn app.main:app --reload`
5. go to `http://localhost:8000/`

![screenshot](/screenshot.png)