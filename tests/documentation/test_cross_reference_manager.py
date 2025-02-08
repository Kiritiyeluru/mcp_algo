"""
Test suite for CrossReferenceManager
"""

import os
import pytest
import networkx as nx

from documentation.generators.cross_reference_manager import CrossReferenceManager

def test_cross_reference_manager_initialization():
    """Test initialization of CrossReferenceManager."""
    base_dir = os.path.dirname(__file__)
    manager = CrossReferenceManager(base_dir)
    
    assert manager.base_dir == base_dir
    assert isinstance(manager.dependency_graph, nx.DiGraph)
    assert len(manager.dependency_graph.nodes()) == 0

def test_analyze_dependencies():
    """Test dependency analysis functionality."""
    # Create a test directory with sample Python files
    import tempfile
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create sample Python files
        with open(os.path.join(tmpdir, 'module1.py'), 'w') as f:
            f.write('import os\nimport sys\n\ndef func1():\n    pass')
        
        with open(os.path.join(tmpdir, 'module2.py'), 'w') as f:
            f.write('from module1 import func1\n\ndef func2():\n    func1()')
        
        # Analyze dependencies
        manager = CrossReferenceManager(tmpdir)
        manager.analyze_dependencies()
        
        # Check graph structure
        assert 'module1' in manager.dependency_graph.nodes()
        assert 'module2' in manager.dependency_graph.nodes()
        assert 'os' in manager.dependency_graph.nodes()
        assert 'sys' in manager.dependency_graph.nodes()
        
        # Check edges
        assert manager.dependency_graph.has_edge('module2', 'module1')
        assert manager.dependency_graph.has_edge('module1', 'os')
        assert manager.dependency_graph.has_edge('module1', 'sys')

def test_generate_reference_links():
    """Test reference link generation."""
    # Create a test directory with sample Python files
    import tempfile
    
    with tempfile.TemporaryDirectory() as tmpdir:
        with open(os.path.join(tmpdir, 'module1.py'), 'w') as f:
            f.write('import math\n\ndef func1():\n    pass')
        
        with open(os.path.join(tmpdir, 'module2.py'), 'w') as f:
            f.write('from module1 import func1\nimport os\n\ndef func2():\n    func1()')
        
        # Analyze dependencies
        manager = CrossReferenceManager(tmpdir)
        manager.analyze_dependencies()
        
        # Generate reference links
        references = manager.generate_reference_links()
        
        assert 'module1' in references
        assert 'module2' in references
        assert 'math' in references['module1']
        assert 'module1' in references['module2']
        assert 'os' in references['module2']

def test_export_dependency_graph():
    """Test dependency graph export."""
    import tempfile
    
    with tempfile.TemporaryDirectory() as tmpdir:
        with open(os.path.join(tmpdir, 'module1.py'), 'w') as f:
            f.write('import os\nimport sys\n\ndef func1():\n    pass')
        
        manager = CrossReferenceManager(tmpdir)
        manager.analyze_dependencies()
        
        # Test DOT export
        dot_graph = manager.export_dependency_graph('dot')
        assert isinstance(dot_graph, str)
        assert 'digraph' in dot_graph
        
        # Test JSON export
        json_graph = manager.export_dependency_graph('json')
        assert isinstance(json_graph, str)
        
        # Test invalid format
        with pytest.raises(ValueError):
            manager.export_dependency_graph('invalid_format')
