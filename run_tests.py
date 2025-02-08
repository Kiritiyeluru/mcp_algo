import pytest
import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Run tests in the documentation directory
pytest.main(['tests/documentation/test_cross_reference_manager.py', '-v'])
