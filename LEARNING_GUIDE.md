# 📚 Complete Learning Guide: Netflix Recommendation System Deployment

## Part 1: Understanding What You Have

Your Jupyter notebook (`netflix.ipynb`) does this:

```
Raw Data (CSV files)
    ↓
[Data Cleaning & Processing]
    ↓
[Feature Engineering - combines genres, cast, keywords, etc.]
    ↓
[TF-IDF Vectorization - converts text to numbers]
    ↓
[Cosine Similarity - calculates how similar movies are]
    ↓
Pickle Files (movies.pkl, similarity.pkl, movie_dict.pkl)
```

The pickle files are like **snapshots** of processed data saved to disk. You don't have to recalculate them every time!

---

## Part 2: What Each File Does

### 📄 **requirements.txt** - Dependencies (What Python needs)

```
fastapi==0.104.1          # Web framework for creating API
uvicorn==0.24.0           # Server that runs FastAPI
pandas==2.1.3             # Data manipulation
numpy==1.26.2             # Numerical computing
scikit-learn==1.3.2       # Machine learning library (has cosine_similarity)
nltk==3.8.1               # Natural Language Processing
python-multipart==0.0.6   # Handles file uploads
pydantic==2.5.0           # Data validation
```

**What it means:** When you run `pip install -r requirements.txt`, Python downloads and installs all these libraries.

---

### 🐍 **main.py** - The API Application

This is the **core** of your deployment. Let me explain each part:

#### Section 1: Setup

```python
from fastapi import FastAPI
app = FastAPI(title="Netflix Movie Recommendation System")
```

**What it does:** Creates a web server that listens for HTTP requests

#### Section 2: Load Models

```python
movies = pickle.load(open("movies.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))
```

**What it does:** 
- Loads your preprocessed movies data
- Loads precomputed similarity scores
- These are loaded **once** when the server starts (not every request!)

#### Section 3: API Endpoints

**Endpoint 1: Health Check**
```python
@app.get("/")
async def root():
    return {"status": "running"}
```

- URL: `http://localhost:8000/`
- Does: Returns API status
- Why: Tells you if the server is alive

**Endpoint 2: Get All Movies**
```python
@app.get("/movies")
async def get_all_movies():
    movie_list = movies["title"].tolist()
    return {"movies": movie_list, "count": len(movie_list)}
```

- URL: `http://localhost:8000/movies`
- Does: Returns list of all 4,803 movies
- Why: You need to know exact movie titles for recommendations

**Endpoint 3: Get Recommendations (POST)**
```python
@app.post("/recommend")
async def recommend(request: RecommendationRequest):
    movie_index = movies[movies["title"] == request.movie_title].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True)[1:6]
    recommendations = [movies.iloc[i[0]]["title"] for i in movie_list]
    return {"movie": request.movie_title, "recommendations": recommendations}
```

**Step-by-step breakdown:**
```
1. User sends: {"movie_title": "Avatar", "num_recommendations": 5}
2. Find index of "Avatar" in movies dataframe
3. Get similarity scores for Avatar against ALL movies
4. Sort scores from highest to lowest (most similar first)
5. Skip first one (Avatar itself) and take next 5
6. Return their titles
```

**Endpoint 4: Get Recommendations (GET)**
```python
@app.get("/recommend/{movie_title}")
async def recommend_simple(movie_title: str, num_recommendations: int = 5):
    # Same logic as POST but simpler URL
```

- URL: `http://localhost:8000/recommend/Avatar?num_recommendations=5`
- Does: Same as POST but easier to use in browser

---

### 🐳 **Dockerfile** - Container Recipe

Think of Docker like a recipe for building a computer:

```dockerfile
FROM python:3.11-slim
```
**Meaning:** Start with a pre-built Linux computer with Python 3.11

```dockerfile
WORKDIR /app
```
**Meaning:** Create folder `/app` and go inside (like `cd /app`)

```dockerfile
COPY requirements.txt .
RUN pip install -r requirements.txt
```
**Meaning:** 
1. Copy requirements.txt into the container
2. Install all dependencies

```dockerfile
COPY main.py .
COPY movies.pkl .
COPY similarity.pkl .
```
**Meaning:** Copy your application files into the container

```dockerfile
EXPOSE 8000
```
**Meaning:** Open port 8000 (like a door) so requests can enter

```dockerfile
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```
**Meaning:** When container starts, run this command (start the server)

