import pickle
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List

app = FastAPI(
    title="Netflix Movie Recommendation System",
    description="API for getting movie recommendations based on content similarity",
    version="1.0.0"
)

# Add CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get the directory where main.py is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load the pre-trained models
try:
    movies = pickle.load(open(os.path.join(BASE_DIR, "movies.pkl"), "rb"))
    similarity = pickle.load(open(os.path.join(BASE_DIR, "similarity.pkl"), "rb"))
    print("Models loaded successfully!")
except FileNotFoundError as e:
    print(f"Error loading models: {e}")
    movies = None
    similarity = None


class RecommendationRequest(BaseModel):
    movie_title: str
    num_recommendations: int = 5


class RecommendationResponse(BaseModel):
    movie: str
    recommendations: List[str]
    status: str


class MovieListResponse(BaseModel):
    movies: List[str]
    count: int


@app.get("/", tags=["UI"])
async def root():
    """Serve the interactive web interface"""
    html_path = os.path.join(BASE_DIR, "app.html")
    if os.path.exists(html_path):
        return FileResponse(html_path, media_type="text/html")
    return {
        "message": "Netflix Movie Recommendation System API",
        "version": "1.0.0",
        "status": "running",
        "help": "Visit http://localhost:8000/docs for API documentation"
    }


@app.get("/health", tags=["Health Check"])
async def health_check():
    """Health check endpoint"""
    return {
        "message": "Netflix Movie Recommendation System API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/movies", response_model=MovieListResponse, tags=["Movies"])
async def get_all_movies():
    """Get list of all available movies"""
    if movies is None:
        raise HTTPException(status_code=500, detail="Models not loaded")
    
    movie_list = movies["title"].tolist()
    return {
        "movies": movie_list,
        "count": len(movie_list)
    }


@app.post("/recommend", response_model=RecommendationResponse, tags=["Recommendations"])
async def recommend(request: RecommendationRequest):
    """
    Get movie recommendations based on a movie title.
    
    - **movie_title**: The title of the movie to base recommendations on
    - **num_recommendations**: Number of recommendations to return (default: 5, max: 10)
    """
    
    if movies is None or similarity is None:
        raise HTTPException(status_code=500, detail="Models not loaded")
    
    # Validate input
    if num_recommendations := request.num_recommendations:
        if num_recommendations > 10:
            num_recommendations = 10
        elif num_recommendations < 1:
            num_recommendations = 5
    else:
        num_recommendations = 5
    
    # Find the movie
    try:
        movie_index = movies[movies["title"] == request.movie_title].index[0]
    except IndexError:
        raise HTTPException(
            status_code=404,
            detail=f"Movie '{request.movie_title}' not found in database"
        )
    
    # Get similarity scores
    distances = similarity[movie_index]
    
    # Sort and get recommendations (exclude the movie itself with [1:])
    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:num_recommendations + 1]
    
    # Extract movie titles
    recommendations = [movies.iloc[i[0]]["title"] for i in movie_list]
    
    return {
        "movie": request.movie_title,
        "recommendations": recommendations,
        "status": "success"
    }


@app.get("/recommend/{movie_title}", response_model=RecommendationResponse, tags=["Recommendations"])
async def recommend_simple(movie_title: str, num_recommendations: int = 5):
    """
    Get movie recommendations using simple GET request.
    
    - **movie_title**: The title of the movie to base recommendations on
    - **num_recommendations**: Number of recommendations to return (default: 5, max: 10)
    """
    
    if movies is None or similarity is None:
        raise HTTPException(status_code=500, detail="Models not loaded")
    
    # Validate input
    if num_recommendations > 10:
        num_recommendations = 10
    elif num_recommendations < 1:
        num_recommendations = 5
    
    # Find the movie
    try:
        movie_index = movies[movies["title"] == movie_title].index[0]
    except IndexError:
        raise HTTPException(
            status_code=404,
            detail=f"Movie '{movie_title}' not found in database"
        )
    
    # Get similarity scores
    distances = similarity[movie_index]
    
    # Sort and get recommendations
    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:num_recommendations + 1]
    
    # Extract movie titles
    recommendations = [movies.iloc[i[0]]["title"] for i in movie_list]
    
    return {
        "movie": movie_title,
        "recommendations": recommendations,
        "status": "success"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
