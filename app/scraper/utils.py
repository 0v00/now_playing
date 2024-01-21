import os
import requests
from urllib.parse import quote

tmdb_url = os.getenv("TMDB_URL")
api_key = os.getenv("API_KEY")

def clean_movie_title(title, substrings=None):
    if substrings is None:
        substrings = ["(Dubbed)", "(Subbed)", "35mm", "70mm"]
    for substring in substrings:
        title = title.replace(substring, '')
    return title

def movies_search(movie_title):
    uri_encoded_title = quote(movie_title)
    search_url = f"{tmdb_url}/3/search/movie?api_key={api_key}&query={uri_encoded_title}&include_adult=false&language=en-US&page=1"
    try:
        response = requests.get(search_url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"an error occurred: {e}")
        return None
    
def get_movie_genres_by_id(movie_id):
    search_url = f"{tmdb_url}/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    try:
        response = requests.get(search_url)
        response.raise_for_status()
        data = response.json()
        genres = [genre['name'] for genre in data.get('genres', [])]
        title = data.get('title', 'Unknown')
        return genres, title
    except requests.RequestException as e:
        print(f"an error occurred: {e}")
        return None
    
def l_distance(title1, title2):
    if len(title1) == 0 or len(title2) == 0:
        return len(title1) + len(title2)
    
    if title1[0] == title2[0]:
        return l_distance(title1[1:], title2[1:])
    
    return 1 + min(
        l_distance(title1, title2[1:]),
        l_distance(title1[1:], title2),
        l_distance(title1[1:], title2[1:])
    )

def l_distance_dynamic(title1, title2):
    rows = len(title1) + 1
    cols = len(title2) + 1

    dp = [[0 for _ in range(cols)] for _ in range(rows)]

    for i in range(rows):
        dp[i][0] = i
    for j in range(cols):
        dp[0][j] = j
    
    for i in range(1, rows):
        for j in range(1, cols):
            if title1[i - 1] == title2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],
                    dp[i][j - 1],
                    dp[i - 1][j - 1]
                )
    return dp[-1][-1]
    
def find_best_match(title, candidates):
    best_match = None
    smallest_distance = float('inf')
    title = title.lower()
    for candidate in candidates:
        candidate_lower = candidate.lower()
        if title == candidate_lower:
            best_match = candidate
            return best_match
        print(f"computing levenshtein distance for {title} and {candidate}")
        distance = l_distance_dynamic(title, candidate)
        if distance < smallest_distance:
            smallest_distance = distance
            best_match = candidate
    return best_match