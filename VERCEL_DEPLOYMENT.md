# Vercel Deployment Guide - Construction Defect Detection

## ⚠️ Important Limitation

**Vercel has significant limitations for this project:**

### Issues with Vercel Deployment:

1. **Model File Size**: Your `model.keras` (97 MB) exceeds Vercel's 50 MB limit
2. **TensorFlow Size**: TensorFlow package is too large for Vercel serverless functions
3. **Lambda Limits**: Vercel functions have 50 MB deployment size limit (uncompressed)
4. **Cold Start**: Serverless functions timeout (10s hobby, 60s pro) - TensorFlow loads slowly

### ❌ Vercel is NOT recommended for this project

---

## 🎯 Recommended Alternatives

### Best Option: Railway (All-in-One)

**Why Railway?**
- ✅ No file size limits
- ✅ Supports large ML models
- ✅ Persistent storage
- ✅ $5 free credit/month
- ✅ Easy deployment from GitHub

### Deploy to Railway:

1. **Sign up at https://railway.app**
   - Connect with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `apoorvtripathi1999/construction-defects`

3. **Configure API Service**
   - Railway auto-detects Python
   - Add these environment variables:
     ```
     PORT=8000
     TF_ENABLE_ONEDNN_OPTS=0
     ```
   - Set start command: `uvicorn api:app --host 0.0.0.0 --port $PORT`

4. **Add Streamlit Service** (Optional - separate service)
   - Click "New Service" → "GitHub Repo"
   - Same repository
   - Start command: `streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0`
   - Add environment variable:
     ```
     API_URL=https://your-api-url.railway.app
     ```

5. **Deploy**
   - Railway automatically deploys
   - Get your public URLs
   - Test the endpoints

**Cost**: Free tier with $5 credit (~500 hours/month)

---

## Alternative: Render + Streamlit Cloud

Already configured in `DEPLOYMENT.md` - this is the most reliable free option.

**Render (API):**
- Free tier available
- Better for ML models
- No strict size limits

**Streamlit Cloud (UI):**
- Free for public apps
- 1 GB RAM
- Perfect for Streamlit

---

## If You Still Want to Try Vercel (Not Recommended)

### Workaround for Vercel:

You would need to:

1. **Host model separately** (AWS S3, Google Cloud Storage, Hugging Face)
2. **Use lightweight inference** (ONNX Runtime instead of TensorFlow)
3. **Reduce model size** (quantization, pruning)
4. **Split deployment**: API elsewhere, UI on Vercel

### Steps (Complex):

1. **Export model to ONNX**
   ```python
   import tf2onnx
   import onnx
   
   # Convert Keras to ONNX
   model_proto, _ = tf2onnx.convert.from_keras(model)
   onnx.save(model_proto, "model.onnx")
   ```

2. **Host model on external storage**
   - Upload to AWS S3 / Google Cloud Storage
   - Update API to download model on startup

3. **Update requirements for Vercel**
   ```txt
   fastapi
   uvicorn
   pillow
   numpy
   onnxruntime  # Instead of tensorflow
   ```

4. **Deploy API to Vercel**
   ```bash
   vercel --prod
   ```

5. **Deploy UI to Vercel or Streamlit Cloud**

---

## 📊 Comparison Table

| Platform | API Support | Model Size | Free Tier | Recommendation |
|----------|-------------|------------|-----------|----------------|
| **Railway** | ✅ Excellent | ✅ No limits | $5 credit | ⭐⭐⭐⭐⭐ Best |
| **Render** | ✅ Good | ✅ No limits | Free with limits | ⭐⭐⭐⭐ Great |
| **Streamlit Cloud** | ❌ UI only | ✅ 1GB | Free | ⭐⭐⭐⭐ For UI |
| **Vercel** | ⚠️ Limited | ❌ 50MB limit | Free | ⭐ Not suitable |
| **Heroku** | ✅ Good | ✅ No limits | ❌ No free tier | ⭐⭐ Paid only |

---

## 🎯 Final Recommendation

**For your Construction Defect Detection app:**

### Option A: Railway (Simplest)
- Deploy both API and UI on Railway
- Single platform
- Easy management
- $5/month free credit

### Option B: Render + Streamlit Cloud (Most Reliable Free)
- API on Render (free)
- UI on Streamlit Cloud (free)
- Best for free hosting
- Slightly more setup

### Option C: Fly.io (Alternative)
- Similar to Railway
- Good free tier
- Supports Docker
- Deploy with: `flyctl launch`

---

## 🚀 Quick Start with Railway

1. Go to https://railway.app
2. Click "Start a New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository
5. Add environment variables
6. Deploy (takes ~5 minutes)
7. Done! Get your URL

**Railway is the best choice for your ML application with a large model.**

---

## Need Help?

Check the other deployment guides:
- `DEPLOYMENT.md` - Render + Streamlit Cloud guide
- Railway docs: https://docs.railway.app
- Contact support if issues arise

**Bottom line: Skip Vercel, use Railway or Render instead.**
