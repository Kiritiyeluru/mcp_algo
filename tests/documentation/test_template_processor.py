"""
File: tests/documentation/test_template_processor.py
Purpose: Test suite for TemplateProcessor functionality
Author: AI Assistant
Environment: Testing
Dependencies: pytest, jinja2, markdown
"""

import pytest
from pathlib import Path
from documentation.generators.template_processor import TemplateProcessor

@pytest.fixture
def template_dir(tmp_path):
    """Create temporary template directory with test templates."""
    template_dir = tmp_path / "templates"
    template_dir.mkdir()
    
    # Create test template
    test_template = template_dir / "test_template.md"
    test_template.write_text("""# {{title}}

{{description}}

## Methods
{% for method in methods %}
### {{method.name}}
{{method.description}}
{% endfor %}
""")
    
    return template_dir

@pytest.fixture
def processor(template_dir):
    """Create TemplateProcessor instance with test template directory."""
    return TemplateProcessor(str(template_dir), default_template='test_template.md')

def test_load_template(processor):
    """Test loading template file."""
    template = processor.load_template('test_template.md')
    assert template is not None
    
    with pytest.raises(FileNotFoundError):
        processor.load_template('nonexistent.md')

def test_process_template(processor):
    """Test template processing with data."""
    data = {
        'title': 'Test Class',
        'description': 'Test description',
        'methods': [
            {'name': 'test_method', 'description': 'Method description'}
        ]
    }
    
    result = processor.process_template(data)
    assert 'Test Class' in result
    assert 'Test description' in result
    assert 'test_method' in result
    assert 'Method description' in result

def test_generate_markdown(processor):
    """Test Markdown generation."""
    data = {
        'title': 'Test',
        'description': 'Description',
        'methods': []
    }
    
    markdown = processor.generate_markdown(data)
    assert '# Test' in markdown
    assert 'Description' in markdown

def test_generate_html(processor):
    """Test HTML generation from Markdown."""
    data = {
        'title': 'Test',
        'description': 'Description',
        'methods': []
    }
    
    html = processor.generate_html(data)
    assert '<h1>Test</h1>' in html
    assert 'Description' in html

def test_validate_template_data(processor):
    """Test template data validation."""
    data = {
        'title': 'Test',
        'description': 'Description'
    }
    
    # Methods is missing but required by template
    missing = processor.validate_template_data(data)
    assert 'methods' in missing
    
    # Add missing field
    data['methods'] = []
    missing = processor.validate_template_data(data)
    assert len(missing) == 0