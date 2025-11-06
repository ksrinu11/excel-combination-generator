# Deployment Guide for Excel Combination Generator

## 🚀 Quick Deploy Options

### 1. Railway (Recommended - Free Tier Available)

**One-Click Deploy:**
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/cFLo4c?referralCode=bonus)

**Manual Deploy:**
1. Go to [Railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select `ksrinu11/excel-combination-generator`
5. Railway will automatically detect and deploy!

### 2. Render (Free Tier Available)

1. Go to [Render.com](https://render.com)
2. Sign up with GitHub
3. Click "New +" → "Web Service"
4. Connect your GitHub repo: `ksrinu11/excel-combination-generator`
5. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Environment:** Python 3

### 3. Heroku

```bash
# Install Heroku CLI first
heroku create excel-combo-generator
git push heroku main
heroku open
```

### 4. Google Cloud Run

```bash
# Install Google Cloud SDK first
gcloud run deploy excel-combo-generator \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### 5. Docker Deployment (Any Platform)

```bash
# Build image
docker build -t excel-combo-generator .

# Run locally
docker run -p 8000:8000 excel-combo-generator

# Deploy to any Docker-compatible platform
```

### 6. Vercel (Serverless)

1. Go to [Vercel.com](https://vercel.com)
2. Import your GitHub repository
3. Vercel will auto-detect and deploy

## 🔧 Environment Variables

For production deployments, you might need:

```bash
PORT=8080                    # Port for the application
PYTHONPATH=/app             # Python path (usually automatic)
```

## 📊 Deployment Status

After deployment, your app will be available at:
- **Railway:** `https://your-app-name.railway.app`
- **Render:** `https://your-app-name.onrender.com`
- **Heroku:** `https://your-app-name.herokuapp.com`
- **Vercel:** `https://your-app-name.vercel.app`

## 🎯 Features Available in Production

- ✅ Excel file upload (up to 10MB)
- ✅ Column combination generation
- ✅ File download
- ✅ Responsive web interface
- ✅ Error handling and validation

## 🛠️ Troubleshooting

**Common Issues:**
1. **Port binding:** Make sure app uses `$PORT` environment variable
2. **File uploads:** Some platforms limit file upload size
3. **Memory:** Large Excel files may need more RAM

**Solutions:**
- Check platform-specific logs
- Increase memory allocation if available
- Use smaller test files initially

## 📈 Scaling

For high-traffic usage:
- Use Redis for session storage
- Implement file cleanup jobs
- Add database for file metadata
- Set up CDN for static assets

---

Choose the platform that best fits your needs. Railway and Render are great for beginners with free tiers!