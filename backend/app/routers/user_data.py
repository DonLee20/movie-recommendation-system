from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.database import get_db
from app.auth.auth_handler import get_current_user
from app.models.models import User, Favorite, Watchlist, Rating
from app.schemas.schemas import FavoriteBase, FavoriteResponse, WatchlistBase, WatchlistResponse, RatingBase, RatingResponse, MovieResponse
from app.routers.movies import format_movie
from app.services.recommendation import data_store

router = APIRouter(
    tags=["User Data"]
)

@router.get("/favorites", response_model=List[MovieResponse])
def get_favorites(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    favorites = db.query(Favorite).filter(Favorite.user_id == current_user.id).all()
    movies = data_store.get('movies')
    return [format_movie(movies[movies['movieId'] == f.movie_id].iloc[0]) for f in favorites if not movies[movies['movieId'] == f.movie_id].empty]

@router.post("/favorites", response_model=FavoriteResponse)
def add_favorite(fav: FavoriteBase, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    existing = db.query(Favorite).filter(Favorite.user_id == current_user.id, Favorite.movie_id == fav.movie_id).first()
    if existing:
        return existing
    new_fav = Favorite(user_id=current_user.id, movie_id=fav.movie_id)
    db.add(new_fav)
    db.commit()
    db.refresh(new_fav)
    return new_fav

@router.delete("/favorites/{movie_id}")
def remove_favorite(movie_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    fav = db.query(Favorite).filter(Favorite.user_id == current_user.id, Favorite.movie_id == movie_id).first()
    if fav:
        db.delete(fav)
        db.commit()
    return {"status": "success"}

@router.get("/watchlist", response_model=List[MovieResponse])
def get_watchlist(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    watchlist = db.query(Watchlist).filter(Watchlist.user_id == current_user.id).all()
    movies = data_store.get('movies')
    return [format_movie(movies[movies['movieId'] == w.movie_id].iloc[0]) for w in watchlist if not movies[movies['movieId'] == w.movie_id].empty]

@router.post("/watchlist", response_model=WatchlistResponse)
def add_watchlist(item: WatchlistBase, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    existing = db.query(Watchlist).filter(Watchlist.user_id == current_user.id, Watchlist.movie_id == item.movie_id).first()
    if existing:
        return existing
    new_item = Watchlist(user_id=current_user.id, movie_id=item.movie_id)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

@router.delete("/watchlist/{movie_id}")
def remove_watchlist(movie_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    item = db.query(Watchlist).filter(Watchlist.user_id == current_user.id, Watchlist.movie_id == movie_id).first()
    if item:
        db.delete(item)
        db.commit()
    return {"status": "success"}

@router.post("/ratings", response_model=RatingResponse)
def add_rating(rating: RatingBase, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    existing = db.query(Rating).filter(Rating.user_id == current_user.id, Rating.movie_id == rating.movie_id).first()
    if existing:
        existing.rating = rating.rating
        db.commit()
        db.refresh(existing)
        return existing
    new_rating = Rating(user_id=current_user.id, movie_id=rating.movie_id, rating=rating.rating)
    db.add(new_rating)
    db.commit()
    db.refresh(new_rating)
    return new_rating

@router.get("/profile")
def get_profile(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "created_at": current_user.created_at
    }
