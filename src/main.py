import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import os
import pymysql

# Constants
DATA_FILE = "imdb_top_250.json"

# Database connection setup
DB_CONFIG = {
    'host': 'localhost',
    'user': 'imdb_user',
    'password': 'admin',
    'database': 'imdb',
    'port': 3306 
}

def fetch_imdb_top_250():
    """Fetch IMDb Top 250 movies."""
    url = "https://www.imdb.com/chart/top/"
    headers = {
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
        'Accept-Language': 'en-US;q=0.5,en;q=0.3',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1'
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch IMDb page: {response.status_code}")

    soup = BeautifulSoup(response.content, 'html.parser')
    json_script = soup.find('script', {'type': "application/ld+json"})
    if not json_script:
        raise Exception("Failed to find JSON-LD data on the IMDb page.")

    json_data = json.loads(json_script.string)
    if 'itemListElement' not in json_data:
        raise Exception("Unexpected JSON-LD structure from IMDb page.")

    movies = []
    for idx, item in enumerate(json_data['itemListElement'], start=1):
        movies.append({
            "rank": idx,
            "title": item['item']['name'],
            "url": item['item']['url'],
            "rating": item['item'].get('aggregateRating', {}).get('ratingValue', 'N/A'),
            "date": datetime.now().strftime('%Y-%m-%d')  # Add today's date
        })

    return movies

def load_previous_data():
    """Load previous IMDb Top 250 data."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return []

def save_data(data):
    """Save IMDb Top 250 data to a file."""
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

def track_rank_changes(new_data, old_data):
    """Track ranking changes compared to the previous day."""
    old_rank_map = {movie["title"]: movie["rank"] for movie in old_data}
    for movie in new_data:
        old_rank = old_rank_map.get(movie["title"])
        if old_rank:
            movie["rank_change"] = old_rank - movie["rank"]
        else:
            movie["rank_change"] = "New Entry"
    return new_data

def save_to_mysql(data):
    """Save IMDb Top 250 data to MySQL database."""
    connection = None  # Initialize connection variable
    try:
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # Clear previous data
        cursor.execute("DELETE FROM top_250_movies")

        # Insert data into the table
        for movie in data:
            cursor.execute("""
                INSERT INTO top_250_movies (`rank`, title, url, rating, date, rank_change)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                movie['rank'],
                movie['title'],
                movie['url'],
                movie['rating'],
                datetime.strptime(movie['date'], '%Y-%m-%d'),
                movie['rank_change']
            ))

        connection.commit()
        print("Data successfully saved to MySQL.")
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
    finally:
        if connection:
            connection.close()


def main():
    """Main function to scrape IMDb Top 250 and track rank changes."""
    print("Fetching IMDb Top 250 movies...")
    current_data = fetch_imdb_top_250()
    print("Loaded current data.")

    print("Loading previous data...")
    previous_data = load_previous_data()

    print("Tracking rank changes...")
    updated_data = track_rank_changes(current_data, previous_data)

    print("Saving data to database...")
    save_to_mysql(updated_data)

    print("Saving updated data to JSON...")
    save_data(updated_data)
    print(f"Data saved to {DATA_FILE}.")

if __name__ == "__main__":
    main()

