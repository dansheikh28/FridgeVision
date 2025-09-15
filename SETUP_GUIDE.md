# 🚀 FridgeVision Setup Guide

## ✅ Complete Setup Checklist

Follow these steps to get your FridgeVision app up and running:

### 1. 🔑 Get Your API Keys

#### Google Gemini API Key (Required)
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key (starts with `AIza...`)

#### Spoonacular API Key (Recommended)
1. Go to [Spoonacular API](https://spoonacular.com/food-api)
2. Sign up for a free account
3. Go to your dashboard and copy your API key
4. Free tier includes 150 requests/day (perfect for testing)

### 2. 📁 Setup Your Environment

```bash
# 1. Clone the repository (if you haven't already)
git clone https://github.com/yourusername/fridgevision.git
cd fridgevision

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt
```

### 3. 🔧 Configure API Keys

Create a `.env` file in the root directory:

```bash
# Copy the example file
copy env.example .env
```

Edit the `.env` file with your API keys:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
SPOONACULAR_API_KEY=your_actual_spoonacular_api_key_here
```

### 4. 🧪 Test Your Setup

```bash
# Run setup checks
python scripts/run_app.py --setup-only
```

You should see:
```
✅ All dependencies are installed
✅ Gemini API key found
✅ Spoonacular API key found
✅ Environment configured
✅ All checks passed!
```

### 5. 🚀 Launch the App

```bash
# Start the application
python scripts/run_app.py
```

The app will automatically open in your browser at `http://localhost:8501`

## 🎯 Quick Test

1. **Upload a test image**: Take a photo of your fridge or use any image with visible food items
2. **Adjust confidence**: Try different confidence thresholds (0.6 is recommended)
3. **Analyze**: Click "Analyze Fridge Contents" 
4. **View results**: You should see bounding boxes around detected food items
5. **Get recipes**: The app will automatically suggest recipes based on detected ingredients

## 🔧 Troubleshooting

### Common Issues

#### "GEMINI_API_KEY not found"
- Make sure your `.env` file is in the root directory
- Check that your API key is correctly formatted (no extra spaces)
- Verify your API key is active at [Google AI Studio](https://makersuite.google.com/app/apikey)

#### "Failed to load models"
- Check your internet connection
- Verify your Gemini API key has sufficient quota
- Try restarting the application

#### "No food items detected"
- Try uploading a clearer image
- Lower the confidence threshold (try 0.4-0.5)
- Ensure the image contains visible food items
- Check that lighting in the image is adequate

#### Import Errors
```bash
# Reinstall dependencies
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

### Performance Tips

1. **Image Quality**: Use well-lit, clear images for best results
2. **Image Size**: Images are automatically resized, but smaller files upload faster
3. **Confidence Threshold**: 
   - Higher (0.7-0.8): Fewer, more confident detections
   - Lower (0.4-0.6): More detections, some may be less accurate

## 📊 API Usage Limits

### Gemini API (Free Tier)
- 60 requests per minute
- 1,500 requests per day
- Rate limiting is handled automatically

### Spoonacular API (Free Tier)
- 150 requests per day
- App includes fallback recipes if quota exceeded

## 🎨 Customization Options

### Environment Variables
```env
# Optional customizations
CONFIDENCE_THRESHOLD=0.6          # Default detection confidence
MAX_RECIPES=10                    # Maximum recipes to show
DEFAULT_CUISINE=Any               # Default cuisine filter
DEFAULT_DIET=None                 # Default dietary restriction
MAX_COOKING_TIME=60               # Default max cooking time
```

### Streamlit Configuration
Create `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#16dbff"
backgroundColor = "#0e1117"
secondaryBackgroundColor = "#262730"
textColor = "#fafafa"
```

## 🚀 Next Steps

Once everything is working:

1. **Test with different images**: Try various fridge photos
2. **Explore filters**: Test different cuisine and diet options
3. **Share with friends**: Get feedback on recipe suggestions
4. **Customize**: Modify the code to add new features
5. **Deploy**: Consider deploying to Streamlit Cloud for public access

## 📞 Need Help?

If you encounter any issues:

1. Check the [README.md](README.md) for detailed documentation
2. Review error messages in the terminal
3. Verify your API keys are working
4. Try the troubleshooting steps above

Happy cooking! 🍳✨
