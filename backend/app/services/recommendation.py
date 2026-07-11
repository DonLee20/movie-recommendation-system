import os
import joblib
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity

# Global variables for data and models
data_store = {}

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "models")

def load_data_and_models():
    print("Loading datasets into memory (this may take a while)...")
    data_store['movies'] = pd.read_csv(os.path.join(DATA_DIR, "movies.csv"))
    data_store['ratings'] = pd.read_csv(os.path.join(DATA_DIR, "ratings.csv"))
    data_store['links'] = pd.read_csv(os.path.join(DATA_DIR, "links.csv"))
    data_store['tags'] = pd.read_csv(os.path.join(DATA_DIR, "tags.csv"))
    data_store['genome_tags'] = pd.read_csv(os.path.join(DATA_DIR, "genome-tags.csv"))
    data_store['genome_scores'] = pd.read_csv(os.path.join(DATA_DIR, "genome-scores.csv"))
    
    print("Loading trained models...")
    data_store['tfidf_matrix'] = joblib.load(os.path.join(MODELS_DIR, "tfidf_matrix.pkl"))
    data_store['movie_indices'] = joblib.load(os.path.join(MODELS_DIR, "movies.pkl"))
    data_store['genome_matrix'] = joblib.load(os.path.join(MODELS_DIR, "genome_matrix.pkl"))
    data_store['svd_model'] = joblib.load(os.path.join(MODELS_DIR, "svd_model.pkl"))
    
    # We create a reverse mapping for movieIds
    # Assuming movie_indices maps Title -> Index
    data_store['movies'] = data_store['movies'].reset_index()
    print("All datasets and models loaded successfully!")

def get_content_recommendations(movie_id: int, top_n: int = 10):
    movies = data_store['movies']
    # Find the title or index for the movie_id
    movie_row = movies[movies['movieId'] == movie_id]
    if movie_row.empty:
        return []
    idx = movie_row.index[0]
    
    tfidf_matrix = data_store['tfidf_matrix']
    sim_scores = list(enumerate(linear_kernel(tfidf_matrix[idx], tfidf_matrix).flatten()))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:top_n+1]
    
    movie_indices_to_return = [i[0] for i in sim_scores]
    return movies.iloc[movie_indices_to_return]['movieId'].tolist()

def get_genome_recommendations(movie_id: int, top_n: int = 10):
    movies = data_store['movies']
    movie_row = movies[movies['movieId'] == movie_id]
    if movie_row.empty:
        return []
    idx = movie_row.index[0]
    
    genome_matrix = data_store['genome_matrix']
    # If genome_matrix is a dataframe or sparse matrix
    sim_scores = list(enumerate(cosine_similarity(genome_matrix[idx].reshape(1, -1), genome_matrix).flatten()))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:top_n+1]
    
    movie_indices_to_return = [i[0] for i in sim_scores]
    return movies.iloc[movie_indices_to_return]['movieId'].tolist()

def get_collaborative_recommendations(user_id: int, top_n: int = 10):
    movies = data_store['movies']
    ratings = data_store['ratings']
    svd = data_store['svd_model']
    
    # Movies user has rated
    rated_movies = ratings[ratings['userId'] == user_id]['movieId'].tolist()
    all_movies = movies['movieId'].tolist()
    unrated_movies = [m for m in all_movies if m not in rated_movies]
    
    # Predict ratings for unrated movies
    predictions = []
    for m_id in unrated_movies:
        pred = svd.predict(user_id, m_id)
        predictions.append((m_id, pred.est))
        
    predictions.sort(key=lambda x: x[1], reverse=True)
    return [m_id for m_id, _ in predictions[:top_n]]

def get_hybrid_recommendations(user_id: int, movie_id: int, top_n: int = 10):
    # Combine collaborative and content
    content_recs = get_content_recommendations(movie_id, top_n * 2)
    collab_recs = get_collaborative_recommendations(user_id, top_n * 2)
    
    hybrid_recs = list(set(content_recs + collab_recs))
    # In a real scenario we'd weight them, but let's just return a mix
    # We will score them based on SVD predictions for this user
    svd = data_store['svd_model']
    scored_hybrid = []
    for m in hybrid_recs:
        pred = svd.predict(user_id, m)
        scored_hybrid.append((m, pred.est))
        
    scored_hybrid.sort(key=lambda x: x[1], reverse=True)
    return [m for m, _ in scored_hybrid[:top_n]]
