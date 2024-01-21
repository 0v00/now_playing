## now playing

Scraping today's movies from my local movie theatre so I don't have to actually browse their website.

I use TMDB's API to get more information about each movie - and sometimes I use the Levenshtein distance to help find the closest match from TMDB's API. [Read more here](https://0v00.io/websites-as-non-places-scraping-and-the-levenshtein-distance/).

## how to run

Unless you go to The Ritz cinema, I don't see why you would use this.

1. `python3 -m venv myvenv`
2. `source myvenv/bin/activate`
3. `pip3 install -r requirements.txt`
4. `python3 app/scraper/scrape.py`