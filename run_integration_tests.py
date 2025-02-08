import os
import sys
import pytest

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Configure detailed test output
pytest_args = [
    'tests/documentation/test_documentation_pipeline.py', 
    '-v',  # Verbose output
    '-s',  # Show print statements
    '--tb=short'  # Shorter traceback format
]

# Run tests
result = pytest.main(pytest_args)

# Exit with the same code as pytest
sys.exit(result)
