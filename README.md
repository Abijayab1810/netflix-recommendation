# Netflix Movie Recommendation System

A FastAPI-based REST API for getting movie recommendations using content-based filtering with cosine similarity.

## Overview

This system analyzes movie metadata (genres, keywords, cast, crew, overview) and uses machine learning to recommend similar movies. Recommendations are based on cosine similarity between movie feature vectors.

## Features

- 🎬 Content-based movie recommendations
- 📊 Built with TMDB movie dataset (5000+ movies)
- 🚀 FastAPI with auto-generated API documentation
- 🐳 Docker containerization for easy deployment
- 📝 Interactive Swagger UI at `/docs`
- 🔄 CORS enabled for frontend integration

## Project Structure

```
.
├── main.py                      # FastAPI application
├── netflix.ipynb               # Jupyter notebook with model training
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker image configuration
├── docker-compose.yml          # Docker Compose configuration
├── movies.pkl                  # Preprocessed movies data
├── similarity.pkl              # Pre-computed similarity matrix
├── movie_dict.pkl              # Movie dictionary
├── tmdb_5000_movies.csv        # Raw movie data
├── tmdb_5000_credits.csv       # Raw credits data
└── README.md                   # This file
```

## Prerequisites

- Docker and Docker Compose (recommended)
  - OR
- Python 3.11+
- pip package manager

## Quick Start with Docker (Recommended)

### 1. Build and Run with Docker Compose

```bash
# Navigate to project directory
cd d:\projects\netflix\ recommendation\ system\movie_recom_data

# Start the application
docker-compose up --build
```

The API will be available at: `http://localhost:8000`

### 2. Access the API

- **Interactive Documentation**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/

### 3. Stop the Application

```bash
docker-compose down
```

## Local Installation (Without Docker)

### 1. Create Virtual Environment

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Application

```bash
python main.py
```

Or with uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### 1. Health Check
```
GET /
```
Returns API status and version information.

**Response:**
```json
{
  "message": "Netflix Movie Recommendation System API",
  "version": "1.0.0",
  "status": "running"
}
```

### 2. Get All Movies
```
GET /movies
```
Returns list of all available movies in the database.

**Response:**
```json
{
  "movies": ["Avatar", "Spectre", "The Dark Knight", ...],
  "count": 4803
}
```

### 3. Get Recommendations (POST)
```
POST /recommend
```
Get movie recommendations based on a movie title.

**Request Body:**
```json
{
  "movie_title": "Avatar",
  "num_recommendations": 5
}
```

**Response:**
```json
{
  "movie": "Avatar",
  "recommendations": [
    "Avatar: The Way of Water",
    "Titanic",
    "Inception",
    "The Day After Tomorrow",
    "Interstellar"
  ],
  "status": "success"
}
```

### 4. Get Recommendations (GET)
```
GET /recommend/{movie_title}?num_recommendations=5
```
Get movie recommendations using a simple GET request.

**Parameters:**
- `movie_title` (path): Movie title to get recommendations for
- `num_recommendations` (query, optional): Number of recommendations (1-10, default: 5)

**Example:**
```
http://localhost:8000/recommend/Avatar?num_recommendations=5
```

## Usage Examples

### Using curl

```bash
# Health check
curl http://localhost:8000/

# Get all movies
curl http://localhost:8000/movies

# Get recommendations (GET)
curl "http://localhost:8000/recommend/Avatar?num_recommendations=5"

# Get recommendations (POST)
curl -X POST http://localhost:8000/recommend \
  -H "Content-Type: application/json" \
  -d '{"movie_title": "Avatar", "num_recommendations": 5}'
```

### Using Python

```python
import requests

BASE_URL = "http://localhost:8000"

# Get recommendations
response = requests.post(
    f"{BASE_URL}/recommend",
    json={
        "movie_title": "Avatar",
        "num_recommendations": 5
    }
)

print(response.json())
```

### Using JavaScript/Fetch

```javascript
const movieTitle = "Avatar";
const numRecommendations = 5;

fetch(`http://localhost:8000/recommend/${movieTitle}?num_recommendations=${numRecommendations}`)
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));
```

## Docker Commands Reference

### Build the image manually
```bash
docker build -t netflix-recommender:latest .
```

### Run container manually
```bash
docker run -p 8000:8000 --name netflix-recommender netflix-recommender:latest
```

### View container logs
```bash
docker-compose logs -f movie-recommender
```

### Remove all containers and images
```bash
docker-compose down -v
docker rmi netflix-recommender:latest
```

## Deployment to Cloud

### AWS (EC2 + Docker)

1. Launch an EC2 instance (Amazon Linux 2 or Ubuntu)
2. Install Docker:
   ```bash
   sudo yum update -y  # Amazon Linux
   sudo yum install docker -y
   # or
   sudo apt-get install docker.io -y  # Ubuntu
   ```
3. Install Docker Compose:
   ```bash
   sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   sudo chmod +x /usr/local/bin/docker-compose
   ```
4. Clone or upload your project and run:
   ```bash
   docker-compose up -d
   ```

### Google Cloud Run

1. Push image to Google Container Registry:
   ```bash
   gcloud builds submit --tag gcr.io/PROJECT_ID/netflix-recommender
   ```
2. Deploy to Cloud Run:
   ```bash
   gcloud run deploy netflix-recommender \
     --image gcr.io/PROJECT_ID/netflix-recommender \
     --platform managed \
     --region us-central1
   ```

### Heroku

1. Install Heroku CLI
2. Create `Procfile`:
   ```
   web: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
3. Deploy:
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

## Model Information

### Training Data
- TMDB Movies Dataset: 5000+ movies
- Features: Genres, Keywords, Cast (top 3), Director, Overview

### Feature Processing
1. Text preprocessing (lowercasing, stemming)
2. CountVectorizer (max 5000 features, English stop words removed)
3. Cosine similarity calculation

### Performance
- Recommendation time: <50ms per request
- Memory footprint: ~100MB (depends on dataset size)

## Troubleshooting

### API not responding
```bash
# Check if container is running
docker-compose ps

# View logs
docker-compose logs movie-recommender

# Restart container
docker-compose restart
```

### Movie not found error
- The movie title must match exactly (case-sensitive)
- Use `/movies` endpoint to get exact movie titles
- Check spelling carefully

### Port already in use
Change port in `docker-compose.yml`:
```yaml
ports:
  - "8080:8000"  # Change 8080 to available port
```

### Out of memory
Increase Docker memory allocation in Docker Desktop settings

## API Documentation

Once running, visit **http://localhost:8000/docs** for interactive Swagger UI documentation where you can:
- Test all endpoints
- View request/response schemas
- See example requests
- Explore error codes

## Contributing

To retrain the model with new data:

1. Update CSV files
2. Run the Jupyter notebook: `netflix.ipynb`
3. This will generate new pickle files
4. Rebuild Docker image: `docker-compose build --no-cache`

## Performance Optimization Tips

1. **Caching**: Implement Redis for frequently requested movies
2. **Load Balancing**: Use multiple replicas in production
3. **Database**: Replace pickle files with a proper database (PostgreSQL, MongoDB)
4. **Scaling**: Use Kubernetes for large-scale deployments

## License

MIT License - Feel free to use and modify this project

## Support

For issues or questions:
1. Check API documentation at `/docs`
2. Review logs: `docker-compose logs -f`
3. Verify pickle files exist in project directory

---

**Ready to deploy? Run `docker-compose up --build` and access the API at http://localhost:8000** 🚀
