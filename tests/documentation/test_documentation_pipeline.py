"""
Integration tests for the documentation generation pipeline
"""

import os
import sys
import pytest
import tempfile

# Ensure project root is in Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

from documentation.generators.docstring_parser import DocStringParser
from documentation.generators.template_processor import TemplateProcessor
from documentation.generators.cross_reference_manager import CrossReferenceManager

def test_full_documentation_pipeline():
    """
    Test the complete documentation generation pipeline
    """
    try:
        # Create a temporary directory for testing
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a sample Python file
            sample_file_path = os.path.join(tmpdir, 'sample_module.py')
            with open(sample_file_path, 'w') as f:
                f.write('''
"""Module-level docstring for testing.

@author: Test Author
@version: 1.0.0
"""

def sample_function(x: int, y: int) -> int:
    """
    A sample function for testing documentation generation.

    Args:
        x: First integer parameter
        y: Second integer parameter

    Returns:
        Sum of x and y
    """
    return x + y
''')

            # Validate file creation
            assert os.path.exists(sample_file_path), "Sample file was not created"

            # Validate project configuration
            template_dir = os.path.join(project_root, 'docs', 'templates')
            assert os.path.exists(template_dir), f"Template directory not found: {template_dir}"

            # Parse docstrings
            parser = DocStringParser(sample_file_path)
            metadata = parser.extract_metadata()
            docstring = parser.parse_docstring(parser.module_ast)

            # Cross-reference analysis
            ref_manager = CrossReferenceManager(tmpdir)
            ref_manager.analyze_dependencies()
            references = ref_manager.generate_reference_links()

            # Prepare template data
            template_data = {
                'metadata': metadata,
                'docstring': docstring,
                'references': references
            }

            # Process template
            template_processor = TemplateProcessor(template_dir)
            markdown = template_processor.generate_markdown(template_data)

            # Assertions
            assert metadata is not None, "Metadata extraction failed"
            assert 'author' in metadata, "Missing author in metadata"
            assert docstring is not None, "Docstring parsing failed"
            assert 'description' in docstring, "Missing description in docstring"
            assert markdown is not None, "Markdown generation failed"
            assert len(markdown) > 0, "Generated markdown is empty"

    except Exception as e:
        pytest.fail(f"Documentation pipeline test failed: {e}")

def test_cross_references():
    """
    Test cross-reference generation and validation
    """
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create multiple sample modules
            module1_path = os.path.join(tmpdir, 'module1.py')
            module2_path = os.path.join(tmpdir, 'module2.py')

            with open(module1_path, 'w') as f:
                f.write('''
def function1():
    """Function in module1"""
    pass
''')
        
            with open(module2_path, 'w') as f:
                f.write('''
from module1 import function1

def function2():
    """Function in module2 that references module1"""
    function1()
''')

            # Analyze cross-references
            ref_manager = CrossReferenceManager(tmpdir)
            ref_manager.analyze_dependencies()
            references = ref_manager.generate_reference_links()

            # Validate cross-references
            assert 'module2' in references, "module2 not found in references"
            assert 'module1' in references['module2'], "module1 not referenced by module2"

    except Exception as e:
        pytest.fail(f"Cross-reference test failed: {e}")

def test_documentation_generation_robustness():
    """
    Test documentation generation with various input scenarios
    """
    scenarios = [
        # Empty docstring
        '''
def empty_function():
    pass
''',
        # Complex docstring with multiple sections
        '''
def complex_function(x: str, y: int) -> bool:
    """
    A complex function with detailed documentation.

    Args:
        x: A string parameter
        y: An integer parameter

    Returns:
        A boolean result

    Raises:
        ValueError: If input is invalid
    """
    return len(x) > y
'''
    ]

    for i, scenario in enumerate(scenarios):
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                test_file_path = os.path.join(tmpdir, f'test_scenario_{i}.py')
                with open(test_file_path, 'w') as f:
                    f.write(scenario)

                parser = DocStringParser(test_file_path)
                docstring = parser.parse_docstring(parser.module_ast)

                assert docstring is not None, f"Docstring parsing failed for scenario {i}"
                assert isinstance(docstring, dict), f"Invalid docstring type for scenario {i}"

        except Exception as e:
            pytest.fail(f"Robustness test failed for scenario {i}: {e}")
