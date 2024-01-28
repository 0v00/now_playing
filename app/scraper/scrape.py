import asyncio
import aiohttp
import json
from bs4 import BeautifulSoup
from datetime import datetime
from ..database.db_utils import movie_exists, get_last_scraped_date, insert_or_update_movie, insert_showtimes
from .utils import clean_movie_title, movies_search, get_movie_genres_by_id, get_movie_keywords, find_best_match
from dotenv import load_dotenv

load_dotenv()

async def scrape_movie_titles_times(session, url):
    async with session.get(url) as response:
        soup = BeautifulSoup(await response.text(), 'html.parser')

    movies_dict = {}
    for li in soup.select('ul.Sessions > li[data-name]'):
        title = li['data-name']
        title = clean_movie_title(title)
        times = [span.text for span in li.select('a > span.Time')]

        if title not in movies_dict:
            movies_dict[title] = {'times': [], 'genres': [], 'keywords': []}
        movies_dict[title]['times'].extend(times)

    return movies_dict

async def process_movie(session, title, movies_dict):
    print(f"Processing movie: {title}")

    existing_movie_id = movie_exists(title)
    last_scraped_date = get_last_scraped_date(existing_movie_id) if existing_movie_id else None

    # convert last_scraped_date to a date object if not None
    last_scraped_date = datetime.strptime(last_scraped_date, '%Y-%m-%d').date() if last_scraped_date else None

    if existing_movie_id and last_scraped_date == datetime.now().date():
        print(f"{title} has already been scraped today. Skipping.")
        return

    if not existing_movie_id:
        movie_details = await movies_search(session, title)
        if not movie_details:
            return

        candidates = movie_details.get('results', [])
        candidate_map = {result['title']: result for result in candidates}
        candidate_titles = list(candidate_map.keys())

        if candidate_titles:
            best_match_title = find_best_match(title, candidate_titles)
            best_match_object = candidate_map.get(best_match_title)

            if best_match_object:
                api_movie_id = best_match_object.get('id')
                api_genres, _ = await get_movie_genres_by_id(session, api_movie_id)
                api_keywords = await get_movie_keywords(session, api_movie_id)

                if api_genres:
                    movies_dict[clean_movie_title(title)]['genres'] = api_genres
                
                if api_keywords:
                    movies_dict[clean_movie_title(title)]['keywords'] = api_keywords

        db_movie_id = insert_or_update_movie(None, title, json.dumps(movies_dict[title]['genres']), json.dumps(movies_dict[title]['keywords']))
        insert_showtimes(db_movie_id, movies_dict[title]['times'])
    else:
        db_movie_id = existing_movie_id
        insert_showtimes(db_movie_id, movies_dict[title]['times'])

async def scrape_movies():
    print('Starting scraper...')
    url = 'https://www.ritzcinemas.com.au/now-showing'

    async with aiohttp.ClientSession() as session:
        movies_dict = await scrape_movie_titles_times(session, url)
        print(f"Found {len(movies_dict)} unique movie titles")

        await asyncio.gather(*(process_movie(session, title, movies_dict) for title in movies_dict.keys()))

    print("Scraper finished successfully")
    return movies_dict

if __name__ == "__main__":
    asyncio.run(scrape_movies())