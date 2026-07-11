from fastapi import APIRouter, HTTPException, Query
from app.services.recommendation import data_store
from app.services.tmdb import get_tmdb_details
from app.schemas.schemas import MovieResponse
from typing import List
import math

router = APIRouter(
    prefix="/movies",
    tags=["Movies"]
)

def format_movie(row):
    # Fetch TMDB info
    links = data_store['links']
    tmdb_row = links[links['movieId'] == row['movieId']]
    tmdb_id = tmdb_row['tmdbId'].values[0] if not tmdb_row.empty else None
    
    tmdb_data = get_tmdb_details(tmdb_id)
    
    # Calculate average rating
    ratings = data_store['ratings']
    movie_ratings = ratings[ratings['movieId'] == row['movieId']]
    avg_rating = movie_ratings['rating'].mean() if not movie_ratings.empty else 0.0
    
    if math.isnan(avg_rating):
        avg_rating = 0.0
        
    return MovieResponse(
        movieId=int(row['movieId']),
        title=str(row['title']),
        genres=str(row['genres']),
        average_rating=round(float(avg_rating), 1),
        poster=tmdb_data.get("poster"),
        backdrop=tmdb_data.get("backdrop"),
        overview=tmdb_data.get("overview"),
        runtime=tmdb_data.get("runtime"),
        release_date=tmdb_data.get("release_date")
    )

@router.get("/search", response_model=List[MovieResponse])
def search_movies(query: str = Query(..., min_length=1)):
    movies = data_store.get('movies')
    if movies is None or movies.empty:
        return []
    
    # Case insensitive search
    matches = movies[movies['title'].str.contains(query, case=False, na=False)].head(20)
    
    results = []
    for _, row in matches.iterrows():
        results.append(format_movie(row))
    return results

@router.get("/{movie_id}", response_model=MovieResponse)
def get_movie(movie_id: int):
    movies = data_store.get('movies')
    if movies is None:
        raise HTTPException(status_code=500, detail="Data not loaded")
        
    movie_row = movies[movies['movieId'] == movie_id]
    if movie_row.empty:
        raise HTTPException(status_code=404, detail="Movie not found")
        
    return format_movie(movie_row.iloc[0])
