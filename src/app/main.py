"""
FridgeVision: AI-Powered Recipe Generator
Main Streamlit application for food detection and recipe recommendation.

Author: Your Name
Date: September 2024
"""

import streamlit as st
import os
import sys
from pathlib import Path
import numpy as np
from PIL import Image
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from models.gemini_food_detector import GeminiFoodDetector
from models.recipe_recommender import RecipeRecommender
from utils.config import load_config
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="FridgeVision - AI Recipe Generator",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1e88e5;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #424242;
        text-align: center;
        margin-bottom: 2rem;
    }
    .detection-card {
        background-color: #f5f5f5;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #1e88e5;
        color: #000000;
    }
    .detection-card h4 {
        color: #000000 !important;
    }
    .recipe-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
    }
    .confidence-bar {
        background-color: #e0e0e0;
        border-radius: 10px;
        overflow: hidden;
        height: 20px;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_models():
    """Load and cache the AI models."""
    try:
        # Check for required API keys
        gemini_key = os.getenv('GEMINI_API_KEY')
        spoonacular_key = os.getenv('SPOONACULAR_API_KEY')
        
        if not gemini_key:
            st.error("❌ GEMINI_API_KEY not found in environment variables")
            return None, None, False
            
        if not spoonacular_key:
            st.warning("⚠️ SPOONACULAR_API_KEY not found - using fallback recipes only")
        
        detector = GeminiFoodDetector(api_key=gemini_key)
        recommender = RecipeRecommender(api_key=spoonacular_key)
        return detector, recommender, True
    except Exception as e:
        st.error(f"Error loading models: {str(e)}")
        return None, None, False

def display_detection_results(detections, image, detector):
    """Display food detection results with confidence scores."""
    if not detections:
        st.warning("No food items detected in the image. Try uploading a clearer image of your fridge contents.")
        return []
    
    st.subheader("🔍 Detected Food Items")
    
    # Create columns for better layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Display image with bounding boxes using Gemini detector's drawing method
        annotated_image = detector.draw_detections(image, detections)
        st.image(annotated_image, caption="Detected Food Items", use_column_width=True)
    
    with col2:
        # Display detection list with confidence scores
        detected_items = []
        for detection in detections:
            item_name = detection['class']
            confidence = detection['confidence']
            detected_items.append(item_name)
            
            # Create detection card
            st.markdown(f"""
            <div class="detection-card">
                <h4>{item_name.title()}</h4>
                <div class="confidence-bar">
                    <div style="background-color: #4caf50; width: {confidence*100}%; height: 100%; 
                                border-radius: 10px; display: flex; align-items: center; 
                                justify-content: center; color: white; font-weight: bold;">
                        {confidence:.1%}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    return detected_items

def display_recipes(recipes):
    """Display recommended recipes in an attractive format."""
    if not recipes:
        st.warning("No recipes found with the detected ingredients. Try adding more items to your fridge!")
        return
    
    st.subheader("🍳 Recommended Recipes")
    
    for i, recipe in enumerate(recipes[:6]):  # Limit to top 6 recipes
        used_count = recipe.get('usedIngredientCount', recipe.get('used_ingredients', 0))
        with st.expander(f"{recipe['title']} (Uses {used_count} ingredients)", expanded=i==0):
            col1, col2 = st.columns([1, 2])
            
            with col1:
                if recipe.get('image'):
                    st.image(recipe['image'], width='stretch')
                
                # Recipe stats
                st.markdown("**Recipe Stats:**")
                st.write(f"⏱️ Ready in: {recipe.get('readyInMinutes', 'N/A')} minutes")
                st.write(f"👥 Servings: {recipe.get('servings', 'N/A')}")
                st.write(f"❤️ Health Score: {recipe.get('healthScore', 'N/A')}/100")
            
            with col2:
                # Ingredients breakdown
                st.markdown("**Ingredients you have:**")
                for ingredient in recipe.get('usedIngredients', []):
                    st.write(f"✅ {ingredient['name']}")
                
                if recipe.get('missedIngredients'):
                    st.markdown("**Ingredients you need:**")
                    for ingredient in recipe.get('missedIngredients', []):
                        st.write(f"🛒 {ingredient['name']}")
                
                # Link to full recipe
                if recipe.get('sourceUrl'):
                    st.markdown(f"[🔗 View Full Recipe]({recipe['sourceUrl']})")

def main():
    """Main application function."""
    # Header
    st.markdown('<h1 class="main-header">🍽️ FridgeVision</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">AI-Powered Recipe Generator from Your Fridge Contents</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("🔧 Settings")
        
        # Model confidence threshold - optimized for Gemini Vision API
        confidence_threshold = st.slider(
            "Detection Confidence Threshold", 
            min_value=0.3,
            max_value=0.9,
            value=0.6,  # Optimized for Gemini Vision API
            step=0.05,
            help="Gemini Vision API confidence threshold (recommended: 0.6-0.8)"
        )
        
        # Recipe preferences
        st.subheader("🍽️ Recipe Preferences")
        cuisine_type = st.selectbox(
            "Cuisine Type",
            ["Any", "Italian", "Mexican", "Asian", "American", "Mediterranean", "Indian"]
        )
        
        diet_type = st.selectbox(
            "Dietary Restrictions",
            ["None", "Vegetarian", "Vegan", "Gluten Free", "Keto", "Paleo"]
        )
        
        max_time = st.slider(
            "Maximum Cooking Time (minutes)",
            min_value=15,
            max_value=120,
            value=60,
            step=15
        )
    
    # Load models
    detector, recommender, models_loaded = load_models()
    
    if not models_loaded:
        st.error("❌ Failed to load models. Please check your installation and model files.")
        st.stop()
    
    # File upload
    st.header("📸 Upload Your Fridge Photo")
    uploaded_file = st.file_uploader(
        "Choose an image file",
        type=['jpg', 'jpeg', 'png', 'bmp'],
        help="Upload a clear photo of the inside of your refrigerator"
    )
    
    # Demo images option
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🖼️ Use Demo Image"):
            # You can add demo images here
            st.info("Demo images feature coming soon!")
    
    with col2:
        if st.button("📋 View Supported Items"):
            st.info("The model can detect 50+ food categories including fruits, vegetables, dairy, meat, and beverages.")
    
    if uploaded_file is not None:
        # Display uploaded image
        image = Image.open(uploaded_file)
        
        # Show original image
        st.subheader("📷 Uploaded Image")
        st.image(image, caption="Your Fridge Photo", width='stretch')
        
        # Process image button
        if st.button("🔍 Analyze Fridge Contents", type="primary"):
            with st.spinner("🤖 Analyzing your fridge contents with Gemini Vision AI..."):
                try:
                    # Run detection using Gemini Vision API
                    detections = detector.predict(image, confidence_threshold=confidence_threshold)
                    
                    # Display results
                    detected_items = display_detection_results(detections, image, detector)
                    
                    if detected_items:
                        # Get recipe recommendations
                        with st.spinner("🍳 Finding recipes for you..."):
                            recipe_params = {
                                'cuisine': cuisine_type if cuisine_type != "Any" else None,
                                'diet': diet_type if diet_type != "None" else None,
                                'max_ready_time': max_time
                            }
                            recipes = recommender.get_recipes(detected_items, **recipe_params)
                            display_recipes(recipes)
                        
                        # Analytics
                        st.subheader("📊 Analysis Summary")
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric("Items Detected", len(detected_items))
                        
                        with col2:
                            st.metric("Recipes Found", len(recipes) if recipes else 0)
                        
                        with col3:
                            avg_confidence = np.mean([d['confidence'] for d in detections])
                            st.metric("Avg. Confidence", f"{avg_confidence:.1%}")
                
                except Exception as e:
                    error_msg = str(e)
                    if "quota" in error_msg.lower() or "429" in error_msg:
                        st.error("🚫 **Gemini API Quota Exceeded**")
                        st.info("""
                        **What happened?** You've reached your daily/hourly limit for the Gemini API.
                        
                        **Solutions:**
                        1. **Wait and retry** - Quotas reset hourly/daily
                        2. **Use Gemini 1.5 Flash** - Has higher quotas (already implemented)
                        3. **Get a paid plan** - For unlimited usage
                        4. **Try again later** - Free tier resets at midnight PST
                        
                        The app will automatically use fallback detection when quotas are exceeded.
                        """)
                    else:
                        st.error(f"❌ Error processing image: {error_msg}")
                        st.info("Please check your API keys and try again. Make sure your image contains visible food items.")

if __name__ == "__main__":
    main()
