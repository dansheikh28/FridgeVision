"""
Application runner script.
Provides a convenient way to run the FridgeVision Streamlit app.

Author: Your Name
Date: September 2024
"""

import sys
import subprocess
import logging
from pathlib import Path
import webbrowser
import time

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import streamlit
        import google.generativeai
        import cv2
        import PIL
        import requests
        logger.info("✅ All dependencies are installed")
        return True
    except ImportError as e:
        logger.error(f"❌ Missing dependency: {e}")
        logger.info("Run: pip install -r requirements.txt")
        return False

def check_api_keys():
    """Check if required API keys are configured."""
    import os
    from dotenv import load_dotenv
    
    # Load environment variables
    load_dotenv()
    
    gemini_key = os.getenv('GEMINI_API_KEY')
    spoonacular_key = os.getenv('SPOONACULAR_API_KEY')
    
    if not gemini_key:
        logger.error("❌ GEMINI_API_KEY not found in environment variables")
        logger.info("Please set your Gemini API key in a .env file or environment variables")
        return False
    
    if not spoonacular_key:
        logger.warning("⚠️ SPOONACULAR_API_KEY not found - app will use fallback recipes only")
    else:
        logger.info("✅ Spoonacular API key found")
    
    logger.info("✅ Gemini API key found")
    return True

def setup_environment():
    """Set up environment variables."""
    import os
    
    # Set default values if not already set
    defaults = {
        'STREAMLIT_SERVER_PORT': '8501',
        'STREAMLIT_SERVER_ADDRESS': 'localhost',
        'CONFIDENCE_THRESHOLD': '0.6',
        'MAX_RECIPES': '10',
        'DEFAULT_CUISINE': 'Any',
        'DEFAULT_DIET': 'None',
        'MAX_COOKING_TIME': '60'
    }
    
    for key, value in defaults.items():
        if key not in os.environ:
            os.environ[key] = value
    
    logger.info("✅ Environment configured")

def run_streamlit_app(port=8501, host='localhost', open_browser=True):
    """
    Run the Streamlit application.
    
    Args:
        port (int): Port to run the app on
        host (str): Host address
        open_browser (bool): Whether to open browser automatically
    """
    try:
        # Construct the streamlit command
        cmd = [
            sys.executable, "-m", "streamlit", "run",
            "src/app/main.py",
            f"--server.port={port}",
            f"--server.address={host}",
            "--server.headless=false"
        ]
        
        logger.info(f"🚀 Starting FridgeVision on http://{host}:{port}")
        
        # Open browser if requested
        if open_browser:
            def open_browser_delayed():
                time.sleep(3)  # Wait for server to start
                webbrowser.open(f"http://{host}:{port}")
            
            import threading
            browser_thread = threading.Thread(target=open_browser_delayed)
            browser_thread.daemon = True
            browser_thread.start()
        
        # Run the app
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        logger.info("\n👋 Shutting down FridgeVision...")
    except Exception as e:
        logger.error(f"❌ Failed to start app: {e}")
        return False
    
    return True

def main():
    """Main application runner."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Run FridgeVision application")
    parser.add_argument(
        "--port", "-p", 
        type=int, 
        default=8501, 
        help="Port to run the app on (default: 8501)"
    )
    parser.add_argument(
        "--host", "-H", 
        type=str, 
        default="localhost", 
        help="Host address (default: localhost)"
    )
    parser.add_argument(
        "--no-browser", 
        action="store_true", 
        help="Don't open browser automatically"
    )
    parser.add_argument(
        "--setup-only", 
        action="store_true", 
        help="Only run setup checks, don't start app"
    )
    
    args = parser.parse_args()
    
    logger.info("🍽️ FridgeVision - AI-Powered Recipe Generator")
    logger.info("=" * 50)
    
    # Run setup checks
    logger.info("🔍 Running setup checks...")
    
    if not check_dependencies():
        logger.error("❌ Dependency check failed")
        return 1
    
    if not check_api_keys():
        logger.error("❌ API key check failed")
        return 1
    
    setup_environment()
    
    logger.info("✅ All checks passed!")
    
    if args.setup_only:
        logger.info("🎉 Setup complete! Run without --setup-only to start the app.")
        return 0
    
    # Start the application
    logger.info("\n🚀 Starting application...")
    
    success = run_streamlit_app(
        port=args.port,
        host=args.host,
        open_browser=not args.no_browser
    )
    
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())
