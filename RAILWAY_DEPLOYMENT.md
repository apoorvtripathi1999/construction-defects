# Railway Deployment Guide - Construction Defect Detection

## 🚂 Deploy to Railway (Recommended)

Railway is the best platform for deploying this ML application with a large model file.

### Why Railway?
- ✅ No file size limits (97 MB model.keras is fine)
- ✅ Supports TensorFlow and large Python packages
- ✅ $5 free credit per month (~500 execution hours)
- ✅ Automatic deployment from GitHub
- ✅ Persistent storage
- ✅ Easy environment variable management

---

## 🚀 Quick Deployment Steps

### 1. Sign Up for Railway

1. Go to https://railway.app
2. Click "Login" → "Login with GitHub"
3. Authorize Railway to access your GitHub account

### 2. Create New Project

1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose repository: `apoorvtripathi1999/construction-defects`
4. Railway will automatically detect it's a Python project

### 3. Configure API Service

Railway auto-configures most settings, but you should add:

**Environment Variables:**
```
PORT=8000
TF_ENABLE_ONEDNN_OPTS=0
```

**Start Command** (Railway usually detects this automatically):
```
uvicorn api:app --host 0.0.0.0 --port $PORT
```

### 4. Deploy!

- Railway automatically builds and deploys
- Wait ~5-10 minutes for first deployment (TensorFlow is large)
- You'll get a URL like: `https://construction-defects-api-production.up.railway.app`

### 5. Deploy Streamlit UI (Optional - Separate Service)

If you want to deploy the Streamlit UI on Railway too:

1. In the same project, click "New Service"
2. Select "GitHub Repo" → Choose the same repository
3. **Environment Variables:**
   ```
   PORT=8501
   API_URL=https://your-api-url.up.railway.app
   ```
4. **Start Command:**
   ```
   streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0
   ```

---

## 🔧 Configuration Files

Railway uses these files from your repo:

- ✅ `requirements.txt` - Python dependencies (already configured)
- ✅ `.env.production` - Environment variables template

No special config files needed - Railway is smart!

---

## 📊 Monitoring & Logs

**View Logs:**
1. Go to Railway dashboard
2. Click on your service
3. Go to "Deployments" tab
4. Click "View Logs"

**Check Status:**
- Green = Running
- Red = Error (check logs)
- Yellow = Building

---

## 💰 Free Tier Details

**Railway Free Plan:**
- $5 credit per month
- ~500 execution hours for hobby projects
- 512 MB RAM (upgradable)
- 1 GB disk space
- Shared CPU

**Estimated Usage:**
- API: ~$3-4/month if running 24/7
- Sleeps after inactivity (optional setting)

---

## 🌐 Get Your URLs

After deployment:

**API Endpoints:**
- Base: `https://your-project.up.railway.app`
- Health: `https://your-project.up.railway.app/health`
- Docs: `https://your-project.up.railway.app/docs`
- Predict: `https://your-project.up.railway.app/predict`

**Update Streamlit App:**
If deploying UI separately, update the API_URL environment variable with your Railway API URL.

---

## 🐛 Troubleshooting

### Deployment Failed
- Check logs in Railway dashboard
- Verify `requirements.txt` has all dependencies
- Ensure Python version compatibility (3.11)

### Model Not Loading
- Check if `model.keras` is in the repository
- Verify file size (<100 MB for Railway free tier)
- Check logs for TensorFlow errors

### Out of Memory
- Upgrade to paid plan ($5/month for 2 GB RAM)
- Or optimize model size

### API Not Responding
- Check if service is running (Railway dashboard)
- Verify PORT environment variable is set
- Check health endpoint: `/health`

---

## 🔄 Continuous Deployment

Railway automatically redeploys when you push to GitHub:

```bash
git add .
git commit -m "Update model or code"
git push origin master
```

Railway detects the push and redeploys automatically!

---

## 🎯 Alternative: Deploy UI to Streamlit Cloud

Instead of deploying UI on Railway, use Streamlit Cloud (free):

1. Go to https://share.streamlit.io
2. Sign in with GitHub
3. New app → Select your repository
4. Main file: `streamlit_app.py`
5. Add secret in settings:
   ```
   API_URL = "https://your-railway-api.up.railway.app"
   ```
6. Deploy

**This combination (Railway API + Streamlit Cloud UI) is completely free!**

---

## ✅ Deployment Checklist

- [ ] Sign up for Railway account
- [ ] Create new project from GitHub
- [ ] Add environment variables (PORT, TF_ENABLE_ONEDNN_OPTS)
- [ ] Wait for deployment to complete
- [ ] Test health endpoint: `/health`
- [ ] Test prediction endpoint: `/predict`
- [ ] (Optional) Deploy Streamlit UI
- [ ] Update API URL in Streamlit app if needed
- [ ] Share your deployed app!

---

## 📞 Support

- Railway Docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- GitHub Issues: Open an issue in your repository

---

## 🎉 You're Done!

Your Construction Defect Detection app is now live on Railway!

**Next Steps:**
1. Test the API with sample images
2. Share the URL with others
3. Monitor usage in Railway dashboard
4. Update README with deployment URL

**Deployment URL structure:**
- API: `https://construction-defects-api-production.up.railway.app`
- UI: `https://construction-defects-ui-production.up.railway.app`

Enjoy your deployed ML application! 🚂🎉
