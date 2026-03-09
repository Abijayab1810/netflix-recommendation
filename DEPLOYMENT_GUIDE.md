# 🚀 Quick Start Deployment Guide

## What Was Created

Your Netflix recommendation system is now ready for deployment with:

✅ **FastAPI Application** (`main.py`)
- RESTful API with 4 endpoints
- Swagger/Redoc auto-documentation
- CORS enabled for frontend integration
- Error handling and input validation

✅ **Docker Setup** (`Dockerfile` + `docker-compose.yml`)
- Containerized application
- Health checks included
- Easy scaling and portability
- Production-ready configuration

✅ **Documentation** (`README.md`)
- Complete API reference
- Cloud deployment guides (AWS, Google Cloud, Heroku)
- Usage examples (curl, Python, JavaScript)
- Troubleshooting tips

✅ **Testing** (`test_api.py`)
- Automated test script
- Validates all API endpoints
- Easy verification after deployment

---

## 🎯 Next Steps to Deploy

### Option 1: Local Docker Deployment (Easiest)

#### Prerequisites
- Install [Docker Desktop](https://www.docker.com/products/docker-desktop) (includes docker-compose)
- Windows: Use PowerShell or Command Prompt
- macOS/Linux: Use Terminal

#### Deploy in 1 Command

```bash
cd "d:\projects\netflix recommendation system\movie_recom_data"
docker-compose up --build
```

✨ **That's it!** Your API is now running at: **http://localhost:8000**

#### Access the API

- **Interactive Docs**: http://localhost:8000/docs
- **Test Endpoint**: http://localhost:8000/recommend/Avatar?num_recommendations=5
- **All Movies**: http://localhost:8000/movies

---

### Option 2: Local Python Deployment (No Docker)

#### Prerequisites
- Python 3.11+
- pip

#### Steps

```bash
# 1. Navigate to project directory
cd "d:\projects\netflix recommendation system\movie_recom_data"

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the API
python main.py
```

API runs at: **http://localhost:8000**

---

### Option 3: Cloud Deployment

#### AWS EC2 (Recommended)

1. **Launch EC2 Instance**
   - Use Amazon Linux 2 or Ubuntu AMI
   - Allow inbound traffic on port 8000

2. **SSH into instance**
   ```bash
   ssh -i your-key.pem ec2-user@your-instance-ip
   ```

3. **Install Docker**
   ```bash
   sudo yum install docker -y
   sudo systemctl start docker
   sudo usermod -aG docker ec2-user
   ```

4. **Upload your project**
   ```bash
   scp -r -i your-key.pem . ec2-user@your-instance-ip:/home/ec2-user/app
   ```

5. **Run the application**
   ```bash
   ssh -i your-key.pem ec2-user@your-instance-ip
   cd app
   docker-compose up -d
   ```

Your API is now live at: **http://your-instance-ip:8000**

#### Google Cloud Run (Easiest Cloud Deployment)

```bash
# 1. Install Google Cloud SDK
# 2. Authenticate
gcloud auth login

# 3. Create a project
gcloud config set project PROJECT_ID

# 4. Build and push image
gcloud builds submit --tag gcr.io/PROJECT_ID/netflix-recommender

# 5. Deploy
gcloud run deploy netflix-recommender \
  --image gcr.io/PROJECT_ID/netflix-recommender \
  --platform managed \
  --region us-central1 \
  --memory 512Mi \
  --timeout 300
```

See `README.md` for more cloud options (Heroku, Azure, etc.)

---

## ✅ Verify Your Deployment

### Test with curl

```bash
# Test 1: Health check
curl http://localhost:8000/

# Test 2: Get recommendations
curl "http://localhost:8000/recommend/Avatar?num_recommendations=5"

# Test 3: Get all movies count
curl http://localhost:8000/movies | grep count
```

### Test with Python script (After deploying)

```bash
pip install requests
python test_api.py
```

---

## 📊 API Endpoints Reference

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/` | Health check |
| GET | `/movies` | List all movies |
| POST | `/recommend` | Get recommendations (body request) |
| GET | `/recommend/{title}` | Get recommendations (simple GET) |

### Example API Calls

**Get Recommendations:**
```json
POST /recommend
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
    "Titanic",
    "Inception",
    "The Day After Tomorrow",
    "Interstellar",
    "Avatar: The Way of Water"
  ],
  "status": "success"
}
```

---

## 🔧 Common Commands

### Docker Commands

```bash
# Start application
docker-compose up -d

# Stop application
docker-compose down

# View logs
docker-compose logs -f

# Rebuild without cache
docker-compose up --build --no-cache

# Remove everything
docker-compose down -v
```

### Python Commands (Without Docker)

```bash
# Install dependencies
pip install -r requirements.txt

# Run development server with auto-reload
uvicorn main:app --reload

# Run production server
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## 🐛 Troubleshooting

### Issue: Port 8000 already in use

**Solution:** Change port in `docker-compose.yml`
```yaml
ports:
  - "8080:8000"  # Use 8080 instead
```

### Issue: "Movie not found" error

**Solution:** Movie titles are case-sensitive
- Get exact titles: `curl http://localhost:8000/movies`
- Use exact match: `"The Dark Knight"` not `"the dark knight"`

### Issue: Docker not working

**Solution:**
1. Ensure Docker Desktop is running
2. Check Docker installation: `docker --version`
3. Check Docker Compose: `docker-compose --version`

### Issue: API takes too long to start

- Initial startup can take 30-60 seconds (loading pickle files)
- Check logs: `docker-compose logs -f`
- Wait for "Application startup complete" message

---

## 📈 Next Steps (After Deployment)

### 1. **Add Frontend**
Create a web UI with React/Vue to interact with the API

### 2. **Enhance Model**
- Add user ratings data
- Implement collaborative filtering
- Use embeddings instead of TF-IDF

### 3. **Scale Up**
- Add database (PostgreSQL/MongoDB for movies)
- Implement caching (Redis)
- Use Kubernetes for container orchestration

### 4. **Monitor & Logs**
- Setup application monitoring
- Configure error tracking (Sentry)
- Add request logging

### 5. **CI/CD Pipeline**
- Add automated testing
- Setup GitHub Actions/GitLab CI
- Automatic deployment on code push

---

## 📚 File Reference

| File | Purpose |
|------|---------|
| `main.py` | FastAPI application code |
| `requirements.txt` | Python dependencies |
| `Dockerfile` | Container image configuration |
| `docker-compose.yml` | Multi-container deployment config |
| `.dockerignore` | Files to exclude from Docker build |
| `README.md` | Comprehensive documentation |
| `test_api.py` | API test script |
| `netflix.ipynb` | Original Jupyter notebook (training) |

---

## 🎉 You're Ready!

Your recommendation system is now production-ready with:
- ✅ Modern FastAPI backend
- ✅ Docker containerization
- ✅ Comprehensive documentation
- ✅ Multiple deployment options
- ✅ Automated testing tools

**Start deploying:**
```bash
docker-compose up --build
```

**Access API:** http://localhost:8000/docs

**Questions?** Check `README.md` for complete documentation.

---

Happy deploying! 🚀
