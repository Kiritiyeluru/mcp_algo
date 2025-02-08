"""
File: documentation/generators/cross_reference_manager.py
Purpose: Manage cross-references and dependencies between documentation artifacts
Author: AI Assistant
Environment: Production
Dependencies: os, networkx, typing
"""

import os
import networkx as nx
from typing import Dict, List, Set
import ast
import importlib.util

class CrossReferenceManager:
    """Manage cross-references and dependencies between documentation artifacts."""
    
    def __init__(self, base_dir: str):
        """
        Initialize CrossReferenceManager.
        
        Args:
            base_dir: Base directory for documentation artifacts
        """
        self.base_dir = base_dir
        self.dependency_graph = nx.DiGraph()
        self.references: Dict[str, Set[str]] = {}
    
    def analyze_dependencies(self) -> None:
        """
        Analyze dependencies between Python modules in the project.
        """
        for root, _, files in os.walk(self.base_dir):
            for file in files:
                if file.endswith('.py'):
                    self._process_module_dependencies(os.path.join(root, file))
    
    def _process_module_dependencies(self, file_path: str) -> None:
        """
        Process dependencies for a single module.
        
        Args:
            file_path: Path to the Python module
        """
        with open(file_path, 'r') as f:
            module_ast = ast.parse(f.read())
        
        module_name = os.path.splitext(os.path.basename(file_path))[0]
        self.dependency_graph.add_node(module_name)
        
        for node in ast.walk(module_ast):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    self.dependency_graph.add_edge(module_name, alias.name)
            
            if isinstance(node, ast.ImportFrom):
                module = node.module or ''
                for alias in node.names:
                    full_import = f"{module}.{alias.name}" if module else alias.name
                    self.dependency_graph.add_edge(module_name, full_import)
    
    def generate_reference_links(self) -> Dict[str, List[str]]:
        """
        Generate cross-reference links between documentation artifacts.
        
        Returns:
            Dictionary of references for each artifact
        """
        references = {}
        for node in self.dependency_graph.nodes():
            references[node] = list(self.dependency_graph.neighbors(node))
        
        return references
    
    def export_dependency_graph(self, output_format: str = 'dot') -> str:
        """
        Export the dependency graph in specified format.
        
        Args:
            output_format: Format to export the graph (dot, json, etc.)
        
        Returns:
            Exported graph representation
        """
        if output_format == 'dot':
            return nx.drawing.nx_pydot.to_pydot(self.dependency_graph).to_string()
        elif output_format == 'json':
            return nx.json_graph.dumps(self.dependency_graph)
        else:
            raise ValueError(f"Unsupported output format: {output_format}")
