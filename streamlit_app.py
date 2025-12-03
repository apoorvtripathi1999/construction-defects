import streamlit as st
import requests
from PIL import Image
import io
import os

# API configuration - supports both local and production
API_BASE_URL = os.getenv("API_URL", "https://web-production-a1a27.up.railway.app")
API_URL = f"{API_BASE_URL}/predict"

# Page configuration
st.set_page_config(
    page_title="Construction Defect Detection",
    page_icon="🏗️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for dark mode styling
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stApp {
        background-color: #0e1117;
    }
    h1 {
        color: #ffffff;
        text-align: center;
        padding: 1rem 0;
    }
    .upload-text {
        color: #ffffff;
        font-size: 1.1rem;
        margin: 1rem 0;
    }
    .result-box {
        background-color: #1e2130;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 1px solid #2e3340;
    }
    .defect-yes {
        color: #ff4b4b;
        font-size: 1.5rem;
        font-weight: bold;
    }
    .defect-no {
        color: #00cc66;
        font-size: 1.5rem;
        font-weight: bold;
    }
    .confidence-text {
        color: #fafafa;
        font-size: 1.2rem;
        margin: 0.5rem 0;
    }
    .prediction-text {
        color: #ffffff;
        font-size: 1rem;
        margin: 0.3rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1>🏗️ Construction Defect Detection</h1>", unsafe_allow_html=True)

# Description
st.markdown("""
<div style='text-align: center; color: #a0a0a0; margin-bottom: 2rem;'>
Upload an image to detect construction defects using AI
</div>
""", unsafe_allow_html=True)

# About section (collapsible)
with st.expander("ℹ️ About This Project"):
    st.markdown("""
    ### The Problem
    
    Construction defect detection is a critical aspect of building maintenance and safety. Traditional manual 
    inspection methods are:
    
    - **Time-consuming** - Inspectors must physically examine every surface
    - **Costly** - Requires trained professionals and extensive labor hours
    - **Inconsistent** - Human error and fatigue can lead to missed defects
    - **Dangerous** - Inspecting hard-to-reach areas poses safety risks
    
    ### Our Solution
    
    This AI-powered system uses a Convolutional Neural Network (CNN) to automatically detect and classify 
    construction defects from images. The model can identify:
    
    - **Algae** - Fungi appearing as green, brown, or black patches
    - **Major Cracks** - Cracks with visible gaps
    - **Minor Cracks** - Cracks without visible gaps
    - **Peeling** - Loss of outer paint covering
    - **Spalling** - Surface breaks exposing inner material
    - **Stains** - Visible color marks (man-made or natural)
    - **Normal** - Clean surfaces with no defects
    
    ### Benefits
    
    ✅ **Faster inspections** - Analyze hundreds of images in minutes  
    ✅ **Cost reduction** - Automated analysis reduces labor costs  
    ✅ **Improved safety** - Reduce need for dangerous manual inspections  
    ✅ **Consistent accuracy** - AI provides objective, repeatable results  
    
    ### Dataset
    
    The model is trained on the **BD3 (Building Defects Detection Dataset)** containing over 3,900 images 
    across 7 defect categories, ensuring robust detection across various building surfaces and conditions.
    """)
    
    st.markdown("---")
    st.markdown("*Powered by TensorFlow and deployed as a FastAPI service*")

# Create tabs for single and bulk upload
tab1, tab2 = st.tabs(["📷 Single Image", "📁 Bulk Upload"])

# Tab 1: Single Image Upload
with tab1:
    st.markdown("<br>", unsafe_allow_html=True)
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose an image...",
        type=["jpg", "jpeg", "png"],
        key="single_upload"
    )

    if uploaded_file is not None:
        # Display the uploaded image
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_container_width=True)
        
        # Analyze button
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            analyze_button = st.button("🔍 Analyze Image", use_container_width=True, type="primary")
        
        if analyze_button:
            with st.spinner("Analyzing image..."):
                try:
                    # Prepare the file for API request
                    uploaded_file.seek(0)
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    
                    # Make API request
                    response = requests.post(API_URL, files=files, timeout=30)
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        if result.get("success", False):
                            # Display results
                            st.markdown("<div class='result-box'>", unsafe_allow_html=True)
                            
                            # Defect status
                            has_defect = result.get("has_defect", False)
                            prediction_text = result.get("prediction", "Unknown")
                            confidence = result.get("confidence", 0) * 100
                            
                            if has_defect:
                                st.markdown(
                                    "<div class='defect-yes'>⚠️ Defect Detected</div>",
                                    unsafe_allow_html=True
                                )
                            else:
                                st.markdown(
                                    "<div class='defect-no'>✓ No Defect Detected</div>",
                                    unsafe_allow_html=True
                                )
                            
                            # Prediction details
                            st.markdown(
                                f"<div class='confidence-text'>Result: {prediction_text}</div>",
                                unsafe_allow_html=True
                            )
                            st.markdown(
                                f"<div class='confidence-text'>Confidence: {confidence:.2f}%</div>",
                                unsafe_allow_html=True
                            )
                            
                            # Visual confidence indicator
                            st.markdown("<br>", unsafe_allow_html=True)
                            st.progress(confidence/100, text=f"Model Confidence: {confidence:.2f}%")
                            
                            st.markdown("</div>", unsafe_allow_html=True)
                        else:
                            st.error(f"❌ Prediction failed: {result.get('error', 'Unknown error')}")
                        
                    else:
                        st.error(f"❌ API Error: {response.status_code} - {response.text}")
                        
                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot connect to API. Please ensure the API server is running at http://localhost:8000")
                    st.info("💡 Start the API with: `uvicorn api:app --reload`")
                except requests.exceptions.Timeout:
                    st.error("❌ Request timed out. Please try again.")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

