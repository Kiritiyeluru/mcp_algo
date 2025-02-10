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
import time
from memory_mcp import MemoryMCP
from github_mcp import GitHubMCP

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
        self.memory_mcp = MemoryMCP()
        self.github_mcp = GitHubMCP()
        self.validate_connections()
    
    def validate_connections(self) -> None:
        """Validate MCP connections and retry if needed."""
        max_retries = 3
        retry_delay = 1  # seconds

        for attempt in range(max_retries):
            try:
                if not self.memory_mcp.test_connection():
                    raise ConnectionError("Memory MCP connection failed")
                if not self.github_mcp.test_connection():
                    raise ConnectionError("GitHub MCP connection failed")
                return
            except ConnectionError:
                if attempt == max_retries - 1:
                    raise
                time.sleep(retry_delay)
    
    def analyze_dependencies(self) -> None:
        """
        Analyze dependencies between Python modules in the project.
        """
        try:
            for root, _, files in os.walk(self.base_dir):
                for file in files:
                    if file.endswith('.py'):
                        self._process_module_dependencies(os.path.join(root, file))
            
            # Store dependency graph in memory MCP for persistence
            self.memory_mcp.store_dependencies(self.dependency_graph)
            
        except Exception as e:
            # Log error and store in GitHub issues
            self.github_mcp.create_issue(
                title="Dependency Analysis Error",
                body=f"Error analyzing dependencies: {str(e)}"
            )
            raise
    
    def _process_module_dependencies(self, file_path: str) -> None:
        """
        Process dependencies for a single module.
        
        Args:
            file_path: Path to the Python module
        """
        try:
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
                        
        except Exception as e:
            # Store error context in memory MCP
            self.memory_mcp.store_error_context({
                'file': file_path,
                'error': str(e),
                'type': 'dependency_analysis'
            })
            raise
    
    def generate_reference_links(self) -> Dict[str, List[str]]:
        """
        Generate cross-reference links between documentation artifacts.
        
        Returns:
            Dictionary of references for each artifact
        """
        try:
            # Try to load from memory MCP first
            cached_refs = self.memory_mcp.get_reference_links()
            if cached_refs:
                return cached_refs
            
            references = {}
            for node in self.dependency_graph.nodes():
                references[node] = list(self.dependency_graph.neighbors(node))
            
            # Cache results
            self.memory_mcp.store_reference_links(references)
            return references
            
        except Exception as e:
            self.github_mcp.create_issue(
                title="Reference Generation Error",
                body=f"Error generating references: {str(e)}"
            )
            raise
    
    def export_dependency_graph(self, output_format: str = 'dot') -> str:
        """
        Export the dependency graph in specified format.
        
        Args:
            output_format: Format to export the graph (dot, json, etc.)
        
        Returns:
            Exported graph representation
        """
        try:
            if output_format == 'dot':
                return nx.drawing.nx_pydot.to_pydot(self.dependency_graph).to_string()
            elif output_format == 'json':
                return nx.json_graph.dumps(self.dependency_graph)
            else:
                raise ValueError(f"Unsupported output format: {output_format}")
                
        except Exception as e:
            self.memory_mcp.store_error_context({
                'error': str(e),
                'type': 'graph_export',
                'format': output_format
            })
            raise
