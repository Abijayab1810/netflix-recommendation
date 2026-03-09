# 🚀 Cloud Deployment Guide

Your app is ready for cloud deployment! Here are **3 easy options** (easiest first):

---

## Option 1: Railway.app (⭐ EASIEST - Recommended)

### Why Railway?
- ✅ Free tier (runs forever)
- ✅ Automatic Docker deployment
- ✅ Takes 5 minutes
- ✅ GitHub integration
- ✅ Public URL for anyone to access

### Steps:

**1. Create GitHub Repository**

```bash
# In your project folder
git init
git add .
git commit -m "Initial commit"
```

Then create a new repo on GitHub.com and push:
```bash
git remote add origin https://github.com/YOUR_USERNAME/netflix-recommendation.git
git branch -M main
git push -u origin main
```

**2. Sign Up on Railway**
- Go to https://railway.app
- Click "Start for Free"
- Sign up with GitHub

**3. Deploy on Railway**
- Click "New Project"
- Select "Deploy from GitHub"
- Choose your `netflix-recommendation` repo
- Railway auto-detects Dockerfile ✅
- Wait 3-5 minutes for build
- Get public URL like: `https://netflix-recommendation-prod.up.railway.app`

**4. Share the Link!**
```
Anyone can now visit:
https://netflix-recommendation-prod.up.railway.app
```

---

## Option 2: Render.com (Also Easy)

### Why Render?
- ✅ Free tier
- ✅ Auto-deploys from GitHub
- ✅ Simple dashboard

### Steps:

**1. Create GitHub Repo** (same as Railway)

**2. Go to https://render.com**
- Sign up with GitHub
- Click "New +"
- Select "Web Service"
- Connect your repo
- Name: `netflix-recommendation`
- Runtime: Docker
- Free plan selected
- Click "Create Web Service"

**3. Wait for deployment** (2-5 minutes)

**4. Get LIVE URL** from Render dashboard

---

## Option 3: Heroku (Classic, Free Tier Ended)

Heroku discontinued free tier, but you can still use it:
- $5-7/month minimum
- Easiest UI
- Best for production

```bash
# Install Heroku CLI
# heroku login
# heroku create netflix-recommendation
# git push heroku main
```

---

## 🌐 How to Access After Deployment

Once deployed, you'll get a URL like:

```
https://netflix-recommendation-prod.up.railway.app
```

**Anyone worldwide can visit this URL and:**
- 🎥 Search for movies
- ⭐ Get recommendations  
- No local setup needed!

---

## 📊 Understanding the Deployment Flow

### Local (What we had):
```
Your Computer (localhost:8000)
    ↓
    Only you can access
    ↓
    Stops when you close it
```

### Cloud with Docker (What we're doing):
```
Your Computer
    ↓
    Docker packages everything
    ↓
    Push to GitHub
    ↓
    Railway sees Dockerfile
    ↓
    Railway builds Docker image
    ↓
    Railway runs container 24/7
    ↓
    https://your-app.railway.app ✅
    ↓
    ANYONE worldwide can access!
```

---

## 🔑 Key Components We're Using

### Dockerfile
```dockerfile
FROM python:3.11-slim
# Lists all dependencies and how to build
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY main.py .
COPY movies.pkl .
# etc.
```

**Why?** Docker reads this and creates a container with everything needed.

### requirements.txt
```
fastapi==0.104.1
uvicorn==0.24.0
pandas==2.1.3
sklearn==1.3.2
```

**Why?** Docker installs exactly these versions.

### Procfile
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

**Why?** Tells Railway/Heroku how to start the app.

---

## 💡 Important: Environment Variables

If you add sensitive data (API keys, passwords), create `.env`:

```
# .env (never commit this!)
API_KEY=your_secret_key
DATABASE_URL=postgres://...
```

Then in code:
```python
import os
api_key = os.getenv("API_KEY")
```

And add to `.gitignore`:
```
.env
```

---

## 📝 Checklist for Deployment

### Before Deploying:
- ✅ Dockerfile configured
- ✅ requirements.txt has all packages
- ✅ Code works locally (http://localhost:8000)
- ✅ app.html exists in same folder as main.py
- ✅ movies.pkl exists
- ✅ similarity.pkl exists

### GitHub Setup:
- ✅ Create GitHub account (free)
- ✅ Create new repository
- ✅ Push code to GitHub
- ✅ Repository is public (so Railway can access)

### Railway Setup:
- ✅ Sign up on Railway.app
- ✅ Connect GitHub account
- ✅ Select your repository
- ✅ Railway auto-deploys
- ✅ Get public URL ✨

---

## 🎯 What Happens After You Deploy

**Railway:**
1. Sees your Dockerfile
2. Builds Docker image from it
3. Starts a container
4. Exposes port to internet
5. Gives you a public URL
6. Auto-updates when you push to GitHub
7. Runs 24/7 ✅

**Your Users:**
1. Visit https://your-app.railway.app
2. See your interactive UI
3. Search movies
4. Get recommendations
5. No setup needed!

---

## 🚨 Troubleshooting Deployment

### "Build failed"
- Check that all files are in repo
- Make sure movies.pkl and similarity.pkl are committed
- Check Dockerfile paths are correct

### "Port doesn't match"
- Railway sets PORT env variable
- Our app listens on 0.0.0.0:$PORT ✅
- Should work!

### "Movies not loading"
- Ensure movies.pkl exists in repo
- Check file paths in main.py
- Logs in Railway dashboard show errors

### "App crashes after 60s"
- Usually means port issue
- Make sure PORT is read from environment
- Check Procfile format

---

## 📚 Next Steps

1. **Push to GitHub** (if not done)
   ```bash
   git init
   git add .
   git commit -m "Add Netflix recommendation app"
   git push origin main
   ```

2. **Go to Railway.app**
   ```
   https://railway.app
   → New Project
   → Deploy from GitHub
   → Select repo
   → Wait 5 mins
   → ✅ Live!
   ```

3. **Share URL with anyone!**
   ```
   https://your-app.railway.app
   ```

---

## 💰 Costs

| Service | Free Tier | Notes |
|---------|-----------|-------|
| Railway | $5/month credit | Enough for small projects |
| Render | Free | Limited to 750 hours/month |
| Heroku | Ended | Was free, now $5+/month |
| AWS | Free 1 year | Complex setup |
| Google Cloud | Free tier | Complex setup |

---

## 🎉 You're Ready to Deploy!

Your app has:
- ✅ Dockerfile (packaging)
- ✅ requirements.txt (dependencies)
- ✅ main.py (backend)
- ✅ app.html (frontend)
- ✅ Procfile (startup)
- ✅ Everything needed!

**Next:** Push to GitHub → Deploy to Railway → Share with the world! 🌍

---

Questions? Each platform has great docs:
- **Railway:** https://docs.railway.app
- **Render:** https://render.com/docs
- **Heroku:** https://devcenter.heroku.com
