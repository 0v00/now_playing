import sqlite3
from contextlib import contextmanager

DATABASE_PATH = "app/database/movies.db"

@contextmanager
def get_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS movies (
                movie_id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                genres TEXT,
                keywords TEXT,
                last_scraped DATE NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS showtimes (
                showtime_id TEXT PRIMARY KEY,
                movie_id TEXT NOT NULL,
                times TEXT NOT NULL,
                valid_for DATE NOT NULL,
                FOREIGN KEY (movie_id) REFERENCES movies (movie_id)
            )
        ''')

        conn.commit()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
