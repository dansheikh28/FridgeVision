# 🤝 Contributing to FridgeVision

Thank you for considering contributing to FridgeVision! This document provides guidelines for contributing to the project.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Pull Request Process](#pull-request-process)
- [Issue Guidelines](#issue-guidelines)
- [Coding Standards](#coding-standards)
- [Testing](#testing)

## 📜 Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct:

- **Be respectful**: Treat everyone with respect and courtesy
- **Be inclusive**: Welcome contributors from all backgrounds
- **Be collaborative**: Work together to improve the project
- **Be constructive**: Provide helpful feedback and suggestions

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Basic knowledge of machine learning and computer vision
- Familiarity with PyTorch and Streamlit

### Development Setup

1. **Fork the repository**
   ```bash
   # Fork on GitHub, then clone your fork
   git clone https://github.com/YOUR_USERNAME/fridgevision.git
   cd fridgevision
   ```

2. **Set up development environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Install development dependencies
   pip install pytest black flake8 pre-commit
   ```

3. **Set up pre-commit hooks**
   ```bash
   pre-commit install
   ```

4. **Run setup script**
   ```bash
   python scripts/setup.py
   ```

## 🛠️ How to Contribute

### Types of Contributions

We welcome several types of contributions:

1. **🐛 Bug Reports**: Report bugs or issues
2. **✨ Feature Requests**: Suggest new features
3. **📝 Documentation**: Improve documentation
4. **🎨 UI/UX Improvements**: Enhance the user interface
5. **🧠 Model Improvements**: Improve detection accuracy
6. **⚡ Performance Optimizations**: Make the app faster
7. **🧪 Tests**: Add or improve test coverage

### Contribution Areas

#### 🤖 Machine Learning
- Improve food detection model accuracy
- Add new food categories
- Implement data augmentation techniques
- Optimize model performance

#### 🍽️ Recipe System
- Enhance recipe matching algorithms
- Add new recipe data sources
- Improve recipe filtering and ranking
- Add nutritional information

#### 💻 Web Application
- Improve user interface design
- Add new features to the Streamlit app
- Enhance user experience
- Mobile responsiveness

#### 📊 Data & Analytics
- Improve data collection pipeline
- Add analytics and metrics
- Create visualization dashboards
- Dataset curation and annotation

## 🔄 Pull Request Process

### Before You Start

1. **Check existing issues**: Look for existing issues or discussions
2. **Create an issue**: For new features, create an issue first to discuss
3. **Get assignment**: Wait for maintainer approval before starting work

### Development Workflow

1. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b bugfix/issue-number
   ```

2. **Make your changes**
   - Follow coding standards
   - Add tests for new functionality
   - Update documentation if needed

3. **Test your changes**
   ```bash
   # Run tests
   pytest tests/
   
   # Check code formatting
   black src/ scripts/
   
   # Check code quality
   flake8 src/ scripts/
   
   # Test the app
   streamlit run src/app/main.py
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add new food detection feature"
   ```

   Use conventional commit messages:
   - `feat:` for new features
   - `fix:` for bug fixes
   - `docs:` for documentation
   - `style:` for formatting changes
   - `refactor:` for code refactoring
   - `test:` for adding tests
   - `chore:` for maintenance tasks

5. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```
   
   Then create a Pull Request on GitHub.

### Pull Request Guidelines

Your PR should include:

- **Clear title**: Descriptive title explaining the change
- **Description**: Detailed description of what was changed and why
- **Testing**: Evidence that your changes work (screenshots, test results)
- **Documentation**: Updates to relevant documentation
- **Breaking changes**: Note any breaking changes

#### PR Template

```markdown
## Description
Brief description of changes.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Testing
- [ ] I have tested my changes locally
- [ ] I have added/updated tests
- [ ] All tests pass

## Screenshots (if applicable)
Add screenshots to help explain your changes.

## Checklist
- [ ] My code follows the project's coding standards
- [ ] I have performed a self-review of my code
- [ ] I have commented my code where necessary
- [ ] I have updated the documentation
- [ ] My changes generate no new warnings
```

## 📝 Issue Guidelines

### Bug Reports

When reporting bugs, please include:

```markdown
## Bug Description
Clear description of the bug.

## Steps to Reproduce
1. Step one
2. Step two
3. Step three

## Expected Behavior
What you expected to happen.

## Actual Behavior
What actually happened.

## Environment
- OS: [e.g., Windows 10, macOS 12, Ubuntu 20.04]
- Python version: [e.g., 3.9.16]
- Browser: [e.g., Chrome 115, Firefox 116]
- App version: [e.g., v1.0.0]

## Additional Context
Any other relevant information.

## Screenshots
If applicable, add screenshots.
```

### Feature Requests

For feature requests, please include:

```markdown
## Feature Description
Clear description of the proposed feature.

## Problem Statement
What problem does this feature solve?

## Proposed Solution
How should this feature work?

## Alternatives Considered
Other solutions you've considered.

## Additional Context
Any other relevant information.

## Mockups/Examples
If applicable, add mockups or examples.
```

## 🎯 Coding Standards

### Python Code Style

We follow PEP 8 with some modifications:

- **Line length**: 88 characters (Black default)
- **Imports**: Use isort for import sorting
- **Docstrings**: Use Google-style docstrings
- **Type hints**: Use type hints for function signatures

### Code Quality Tools

- **Black**: Code formatting
- **Flake8**: Code linting
- **isort**: Import sorting
- **mypy**: Type checking (optional)

### Example Code Structure

```python
"""
Module docstring describing the purpose.

Author: Your Name
Date: YYYY-MM-DD
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Optional

import numpy as np
import torch
from PIL import Image

# Local imports
from src.utils.config import load_config


class ExampleClass:
    """
    Example class demonstrating coding standards.
    
    This class shows proper documentation, type hints,
    and code organization.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the example class.
        
        Args:
            config_path (str, optional): Path to configuration file
        """
        self.config = load_config(config_path)
        self.model = None
    
    def process_image(self, image: Image.Image, threshold: float = 0.5) -> List[Dict]:
        """
        Process an image and return results.
        
        Args:
            image (PIL.Image): Input image to process
            threshold (float): Confidence threshold for filtering
            
        Returns:
            List[Dict]: List of detection results
            
        Raises:
            ValueError: If image is invalid
            RuntimeError: If model is not loaded
        """
        if self.model is None:
            raise RuntimeError("Model not loaded")
        
        # Implementation here
        results = []
        return results
```

### Documentation Standards

- **Docstrings**: All public functions and classes must have docstrings
- **Comments**: Use inline comments for complex logic
- **README**: Update README for new features
- **API docs**: Update API documentation for new endpoints

## 🧪 Testing

### Test Structure

```
tests/
├── __init__.py
├── conftest.py              # Pytest configuration
├── test_models/
│   ├── test_food_detector.py
│   └── test_recipe_recommender.py
├── test_utils/
│   ├── test_image_processing.py
│   └── test_config.py
└── test_app/
    └── test_main.py
```

### Writing Tests

```python
import pytest
from PIL import Image
from src.models.food_detector import FoodDetector


class TestFoodDetector:
    """Test cases for FoodDetector class."""
    
    @pytest.fixture
    def sample_image(self):
        """Create a sample image for testing."""
        return Image.new('RGB', (640, 480), color='red')
    
    @pytest.fixture
    def detector(self):
        """Create a detector instance for testing."""
        return FoodDetector("models/test_model.pt")
    
    def test_initialization(self, detector):
        """Test detector initialization."""
        assert detector.model is not None
        assert len(detector.food_categories) > 0
    
    def test_prediction(self, detector, sample_image):
        """Test food detection prediction."""
        detections = detector.predict(sample_image)
        assert isinstance(detections, list)
        
        for detection in detections:
            assert 'class' in detection
            assert 'confidence' in detection
            assert 'bbox' in detection
            assert 0.0 <= detection['confidence'] <= 1.0
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_models/test_food_detector.py

# Run with verbose output
pytest -v
```

## 🏷️ Versioning

We use [Semantic Versioning](https://semver.org/):

- **MAJOR.MINOR.PATCH** (e.g., 1.2.3)
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

## 📄 License

By contributing to FridgeVision, you agree that your contributions will be licensed under the MIT License.

## 🙋‍♀️ Getting Help

If you need help:

1. **Check documentation**: README, API docs, deployment guide
2. **Search issues**: Look for existing discussions
3. **Create an issue**: Ask questions or report problems
4. **Join discussions**: Participate in GitHub Discussions

## 🎉 Recognition

Contributors will be recognized:

- **Contributors list**: Added to README
- **Release notes**: Mentioned in release notes
- **GitHub insights**: Visible in contributor statistics

Thank you for contributing to FridgeVision! 🚀