# Tab 2: Bulk Upload
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("Upload multiple images for batch processing")
    
    # Multiple file uploader
    uploaded_files = st.file_uploader(
        "Choose images...",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True,
        key="bulk_upload"
    )
    
    if uploaded_files:
        st.write(f"**{len(uploaded_files)} image(s) selected**")
        
        # Show thumbnails
        cols = st.columns(min(len(uploaded_files), 5))
        for idx, file in enumerate(uploaded_files[:5]):
            with cols[idx]:
                img = Image.open(file)
                st.image(img, caption=file.name, use_container_width=True)
        
        if len(uploaded_files) > 5:
            st.caption(f"+ {len(uploaded_files) - 5} more images")
        
        # Analyze button
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            bulk_analyze_button = st.button("🔍 Analyze All Images", use_container_width=True, type="primary", key="bulk_analyze")
        
        if bulk_analyze_button:
            with st.spinner(f"Analyzing {len(uploaded_files)} images..."):
                try:
                    # Prepare files for bulk API request
                    files = []
                    for file in uploaded_files:
                        file.seek(0)
                        files.append(("files", (file.name, file.getvalue(), file.type)))
                    
                    # Make bulk API request
                    bulk_url = f"{API_BASE_URL}/predict/bulk"
                    response = requests.post(bulk_url, files=files, timeout=60)
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        if result.get("success", False):
                            st.success(f"✅ Successfully analyzed {result.get('total_images', 0)} images")
                            
                            # Display results in a table
                            results_data = result.get("results", [])
                            
                            if results_data:
                                st.markdown("<div class='result-box'>", unsafe_allow_html=True)
                                st.markdown("### Analysis Results")
                                
                                # Create a formatted table
                                for idx, item in enumerate(results_data, 1):
                                    image_name = item.get("image_name", "Unknown")
                                    prediction = item.get("prediction", "Unknown")
                                    
                                    # Color code based on prediction
                                    if "Defect Detected" in prediction:
                                        icon = "⚠️"
                                        color = "#ff4b4b"
                                    elif "No Defect" in prediction:
                                        icon = "✓"
                                        color = "#00cc66"
                                    else:
                                        icon = "❓"
                                        color = "#ffa500"
                                    
                                    st.markdown(
                                        f"<div style='padding: 0.5rem; margin: 0.3rem 0; background-color: #1e2130; border-left: 3px solid {color};'>"
                                        f"<span style='color: {color};'>{icon}</span> "
                                        f"<strong>{image_name}</strong>: {prediction}"
                                        f"</div>",
                                        unsafe_allow_html=True
                                    )
                                
                                st.markdown("</div>", unsafe_allow_html=True)
                                
                                # Summary statistics
                                defect_count = sum(1 for item in results_data if "Defect Detected" in item.get("prediction", ""))
                                no_defect_count = sum(1 for item in results_data if "No Defect" in item.get("prediction", ""))
                                
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.metric("Total Images", len(results_data))
                                with col2:
                                    st.metric("Defects Found", defect_count)
                                with col3:
                                    st.metric("No Defects", no_defect_count)
                        else:
                            st.error(f"❌ Bulk prediction failed: {result.get('error', 'Unknown error')}")
                    else:
                        st.error(f"❌ API Error: {response.status_code} - {response.text}")
                        
                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot connect to API. Please ensure the API server is running at http://localhost:8000")
                    st.info("💡 Start the API with: `uvicorn api:app --reload`")
                except requests.exceptions.Timeout:
                    st.error("❌ Request timed out. Please try again with fewer images.")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; color: #606060; font-size: 0.9rem;'>
    <p>Supported formats: JPG, JPEG, PNG</p>
    <p>Make sure the API is running on port 8000</p>
</div>
""", unsafe_allow_html=True)
