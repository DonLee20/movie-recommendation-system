import os
import requests
import pandas as pd

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

def get_tmdb_details(tmdb_id):
    if pd.isna(tmdb_id) or not tmdb_id:
        return {}
    
    url = f"{BASE_URL}/movie/{int(tmdb_id)}?api_key={TMDB_API_KEY}&append_to_response=videos,credits"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            poster_path = data.get("poster_path")
            backdrop_path = data.get("backdrop_path")
            poster = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None
            backdrop = f"https://image.tmdb.org/t/p/original{backdrop_path}" if backdrop_path else None
            return {
                "poster": poster,
                "backdrop": backdrop,
                "overview": data.get("overview"),
                "runtime": data.get("runtime"),
                "release_date": data.get("release_date")
            }
    except Exception as e:
        print(f"Error fetching TMDB data for id {tmdb_id}: {e}")
    return {}
