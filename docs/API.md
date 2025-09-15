# 📡 API Documentation

FridgeVision provides both a web interface and programmatic API for food detection and recipe recommendation.

## Core Components

### FoodDetector Class

The main class for food detection using YOLO models.

```python
from src.models.food_detector import FoodDetector

# Initialize detector
detector = FoodDetector(model_path="models/trained/food_yolo.pt")

# Predict on image
detections = detector.predict(image, confidence_threshold=0.5)
```

#### Methods

##### `__init__(model_path, device=None)`

Initialize the food detector.

**Parameters:**
- `model_path` (str): Path to trained YOLO model
- `device` (str, optional): Device for inference ('cpu', 'cuda', 'auto')

**Example:**
```python
detector = FoodDetector("models/trained/food_yolo.pt", device="cuda")
```

##### `predict(image, confidence_threshold=0.5, iou_threshold=0.45)`

Run food detection on an image.

**Parameters:**
- `image` (PIL.Image): Input image
- `confidence_threshold` (float): Minimum confidence for detections (0.0-1.0)
- `iou_threshold` (float): IoU threshold for NMS (0.0-1.0)

**Returns:**
- `List[Dict]`: List of detection dictionaries

**Detection Dictionary Format:**
```python
{
    'class': 'apple',          # Food class name
    'confidence': 0.85,        # Detection confidence (0.0-1.0)
    'bbox': [x1, y1, x2, y2],  # Bounding box coordinates
    'class_id': 0              # Numeric class identifier
}
```

**Example:**
```python
from PIL import Image

image = Image.open("fridge_photo.jpg")
detections = detector.predict(image, confidence_threshold=0.6)

for detection in detections:
    print(f"Found {detection['class']} with {detection['confidence']:.1%} confidence")
```

##### `get_model_info()`

Get information about the loaded model.

**Returns:**
- `Dict`: Model information

**Example:**
```python
info = detector.get_model_info()
print(f"Model has {info['total_parameters']} parameters")
```

### RecipeRecommender Class

Finds recipes based on detected ingredients.

```python
from src.models.recipe_recommender import RecipeRecommender

# Initialize recommender
recommender = RecipeRecommender(api_key="your_spoonacular_key")

# Get recipes
recipes = recommender.get_recipes(ingredients, cuisine="Italian")
```

#### Methods

##### `__init__(api_key=None)`

Initialize the recipe recommender.

**Parameters:**
- `api_key` (str, optional): Spoonacular API key

##### `get_recipes(ingredients, cuisine=None, diet=None, max_ready_time=None, number=10)`

Get recipe recommendations based on ingredients.

**Parameters:**
- `ingredients` (List[str]): List of available ingredients
- `cuisine` (str, optional): Preferred cuisine type
- `diet` (str, optional): Dietary restrictions
- `max_ready_time` (int, optional): Maximum cooking time in minutes
- `number` (int): Number of recipes to return

**Returns:**
- `List[Dict]`: List of recipe dictionaries

**Recipe Dictionary Format:**
```python
{
    'id': 12345,
    'title': 'Chicken Stir Fry',
    'image': 'https://example.com/image.jpg',
    'used_ingredients': 4,
    'missed_ingredients': 1,
    'readyInMinutes': 20,
    'servings': 2,
    'sourceUrl': 'https://example.com/recipe',
    'healthScore': 75,
    'usedIngredients': [{'name': 'chicken'}, {'name': 'bell pepper'}],
    'missedIngredients': [{'name': 'soy sauce'}]
}
```

**Example:**
```python
ingredients = ['chicken', 'bell_pepper', 'onion', 'garlic']
recipes = recommender.get_recipes(
    ingredients=ingredients,
    cuisine="Asian",
    max_ready_time=30,
    number=5
)

for recipe in recipes:
    print(f"{recipe['title']} - Uses {recipe['used_ingredients']} ingredients")
```

##### `search_recipes(query, number=10)`

Search for recipes by text query.

**Parameters:**
- `query` (str): Search query
- `number` (int): Number of results

**Returns:**
- `List[Dict]`: Recipe search results

**Example:**
```python
results = recommender.search_recipes("vegetarian pasta", number=5)
```

##### `get_recipe_nutrition(recipe_id)`

Get nutrition information for a recipe.

**Parameters:**
- `recipe_id` (int): Recipe ID

**Returns:**
- `Dict`: Nutrition information

## Image Processing Utilities

### preprocess_image()

Preprocess images for model inference.

```python
from src.utils.image_processing import preprocess_image

processed_image = preprocess_image(image, target_size=640)
```

### draw_detections()

Draw bounding boxes on images.

```python
from src.utils.image_processing import draw_detections

annotated_image = draw_detections(image, detections, confidence_threshold=0.3)
```

### non_max_suppression()

Apply Non-Maximum Suppression to filter overlapping detections.

```python
from src.utils.image_processing import non_max_suppression

filtered_detections = non_max_suppression(detections, iou_threshold=0.5)
```

