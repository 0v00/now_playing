import sqlite3
import uuid
from datetime import datetime

DATABASE_PATH = "app/database/movies.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    return conn

def movie_exists(title):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT movie_id FROM movies WHERE title = ?", (title,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def get_last_scraped_date(movie_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT last_scraped FROM movies WHERE movie_id = ?", (movie_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def insert_or_update_movie(movie_id, title, genres, keywords):
    conn = get_db_connection()
    cursor = conn.cursor()
    today = datetime.now().date()
    if movie_id is None:
        movie_id = str(uuid.uuid4())
        cursor.execute("INSERT INTO movies (movie_id, title, genres, keywords, last_scraped) VALUES (?, ?, ?, ?, ?)", (movie_id, title, genres, keywords, today))
    else:
        cursor.execute("UPDATE movies SET genres = ?, keywords = ?, last_scraped = ? WHERE movie_id = ?", (genres, keywords, today, movie_id))
    conn.commit()
    conn.close()
    return movie_id

def insert_showtimes(movie_id, times):
    conn = get_db_connection()
    cursor = conn.cursor()
    today = datetime.now().date()
    for time in times:
        showtime_id = str(uuid.uuid4())
        cursor.execute("INSERT INTO showtimes (showtime_id, movie_id, times, valid_for) VALUES (?, ?, ?, ?)", (showtime_id, movie_id, time, today))
    conn.commit()
    conn.close()

def get_movies_with_showtimes():
    conn = sqlite3.connect("app/database/movies.db")
    cursor = conn.cursor()

    today = datetime.now().date().isoformat()

    query = """
    SELECT m.title, s.times
    FROM movies m
    INNER JOIN showtimes s ON m.movie_id = s.movie_id
    WHERE s.valid_for = ?
    """

    cursor.execute(query, (today,))
    rows = cursor.fetchall()
    conn.close()

    movies_data = {}
    for title, time in rows:
        if title not in movies_data:
            movies_data[title] = {'times': []}
        movies_data[title]['times'].append(time)

    return movies_data