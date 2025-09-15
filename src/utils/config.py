"""
Production Configuration Management for FridgeVision
Handles environment variables, API keys, and application settings.

Author: FridgeVision Team
Date: September 2024
"""

import os
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_config() -> Dict[str, Any]:
    """
    Load production configuration from environment variables.
    
    Returns:
        Dict[str, Any]: Configuration dictionary
    """
    # Load environment variables
    load_dotenv()
    
    config = {
        # API Keys (Required)
        'GEMINI_API_KEY': os.getenv('GEMINI_API_KEY'),
        'SPOONACULAR_API_KEY': os.getenv('SPOONACULAR_API_KEY'),
        
        # Detection settings
        'CONFIDENCE_THRESHOLD': float(os.getenv('CONFIDENCE_THRESHOLD', '0.6')),
        'MAX_RECIPES': int(os.getenv('MAX_RECIPES', '10')),
        'DEFAULT_CUISINE': os.getenv('DEFAULT_CUISINE', 'Any'),
        'DEFAULT_DIET': os.getenv('DEFAULT_DIET', 'None'),
        'MAX_COOKING_TIME': int(os.getenv('MAX_COOKING_TIME', '60')),
        
        # Application settings
        'DEBUG': os.getenv('DEBUG', 'False').lower() == 'true',
        'LOG_LEVEL': os.getenv('LOG_LEVEL', 'INFO'),
        'MAX_IMAGE_SIZE': int(os.getenv('MAX_IMAGE_SIZE', '20971520')),  # 20MB (Gemini limit)
        'CACHE_DIR': os.getenv('CACHE_DIR', 'data/cache'),
        'SUPPORTED_FORMATS': ['jpg', 'jpeg', 'png', 'webp', 'heic'],
        
        # Streamlit settings
        'STREAMLIT_PORT': int(os.getenv('STREAMLIT_PORT', '8501')),
        'STREAMLIT_HOST': os.getenv('STREAMLIT_HOST', '0.0.0.0'),  # Production ready
        
        # Security settings
        'RATE_LIMIT_REQUESTS': int(os.getenv('RATE_LIMIT_REQUESTS', '100')),
        'RATE_LIMIT_WINDOW': int(os.getenv('RATE_LIMIT_WINDOW', '3600')),  # 1 hour
    }
    
    # Validate required API keys
    if not config.get('GEMINI_API_KEY'):
        raise ValueError("GEMINI_API_KEY is required but not found in environment variables")
    
    if not config.get('SPOONACULAR_API_KEY'):
        logger.warning("SPOONACULAR_API_KEY not found - using fallback recipes only")
    
    return config

def get_cache_dir() -> Path:
    """Get the cache directory path, creating it if necessary."""
    cache_dir = Path(os.getenv('CACHE_DIR', 'data/cache'))
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir

def setup_logging(level: str = None) -> None:
    """
    Set up production logging configuration.
    
    Args:
        level (str): Logging level (DEBUG, INFO, WARNING, ERROR)
    """
    if level is None:
        level = os.getenv('LOG_LEVEL', 'INFO')
    
    # Create logs directory
    logs_dir = Path('logs')
    logs_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(logs_dir / 'app.log'),
            logging.FileHandler(logs_dir / 'error.log', level=logging.ERROR)
        ]
    )

def validate_environment() -> bool:
    """
    Validate that all required environment variables are set.
    
    Returns:
        bool: True if environment is valid
    """
    try:
        config = load_config()
        logger.info("✅ Environment validation passed")
        return True
    except Exception as e:
        logger.error(f"❌ Environment validation failed: {str(e)}")
        return False

def validate_image_file(file_path: Path, max_size: int = None) -> bool:
    """
    Validate uploaded image file.
    
    Args:
        file_path (Path): Path to image file
        max_size (int): Maximum file size in bytes
        
    Returns:
        bool: True if file is valid
    """
    config = load_config()
    
    if max_size is None:
        max_size = config['MAX_IMAGE_SIZE']
    
    # Check file exists
    if not file_path.exists():
        logger.error(f"File does not exist: {file_path}")
        return False
    
    # Check file size
    if file_path.stat().st_size > max_size:
        logger.error(f"File too large: {file_path.stat().st_size} bytes (max: {max_size})")
        return False
    
    # Check file extension
    extension = file_path.suffix.lower().lstrip('.')
    if extension not in config['SUPPORTED_FORMATS']:
        logger.error(f"Unsupported format: {extension}")
        return False
    
    return True

class ConfigManager:
    """Production configuration manager."""
    
    def __init__(self):
        """Initialize configuration manager."""
        self.config = load_config()
        self._setup_directories()
    
    def _setup_directories(self) -> None:
        """Create necessary directories."""
        directories = [
            self.config['CACHE_DIR'],
            'logs',
            'data/cache/recipes'
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self.config.get(key, default)
    
    def is_debug(self) -> bool:
        """Check if debug mode is enabled."""
        return self.config.get('DEBUG', False)
    
    def get_api_key(self, service: str) -> Optional[str]:
        """Get API key for a service."""
        key_name = f"{service.upper()}_API_KEY"
        return self.config.get(key_name)

# Global config instance
config_manager = ConfigManager()