---

### 🎯 **docker-compose.yml** - Multiple Container Manager

```yaml
version: '3.8'
services:
  movie-recommender:
    build: .                    # Build from Dockerfile in current directory
    container_name: netflix-recommender-api
    ports:
      - "8000:8000"            # Map port 8000 (host) → 8000 (container)
    restart: unless-stopped     # Restart if it crashes
    healthcheck:                # Check if service is healthy
      test: ["CMD", "curl", "-f", "http://localhost:8000/"]
      interval: 30s
```

**Simple explanation:**
- Build a container from Dockerfile
- Name it `netflix-recommender-api`
- Listen on port 8000
- If it crashes, restart automatically
- Every 30 seconds, check if it's still working

---

## Part 3: How It Works (End-to-End)

### Scenario: User wants recommendations for "Avatar"

```
USER'S BROWSER/CURL
        ↓
[Sends HTTP request]
        ↓
UVICORN SERVER (main.py)
        ↓
[Receives request at endpoint /recommend/Avatar]
        ↓
[Looks up "Avatar" in movies dataframe]
        ↓
[Gets similarity scores from similarity matrix]
        ↓
[Sorts and picks top 5]
        ↓
[Returns JSON with movie titles]
        ↓
USER GETS RESPONSE
{
  "movie": "Avatar",
  "recommendations": ["Titanic", "Inception", ...]
}
```

---

## Part 4: Installation & Running (What Happens)

### Step 1: Virtual Environment

```bash
python -m venv venv
```

**What it does:**
- Creates isolated Python environment
- Like having a separate folder just for this project
- Prevents conflicts with other Python projects

**Why?** Other projects might need different versions of libraries. This keeps everything organized.

```bash
venv\Scripts\activate
```

**What it does:**
- Activates the virtual environment
- Now `pip install` will install packages **only in this folder**, not system-wide

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

**What it does:**
- Reads `requirements.txt`
- Downloads and installs each library from the internet
- Installs dependencies of those libraries too (automatically)

**Example of dependency chain:**
```
fastapi depends on: starlette, pydantic, typing_extensions
starlette depends on: asgiref, anyio
... and so on
```

All happen automatically!

### Step 3: Run the API

```bash
python main.py
```

**What happens:**
```
1. Python loads main.py
2. Loads pickle files (movies.pkl, similarity.pkl)
3. Creates FastAPI app
4. Starts uvicorn server
5. Listens on http://0.0.0.0:8000
6. Waits for requests...
```

---

## Part 5: Making Requests (How Users Interact)

### Method 1: Browser (Simplest)

Go to: `http://localhost:8000/docs`

You see an interactive UI (Swagger) where you can:
- Click "Try it out"
- Enter parameters
- See responses

### Method 2: Curl (Command Line)

```bash
curl "http://localhost:8000/recommend/Avatar?num_recommendations=5"
```

**What it does:**
- Sends GET request to your API
- Receives JSON response
- Prints it in terminal

### Method 3: Python Script

```python
import requests

response = requests.post(
    "http://localhost:8000/recommend",
    json={"movie_title": "Avatar", "num_recommendations": 5}
)
print(response.json())
```

**What it does:**
- Sends HTTP POST request with JSON data
- Gets response
- Prints it

### Method 4: JavaScript/Frontend

```javascript
fetch("http://localhost:8000/recommend/Avatar?num_recommendations=5")
  .then(r => r.json())
  .then(data => console.log(data))
```

**What it does:**
- JavaScript in a web page can call your API
- Gets recommendations dynamically

---

## Part 6: Data Flow (What Movies Are Used)

### Original Jupyter Notebook Process

```
tmdb_5000_movies.csv (4,803 movies)
    ↓
[Extract: title, genres, keywords, overview, cast, crew]
    ↓
[Parse JSON strings into lists]
    ↓
[Lowercase everything]
    ↓
[Remove spaces: "Science Fiction" → "ScienceFiction"]
    ↓
[Stemming: "running" → "run", "movies" → "movi"]
    ↓
[Combine: overview + genres + keywords + cast + crew]
    ↓
[CountVectorizer: convert text to 5000 numbers]
    ↓
[Cosine Similarity: calculate distances between vectors]
    ↓
Save as pickle files ✓
```

### What the Pickle Files Contain

