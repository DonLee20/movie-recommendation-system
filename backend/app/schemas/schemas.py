from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# User Schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Movie / User Data Schemas
class FavoriteBase(BaseModel):
    movie_id: int

class FavoriteResponse(FavoriteBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

class WatchlistBase(BaseModel):
    movie_id: int

class WatchlistResponse(WatchlistBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

class RatingBase(BaseModel):
    movie_id: int
    rating: float

class RatingResponse(RatingBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

class MovieResponse(BaseModel):
    movieId: int
    title: str
    genres: str
    average_rating: float = 0.0
    poster: Optional[str] = None
    backdrop: Optional[str] = None
    overview: Optional[str] = None
    runtime: Optional[int] = None
    release_date: Optional[str] = None
