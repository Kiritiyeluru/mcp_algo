"""
File: tests/documentation/test_docstring_parser.py
Purpose: Test suite for DocStringParser functionality
Author: AI Assistant
Environment: Testing
Dependencies: pytest, ast
"""

import pytest
import ast
from documentation.generators.docstring_parser import DocStringParser

@pytest.fixture
def sample_source():
    return '''"""
    @module: test_module
    @version: 1.0
    @author: Test Author
    """
    
    def sample_function(arg1: int, arg2: str) -> bool:
        """Sample function for testing.
        
        Args:
            arg1: First argument
            arg2: Second argument
            
        Returns:
            Boolean result
            
        Raises:
            ValueError: If arguments invalid
            
        Examples:
            >>> sample_function(1, "test")
            True
        """
        return True
    '''

@pytest.fixture
def parser(tmp_path):
    source_file = tmp_path / "test_source.py"
    source_file.write_text(sample_source())
    return DocStringParser(str(source_file))

def test_extract_metadata(parser):
    """Test metadata extraction from module docstring."""
    metadata = parser.extract_metadata()
    assert metadata['module'] == 'test_module'
    assert metadata['version'] == '1.0'
    assert metadata['author'] == 'Test Author'

def test_parse_docstring(parser):
    """Test docstring parsing from function."""
    for node in ast.walk(parser.module_ast):
        if isinstance(node, ast.FunctionDef):
            docstring = parser.parse_docstring(node)
            assert 'Sample function for testing' in docstring['description']
            assert 'First argument' in docstring['args']
            assert 'Boolean result' in docstring['returns']
            assert 'ValueError' in docstring['raises']
            assert 'sample_function(1, "test")' in docstring['examples']

def test_get_type_hints(parser):
    """Test extraction of type hints."""
    for node in ast.walk(parser.module_ast):
        if isinstance(node, ast.FunctionDef):
            type_hints = parser.get_type_hints(node)
            assert type_hints['arg1'] == 'int'
            assert type_hints['arg2'] == 'str'
            assert type_hints['return'] == 'bool'