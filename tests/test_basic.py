"""
Basic tests for FridgeVision functionality.
Tests core components to ensure they work correctly.

Author: Your Name
Date: September 2024
"""

import pytest
import sys
from pathlib import Path
from PIL import Image
import numpy as np

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent / "src"))

def test_imports():
    """Test that all core modules can be imported."""
    try:
        from models.food_detector import FoodDetector
        from models.recipe_recommender import RecipeRecommender
        from utils.image_processing import preprocess_image, draw_detections
        from utils.config import load_config
        assert True, "All imports successful"
    except ImportError as e:
        pytest.fail(f"Import failed: {e}")

def test_config_loading():
    """Test configuration loading."""
    from utils.config import load_config
    
    config = load_config()
    assert isinstance(config, dict)
    assert 'CONFIDENCE_THRESHOLD' in config
    assert 'MODEL_PATH' in config

def test_image_preprocessing():
    """Test image preprocessing functionality."""
    from utils.image_processing import preprocess_image
    
    # Create a test image
    test_image = Image.new('RGB', (800, 600), color='red')
    
    # Preprocess image
    processed = preprocess_image(test_image, target_size=640)
    
    assert isinstance(processed, Image.Image)
    assert processed.size == (640, 640)

def test_recipe_recommender_init():
    """Test recipe recommender initialization."""
    from models.recipe_recommender import RecipeRecommender
    
    # Test without API key (should still work with fallback)
    recommender = RecipeRecommender()
    assert recommender is not None
    assert len(recommender.fallback_recipes) > 0

def test_recipe_fallback():
    """Test recipe fallback functionality."""
    from models.recipe_recommender import RecipeRecommender
    
    recommender = RecipeRecommender()
    
    # Test with common ingredients
    ingredients = ['chicken', 'tomato', 'onion']
    recipes = recommender._get_fallback_recipes(ingredients, 3)
    
    assert isinstance(recipes, list)
    assert len(recipes) <= 3
    
    for recipe in recipes:
        assert 'title' in recipe
        assert 'used_ingredients' in recipe

def test_food_detector_init():
    """Test food detector initialization (without actual model)."""
    from models.food_detector import FoodDetector
    
    # This will fail to load the specific model but should handle gracefully
    try:
        detector = FoodDetector("nonexistent_model.pt")
        # Should fallback to pretrained YOLO
        assert detector.model is not None
    except Exception as e:
        # Expected if YOLO dependencies aren't fully installed
        assert "Failed to load model" in str(e)

def test_image_processing_utilities():
    """Test image processing utility functions."""
    from utils.image_processing import calculate_iou, non_max_suppression
    
    # Test IoU calculation
    box1 = [0, 0, 10, 10]
    box2 = [5, 5, 15, 15]
    iou = calculate_iou(box1, box2)
    
    assert 0 <= iou <= 1
    assert iou > 0  # Should have some overlap
    
    # Test NMS
    detections = [
        {'bbox': [0, 0, 10, 10], 'confidence': 0.9, 'class': 'apple'},
        {'bbox': [5, 5, 15, 15], 'confidence': 0.8, 'class': 'apple'},
        {'bbox': [50, 50, 60, 60], 'confidence': 0.7, 'class': 'banana'}
    ]
    
    filtered = non_max_suppression(detections, iou_threshold=0.5)
    assert len(filtered) <= len(detections)

def test_class_mapping():
    """Test food class mapping."""
    from models.food_detector import FoodDetector
    
    # Test without loading actual model
    detector = FoodDetector.__new__(FoodDetector)
    detector.model = None  # Initialize model attribute
    detector.food_categories = {
        0: 'apple', 1: 'banana', 2: 'orange'
    }
    
    # Test class name retrieval
    assert detector.get_class_name(0) == 'apple'
    assert detector.get_class_name(1) == 'banana'
    assert 'unknown' in detector.get_class_name(999)  # Non-existent class

def test_directory_structure():
    """Test that required directories exist or can be created."""
    required_dirs = [
        'data', 'models', 'src', 'scripts', 'config', 'docs'
    ]
    
    for dir_name in required_dirs:
        dir_path = Path(dir_name)
        assert dir_path.exists(), f"Required directory {dir_name} not found"

def test_file_existence():
    """Test that required files exist."""
    required_files = [
        'requirements.txt',
        'README.md',
        'LICENSE',
        'src/app/main.py',
        'scripts/download_model.py',
        'scripts/train_model.py'
    ]
    
    for file_name in required_files:
        file_path = Path(file_name)
        assert file_path.exists(), f"Required file {file_name} not found"

if __name__ == "__main__":
    pytest.main([__file__])