**movies.pkl:**
```
DataFrame with columns:
  - id: unique movie ID
  - title: movie name
  - tags: combined text (genres + keywords + cast + crew + overview)

Example row:
  id: 19995
  title: "Avatar"
  tags: "Avatar Science Fiction alien planet..."
```

**similarity.pkl:**
```
Matrix showing how similar each movie is to every other movie
Shape: (4803, 4803)

Example:
  similarity[0][100] = 0.87  (Movie 0 is 87% similar to movie 100)
  similarity[0][200] = 0.45  (Movie 0 is 45% similar to movie 200)
```

---

## Part 7: Deployment Patterns

### Pattern 1: Local (What You Need to Know Now)

```
Your Computer
    ↓
[Python virtual environment]
    ↓
[Python files + pickle files]
    ↓
[Uvicorn server on port 8000]
    ↓
[Accessible at http://localhost:8000]
```

**Pros:** Quick, easy to test, low resources
**Cons:** Not accessible from other computers, not production-ready

### Pattern 2: Docker (Next Step)

```
Your Computer
    ↓
[Docker container (like a virtual computer inside your computer)]
    ↓
[Has Linux OS + Python + your files]
    ↓
[Isolated from your system]
    ↓
[Portable - works on any machine with Docker]
```

**Pros:** Consistent, reproducible, portable
**Cons:** Requires Docker installed

### Pattern 3: Cloud Server (Production)

```
AWS/Google Cloud/Azure
    ↓
[Virtual Linux server in cloud]
    ↓
[Docker container running your API]
    ↓
[Accessible from internet with public IP]
    ↓
[Your API available 24/7]
```

**Pros:** Always online, accessible globally, scalable
**Cons:** Costs money, more complex setup

---

## Part 8: Common Questions Answered

### Q: Why pickle files?
**A:** Jupyter notebook processes 4,803 movies and calculates 4803×4803 similarity matrix. This takes 2-3 minutes. Pickle files save the result, so API loads in seconds.

### Q: Why FastAPI instead of other frameworks?
**A:** 
- Easy to use
- Auto-generates documentation
- Fast performance
- Great error messages

### Q: Why Uvicorn?
**A:** It's an **ASGI server** (Asynchronous Server Gateway Interface). FastAPI is a framework, Uvicorn is the server that runs it.

**Analogy:** FastAPI is a restaurant's recipe, Uvicorn is the kitchen that cooks it.

### Q: What's CORS?
**A:** Allows other websites to request data from your API. Without it, frontend on `example.com` can't call your API on `localhost:8000`.

### Q: Can multiple people use it at once?
**A:** Yes! Uvicorn handles concurrent requests (multiple at same time).

### Q: What if pickle files are missing?
**A:** Error on startup. You must run `netflix.ipynb` first to generate them.

---

## Part 9: Modification Examples

### Change 1: Get top 10 instead of 5 recommendations

In `main.py`, change:
```python
# OLD
)[1:6]  # Takes positions 1-5 (6 items, but skip first)

# NEW
)[1:11]  # Takes positions 1-10
```

### Change 2: Add minimum similarity threshold

```python
# Filter by score
movie_list = [(idx, score) for idx, score in enumerate(distances) if score > 0.5]
```

### Change 3: Add movie description to response

```python
# In recommend function
recommendations = [
    {
        "title": movies.iloc[i[0]]["title"],
        "similarity": float(i[1])  # How similar (0-1)
    }
    for i in movie_list
]
```

---

## Part 10: Running It (Complete Walkthrough)

### You already did:
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Next, run the API:
```bash
python main.py
```

You'll see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### Test it:
1. **Browser:** Go to `http://localhost:8000/docs`
2. **Curl:** 
   ```bash
   curl "http://localhost:8000/recommend/Avatar"
   ```

### Stop it:
Press `Ctrl+C`

---

## Summary

| Component | Purpose | Language |
|-----------|---------|----------|
| requirements.txt | List dependencies | Text |
| main.py | FastAPI application | Python |
| pickle files | Saved ML models | Binary |
| Dockerfile | Container recipe | Docker |
| docker-compose.yml | Container orchestration | YAML |
| test_api.py | Verify it works | Python |

**The flow:**
```
Jupyter Notebook (training)
    ↓ (generates pickle files)
FastAPI App (main.py)
    ↓ (runs on port 8000)
API Requests (GET/POST)
    ↓ (returns recommendations)
User/Frontend
```

---

You're all set! Run `python main.py` and start exploring! 🚀