## Configuration Management

### load_config()

Load application configuration.

```python
from src.utils.config import load_config

config = load_config("config/custom_config.yaml")
api_key = config.get('SPOONACULAR_API_KEY')
```

### ConfigManager

Manage application configuration.

```python
from src.utils.config import ConfigManager

config_manager = ConfigManager("config/app_config.yaml")
threshold = config_manager.get('CONFIDENCE_THRESHOLD', 0.5)
```

## Complete Usage Example

Here's a complete example showing how to use the API:

```python
#!/usr/bin/env python3
"""
Complete FridgeVision API usage example.
"""

from PIL import Image
from src.models.food_detector import FoodDetector
from src.models.recipe_recommender import RecipeRecommender
from src.utils.image_processing import draw_detections, preprocess_image
from src.utils.config import load_config

def analyze_fridge_photo(image_path: str):
    """Analyze a fridge photo and get recipe recommendations."""
    
    # Load configuration
    config = load_config()
    
    # Initialize models
    detector = FoodDetector(config.get('MODEL_PATH', 'models/trained/food_yolo.pt'))
    recommender = RecipeRecommender(config.get('SPOONACULAR_API_KEY'))
    
    # Load and preprocess image
    image = Image.open(image_path)
    processed_image = preprocess_image(image)
    
    # Detect food items
    print("🔍 Detecting food items...")
    detections = detector.predict(
        processed_image, 
        confidence_threshold=config.get('CONFIDENCE_THRESHOLD', 0.5)
    )
    
    # Print detected items
    detected_foods = []
    for detection in detections:
        food_name = detection['class']
        confidence = detection['confidence']
        detected_foods.append(food_name)
        print(f"  ✅ {food_name.title()}: {confidence:.1%}")
    
    if not detected_foods:
        print("❌ No food items detected")
        return
    
    # Get recipe recommendations
    print(f"\n🍳 Finding recipes for {len(detected_foods)} ingredients...")
    recipes = recommender.get_recipes(
        ingredients=detected_foods,
        cuisine="Any",
        max_ready_time=60,
        number=5
    )
    
    # Print recipes
    print(f"\n📋 Found {len(recipes)} recipe recommendations:")
    for i, recipe in enumerate(recipes, 1):
        print(f"\n{i}. {recipe['title']}")
        print(f"   ⏱️  Ready in: {recipe.get('readyInMinutes', 'N/A')} minutes")
        print(f"   👥 Servings: {recipe.get('servings', 'N/A')}")
        print(f"   ✅ Uses {recipe.get('used_ingredients', 0)} of your ingredients")
        if recipe.get('sourceUrl'):
            print(f"   🔗 Recipe: {recipe['sourceUrl']}")
    
    # Create annotated image
    annotated_image = draw_detections(image, detections)
    output_path = f"output_annotated_{Path(image_path).stem}.jpg"
    annotated_image.save(output_path)
    print(f"\n📸 Annotated image saved: {output_path}")

if __name__ == "__main__":
    # Example usage
    analyze_fridge_photo("data/sample_images/fridge_photo.jpg")
```

## Error Handling

All API methods include proper error handling. Common exceptions:

### Model Loading Errors
```python
try:
    detector = FoodDetector("invalid_path.pt")
except RuntimeError as e:
    print(f"Model loading failed: {e}")
```

### API Errors
```python
try:
    recipes = recommender.get_recipes(ingredients)
except requests.RequestException as e:
    print(f"API request failed: {e}")
```

### Image Processing Errors
```python
try:
    image = Image.open("invalid_image.jpg")
    detections = detector.predict(image)
except Exception as e:
    print(f"Image processing failed: {e}")
```

## Rate Limiting

The RecipeRecommender implements automatic rate limiting for API calls:

- Minimum 1 second between requests
- Automatic retry on rate limit errors
- Fallback to cached/offline recipes when API is unavailable

## Caching

Results are automatically cached to improve performance:

- Model predictions cache frequently used outputs
- Recipe API responses are cached for 1 hour
- Image preprocessing results are cached in memory

## Performance Tips

1. **Batch Processing**: Process multiple images together when possible
2. **Model Caching**: Keep the detector instance alive between calls
3. **Image Optimization**: Resize large images before processing
4. **API Efficiency**: Cache recipe results and use appropriate timeouts

## Extending the API

### Adding Custom Food Classes

```python
# Update food categories in FoodDetector
detector.food_categories[50] = 'new_food_item'
```

### Custom Recipe Sources

```python
# Extend RecipeRecommender for custom recipe APIs
class CustomRecipeRecommender(RecipeRecommender):
    def get_custom_recipes(self, ingredients):
        # Your custom implementation
        pass
```

### Custom Image Processing

```python
# Add custom preprocessing steps
def custom_preprocess(image):
    # Your custom preprocessing
    processed = preprocess_image(image)
    # Additional steps...
    return processed
```
