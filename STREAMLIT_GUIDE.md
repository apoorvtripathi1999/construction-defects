# Running the Construction Defect Detection UI

## Quick Start

### 1. Install Dependencies (if not already installed)
```powershell
python -m pip install -r requirements.txt
```

### 2. Start the API Server
Open a terminal and run:
```powershell
uvicorn api:app --reload
```
The API will run on: http://localhost:8000

### 3. Start the Streamlit UI
Open a **second terminal** and run:
```powershell
streamlit run streamlit_app.py
```
The UI will open automatically in your browser at: http://localhost:8501

## Usage

1. The Streamlit UI will open with a dark mode interface
2. Click "Browse files" or drag and drop an image
3. Click "🔍 Analyze Image" button
4. View the results showing:
   - Whether defect is detected or not
   - Predicted defect type
   - Confidence score
   - All class probabilities

## Troubleshooting

**If you see "Cannot connect to API":**
- Make sure the API server is running in a separate terminal
- Check that it's running on port 8000
- Verify with: http://localhost:8000 in your browser

**If streamlit command not found:**
```powershell
python -m streamlit run streamlit_app.py
```

## Notes

- The UI expects your trained model to be loaded in the API
- Supported image formats: JPG, JPEG, PNG
- The dark mode is configured in `.streamlit/config.toml`
