# 🎬 MovieVerse

MovieVerse is a complete, production-ready AI-powered Movie Recommendation System. It features a modern, premium dark-themed React frontend and a FastAPI backend that serves content-based, collaborative filtering, genome-based, and hybrid AI recommendations.

## Tech Stack
- **Frontend**: React 19, Vite, React Router DOM, Axios, Context API, Vanilla CSS (Glassmorphism).
- **Backend**: FastAPI, SQLAlchemy, PostgreSQL, Passlib (bcrypt), JWT, Python (Pandas, Scikit-learn, Joblib).

## Features
- **Authentication**: JWT-based secure signup, login, and protected routes.
- **AI Recommendations**:
  - **Content-Based**: Recommends movies similar to a given movie using TF-IDF.
  - **Collaborative Filtering**: Predicts user ratings for unseen movies using SVD.
  - **Genome-Based**: Uses MovieLens genome tags to find semantically similar movies.
  - **Hybrid AI**: A weighted mix of content and collaborative algorithms for logged-in users.
- **User Engagement**: Add movies to Watchlist, Favorites, and Rate movies to improve AI predictions.
- **TMDB Integration**: Enriches data with dynamic movie posters, backdrops, and descriptions.
- **Live Search**: Debounced real-time movie search.

## Project Structure
```text
movie-recommendation-system/
├── backend/
│   ├── app/
│   │   ├── auth/          # JWT and Password utilities
│   │   ├── database/      # SQLAlchemy configuration
│   │   ├── models/        # Database models (User, Favorite, Rating, Watchlist)
│   │   ├── routers/       # API endpoints
│   │   ├── schemas/       # Pydantic schemas for data validation
│   │   ├── services/      # Recommendation engine & TMDB fetcher
│   │   └── main.py        # FastAPI entrypoint & lifespan events
│   ├── data/              # CSV Datasets (movies.csv, ratings.csv, etc.)
│   ├── models/            # Trained Models (.pkl files)
│   └── requirements.txt   # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/    # Reusable React components
│   │   ├── contexts/      # AuthContext
│   │   ├── pages/         # React pages (Home, Movie, Search, etc.)
│   │   ├── services/      # Axios API configuration
│   │   ├── App.jsx        # Routing
│   │   ├── index.css      # Vanilla CSS Design System
│   │   └── main.jsx       # React entrypoint
│   └── package.json
└── README.md
```

## Setup & Installation

### 1. PostgreSQL Database Setup
Ensure you have PostgreSQL installed and running locally.
Create a database named `movie_db`:
```sql
CREATE DATABASE movie_db;
```

### 2. Environment Variables
The backend relies on environment variables for sensitive configuration. A `.env` file should be located at `backend/.env`.

**`backend/.env`**:
```ini
DATABASE_URL="postgresql://postgres:yourpassword@localhost:5432/movie_db"
TMDB_API_KEY="your_tmdb_api_key"
SECRET_KEY="your_32_bit_hashing_key"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```
> Note: If your PostgreSQL password contains special characters like `@`, URL-encode it (e.g., `%40`).

### 3. Backend Setup

1. Open a terminal and navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install "fastapi[all]" uvicorn sqlalchemy psycopg2 pydantic pydantic-settings passlib[bcrypt] python-jose[cryptography] joblib pandas scikit-learn numpy python-dotenv requests
   ```
4. Ensure your trained models and datasets are placed inside `backend/models/` and `backend/data/`.
5. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```
   > The server will take several seconds to start up as it loads the massive datasets and models directly into memory.

### 4. Frontend Setup

1. Open a new terminal and navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install Node dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```
4. Open the application in your browser (usually `http://localhost:5173`).

## Usage
- **Sign up / Login** to access AI recommendations tailored for you.
- Browse **Trending** and **Top Rated** carousels.
- Use the **Search Bar** to dynamically look up any movie.
- Click on a movie to view TMDB enriched details, add to **Favorites** / **Watchlist**, or see **Similar Movies**.
