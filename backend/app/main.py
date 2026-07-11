import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.database import engine, Base
from app.routers import auth, movies, recommend, user_data
from app.services.recommendation import load_data_and_models

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables
    Base.metadata.create_all(bind=engine)
    
    # Load models and datasets
    load_data_and_models()
    yield
    # Cleanup if necessary
    pass

app = FastAPI(title="MovieVerse API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(movies.router)
app.include_router(recommend.router)
app.include_router(user_data.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to MovieVerse API"}
