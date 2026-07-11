from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.services.recommendation import (
    get_content_recommendations,
    get_genome_recommendations,
    get_collaborative_recommendations,
    get_hybrid_recommendations,
    data_store
)
from app.routers.movies import format_movie
from app.schemas.schemas import MovieResponse
from app.auth.auth_handler import get_current_user
from app.models.models import User

router = APIRouter(
    prefix="/recommend",
    tags=["Recommendations"]
)

@router.get("/content/{movie_id}", response_model=List[MovieResponse])
def recommend_content(movie_id: int):
    rec_ids = get_content_recommendations(movie_id)
    movies = data_store.get('movies')
    return [format_movie(movies[movies['movieId'] == m].iloc[0]) for m in rec_ids]

@router.get("/genome/{movie_id}", response_model=List[MovieResponse])
def recommend_genome(movie_id: int):
    rec_ids = get_genome_recommendations(movie_id)
    movies = data_store.get('movies')
    return [format_movie(movies[movies['movieId'] == m].iloc[0]) for m in rec_ids]

@router.get("/collaborative", response_model=List[MovieResponse])
def recommend_collaborative(current_user: User = Depends(get_current_user)):
    # Since new users won't be in the pre-trained SVD model, we map them to a valid user for demo,
    # or ideally update the model online. We use user_id = current_user.id if it exists, else 1.
    ratings = data_store.get('ratings')
    valid_users = set(ratings['userId'].unique())
    user_id = current_user.id if current_user.id in valid_users else 1
    
    rec_ids = get_collaborative_recommendations(user_id)
    movies = data_store.get('movies')
    return [format_movie(movies[movies['movieId'] == m].iloc[0]) for m in rec_ids]

@router.get("/hybrid/{movie_id}", response_model=List[MovieResponse])
def recommend_hybrid(movie_id: int, current_user: User = Depends(get_current_user)):
    ratings = data_store.get('ratings')
    valid_users = set(ratings['userId'].unique())
    user_id = current_user.id if current_user.id in valid_users else 1
    
    rec_ids = get_hybrid_recommendations(user_id, movie_id)
    movies = data_store.get('movies')
    return [format_movie(movies[movies['movieId'] == m].iloc[0]) for m in rec_ids]

@router.get("/trending", response_model=List[MovieResponse])
def trending_movies():
    ratings = data_store.get('ratings')
    movies = data_store.get('movies')
    if ratings is None or movies is None:
        return []
    trending_ids = ratings['movieId'].value_counts().head(10).index.tolist()
    return [format_movie(movies[movies['movieId'] == m].iloc[0]) for m in trending_ids if not movies[movies['movieId'] == m].empty]

@router.get("/top-rated", response_model=List[MovieResponse])
def top_rated_movies():
    ratings = data_store.get('ratings')
    movies = data_store.get('movies')
    if ratings is None or movies is None:
        return []
    stats = ratings.groupby('movieId')['rating'].agg(['count', 'mean'])
    top_ids = stats[stats['count'] > 100].sort_values('mean', ascending=False).head(10).index.tolist()
    return [format_movie(movies[movies['movieId'] == m].iloc[0]) for m in top_ids if not movies[movies['movieId'] == m].empty]

@router.get("/latest", response_model=List[MovieResponse])
def latest_movies():
    movies = data_store.get('movies')
    if movies is None:
        return []
    latest_ids = movies.sort_values('movieId', ascending=False).head(10)['movieId'].tolist()
    return [format_movie(movies[movies['movieId'] == m].iloc[0]) for m in latest_ids if not movies[movies['movieId'] == m].empty]
