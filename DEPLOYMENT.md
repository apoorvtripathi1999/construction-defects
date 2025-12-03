# Deployment Guide - Construction Defect Detection

## Free Deployment Options

This guide covers deploying your Construction Defect Detection application using **free** hosting platforms:

### Option 1: Render (API) + Streamlit Cloud (UI) [RECOMMENDED]

---

## 🚀 Deploy API to Render (Free Tier)

### Prerequisites
- GitHub account
- Render account (sign up at https://render.com)

### Step 1: Prepare Your Repository
Your repository already has the required files:
- ✅ `render.yaml` - Render configuration
- ✅ `requirements.txt` - Python dependencies
- ✅ `Procfile` - Process configuration
- ✅ `runtime.txt` - Python version

### Step 2: Deploy API on Render

1. **Go to Render Dashboard**
   - Visit https://render.com
   - Sign in with GitHub

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository: `apoorvtripathi1999/construction-defects`
   - Select the repository

3. **Configure Service**
   - **Name**: `construction-defects-api`
   - **Region**: Choose closest to you (e.g., Oregon for US)
   - **Branch**: `master`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn api:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free

4. **Environment Variables**
   Add these environment variables:
   ```
   TF_ENABLE_ONEDNN_OPTS=0
   PYTHON_VERSION=3.11.0
   ```

5. **Deploy**
   - Click "Create Web Service"
   - Wait 5-10 minutes for deployment (TensorFlow is large)
   - Your API URL will be: `https://construction-defects-api.onrender.com`

6. **Verify Deployment**
   - Visit: `https://construction-defects-api.onrender.com/health`
   - You should see: `{"status":"healthy","model_loaded":true}`

---

## 🎨 Deploy Streamlit UI to Streamlit Cloud (Free)

### Step 1: Update API URL in Streamlit App

Before deploying, you need to update the API URL in `streamlit_app.py`:

1. Open `streamlit_app.py`
2. Find this line (around line 8):
   ```python
   API_URL = "http://localhost:8000/predict"
   ```
3. Change it to your Render API URL:
   ```python
   API_URL = "https://construction-defects-api.onrender.com/predict"
   ```
4. Commit and push changes:
   ```bash
   git add streamlit_app.py
   git commit -m "Update API URL for production deployment"
   git push origin master
   ```

### Step 2: Deploy to Streamlit Cloud

1. **Go to Streamlit Cloud**
   - Visit https://share.streamlit.io
   - Sign in with GitHub

2. **Create New App**
   - Click "New app"
   - **Repository**: `apoorvtripathi1999/construction-defects`
   - **Branch**: `master`
   - **Main file path**: `streamlit_app.py`
   - Click "Deploy"

3. **Your App URL**
   - Will be: `https://construction-defects.streamlit.app`
   - Or similar based on availability

4. **Verify**
   - Open the URL
   - Upload a test image
   - Should connect to your Render API

---

## 🐳 Alternative: Deploy Both on Render (Free)

If you prefer to deploy both on Render:

1. **Deploy API** (as described above)

2. **Deploy Streamlit UI**
   - Create another Web Service on Render
   - **Name**: `construction-defects-ui`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0`
   - **Environment Variables**:
     ```
     API_URL=https://construction-defects-api.onrender.com
     ```

---

## 📦 Alternative: Railway (API + UI)

Railway offers generous free tier:

1. **Sign up at https://railway.app**

2. **Deploy from GitHub**
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway auto-detects Python and deploys

3. **Configure**
   - Add environment variables
   - Set start command: `uvicorn api:app --host 0.0.0.0 --port $PORT`

---

## ⚠️ Important Notes

### Model File Size
Your `model.keras` file (97 MB) may cause issues:
- **Render Free**: 512 MB RAM limit - should work but may be slow on cold starts
- **Streamlit Cloud**: Has storage limits
- **Railway**: More generous limits

**Solution if deployment fails:**
Consider using model compression or hosting the model separately (e.g., AWS S3, Google Cloud Storage).

### Free Tier Limitations

**Render Free:**
- ✅ Unlimited apps
- ⚠️ Sleeps after 15 min inactivity (30s cold start)
- ⚠️ 512 MB RAM
- ⚠️ Shared CPU

**Streamlit Cloud Free:**
- ✅ Unlimited public apps
- ✅ 1 GB RAM
- ⚠️ Sleeps after inactivity

**Railway Free:**
- ✅ $5 free credit/month
- ✅ 512 MB RAM
- ⚠️ Limited to credit usage

---

## 🔧 Troubleshooting

### API doesn't load model
- Check logs on Render dashboard
- Verify `model.keras` is in repository
- May need to increase memory (paid plan)

### Streamlit can't connect to API
- Verify API URL is correct
- Check API is running: visit `/health` endpoint
- Ensure CORS is enabled in API (already configured)

### Cold starts are slow
- Free tiers sleep after inactivity
- First request takes 30-60 seconds
- Consider using a paid tier or keep-alive service

---

## ✅ Quick Deployment Checklist

- [ ] Push all changes to GitHub
- [ ] Sign up for Render account
- [ ] Deploy API to Render
- [ ] Get API URL from Render
- [ ] Update `API_URL` in `streamlit_app.py`
- [ ] Push updated code to GitHub
- [ ] Sign up for Streamlit Cloud
- [ ] Deploy Streamlit app
- [ ] Test the deployed application

---

## 📞 Support

If deployment fails:
1. Check deployment logs on the platform
2. Verify all dependencies in `requirements.txt`
3. Ensure Python version compatibility (3.11)
4. Check model file size and memory requirements

---

## 🎉 After Deployment

Once deployed, share your app:
- API Docs: `https://your-api-url.onrender.com/docs`
- Streamlit UI: `https://your-app.streamlit.app`

Update your README.md with the live URLs!
