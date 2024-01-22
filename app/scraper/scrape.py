import asyncio
import aiohttp
from bs4 import BeautifulSoup
from utils import clean_movie_title, movies_search, get_movie_genres_by_id, find_best_match
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
            movies_dict[title] = {'times': [], 'genres': []}
        movies_dict[title]['times'].extend(times)
    
    return movies_dict

async def process_movie(session, title, movies_dict):
    print(f"processing movie: {title}")
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
            movie_id = best_match_object.get('id')
            api_genres, _ = await get_movie_genres_by_id(session, movie_id)

            if api_genres:
                movies_dict[clean_movie_title(title)]['genres'] = api_genres

    else:
        print(f"no matching candidates found for {title}")

async def main():
    print('starting scraper...')
    url = 'https://www.ritzcinemas.com.au/now-showing'

    async with aiohttp.ClientSession() as session:
        movies_dict = await scrape_movie_titles_times(session, url)
        print(f"found {len(movies_dict)} unique movie titles")

        await asyncio.gather(*(process_movie(session, title, movies_dict) for title in movies_dict.keys()))

    print(dict(filter(lambda movie: "Action" in movie[1]['genres'], movies_dict.items())))
    print(movies_dict)
    print("scraper finished successfully")

asyncio.run(main())