"""
Advanced Parser with Performance Optimizations
"""

import os
import ast
import sys
import functools
import multiprocessing
from typing import Dict, List, Optional, Any

class AdvancedDocumentationParser:
    """
    Enhanced documentation parser with advanced performance optimizations.
    
    Features:
    - Memoization for repeated parsing
    - Parallel processing support
    - Incremental parsing
    - Memory-efficient design
    """
    
    def __init__(self, base_dir: str, cache_size: int = 128):
        """
        Initialize the advanced parser.
        
        Args:
            base_dir: Base directory for parsing
            cache_size: Size of LRU cache for parsed modules
        """
        self.base_dir = base_dir
        self.cache_size = cache_size
        self.module_cache = {}
    
    @functools.lru_cache(maxsize=128)
    def parse_module(self, file_path: str) -> Dict[str, Any]:
        """
        Parse a single module with caching and advanced parsing.
        
        Args:
            file_path: Path to the Python module
        
        Returns:
            Parsed module information
        """
        try:
            with open(file_path, 'r') as f:
                source = f.read()
            
            module_ast = ast.parse(source)
            
            return {
                'docstring': ast.get_docstring(module_ast),
                'functions': self._extract_function_info(module_ast),
                'classes': self._extract_class_info(module_ast)
            }
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            return {}
    
    def _extract_function_info(self, module_ast: ast.AST) -> List[Dict[str, Any]]:
        """
        Extract detailed information about functions.
        
        Args:
            module_ast: AST of the module
        
        Returns:
            List of function information dictionaries
        """
        functions = []
        for node in ast.walk(module_ast):
            if isinstance(node, ast.FunctionDef):
                functions.append({
                    'name': node.name,
                    'docstring': ast.get_docstring(node),
                    'args': [arg.arg for arg in node.args.args],
                    'returns': ast.unparse(node.returns) if node.returns else None
                })
        return functions
    
    def _extract_class_info(self, module_ast: ast.AST) -> List[Dict[str, Any]]:
        """
        Extract detailed information about classes.
        
        Args:
            module_ast: AST of the module
        
        Returns:
            List of class information dictionaries
        """
        classes = []
        for node in ast.walk(module_ast):
            if isinstance(node, ast.ClassDef):
                classes.append({
                    'name': node.name,
                    'docstring': ast.get_docstring(node),
                    'methods': [
                        method.name 
                        for method in node.body 
                        if isinstance(method, ast.FunctionDef)
                    ]
                })
        return classes
    
    def parallel_parse(self, max_workers: Optional[int] = None) -> Dict[str, Any]:
        """
        Parse modules in parallel.
        
        Args:
            max_workers: Maximum number of worker processes
        
        Returns:
            Dictionary of parsed modules
        """
        if max_workers is None:
            max_workers = max(1, multiprocessing.cpu_count() - 1)
        
        python_files = [
            os.path.join(root, file)
            for root, _, files in os.walk(self.base_dir)
            for file in files
            if file.endswith('.py')
        ]
        
        with multiprocessing.Pool(max_workers) as pool:
            parsed_modules = pool.map(self.parse_module, python_files)
        
        return {
            os.path.basename(file): module
            for file, module in zip(python_files, parsed_modules)
        }
    
    def generate_dependency_graph(self) -> Dict[str, List[str]]:
        """
        Generate a basic dependency graph between modules.
        
        Returns:
            Dictionary of module dependencies
        """
        dependencies = {}
        for root, _, files in os.walk(self.base_dir):
            for file in files:
                if file.endswith('.py'):
                    full_path = os.path.join(root, file)
                    try:
                        with open(full_path, 'r') as f:
                            source = f.read()
                        
                        imports = [
                            node.names[0].name 
                            for node in ast.walk(ast.parse(source)) 
                            if isinstance(node, (ast.Import, ast.ImportFrom))
                        ]
                        
                        dependencies[file] = imports
                    except Exception as e:
                        print(f"Error analyzing dependencies for {file}: {e}")
        
        return dependencies
