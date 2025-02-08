"""
File: documentation/generators/docstring_parser.py
Purpose: Parse and process Python docstrings for documentation generation
Author: AI Assistant
Environment: Production
Dependencies: ast, inspect
"""

import ast
import inspect
from typing import Dict, List, Optional

class DocStringParser:
    """Parse and extract information from Python docstrings.
    
    This class handles parsing of docstrings using AST and inspect modules,
    extracting metadata, type hints, and generating structured documentation.
    
    Attributes:
        source_file (str): Path to the Python file being parsed
        module_ast (ast.Module): AST representation of the source file
    """
    
    def __init__(self, source_file: str):
        """Initialize DocStringParser with source file.
        
        Args:
            source_file: Path to Python source file
        """
        self.source_file = source_file
        with open(source_file, 'r') as f:
            self.module_ast = ast.parse(f.read())
    
    def extract_metadata(self) -> Dict[str, str]:
        """Extract metadata from module docstring.
        
        Returns:
            Dict containing parsed metadata fields
        """
        module_docstring = ast.get_docstring(self.module_ast)
        if not module_docstring:
            return {}
            
        metadata = {}
        current_field = None
        
        for line in module_docstring.split('\n'):
            if line.startswith('@'):
                key = line[1:].split(':')[0].strip()
                value = line.split(':', 1)[1].strip() if ':' in line else ''
                metadata[key] = value
                
        return metadata
    
    def parse_docstring(self, node: ast.AST) -> Dict[str, str]:
        """Parse docstring from an AST node.
        
        Args:
            node: AST node to parse docstring from
            
        Returns:
            Dict containing parsed docstring sections
        """
        docstring = ast.get_docstring(node)
        if not docstring:
            return {}
            
        sections = {
            'description': [],
            'args': [],
            'returns': [],
            'raises': [],
            'examples': []
        }
        
        current_section = 'description'
        
        for line in docstring.split('\n'):
            line = line.strip()
            if line.lower().startswith(('args:', 'returns:', 'raises:', 'examples:')):
                current_section = line.lower().split(':')[0]
            elif line:
                sections[current_section].append(line)
                
        return {k: '\n'.join(v) for k, v in sections.items()}

    def get_type_hints(self, node: ast.FunctionDef) -> Dict[str, str]:
        """Extract type hints from function definition.
        
        Args:
            node: Function definition AST node
            
        Returns:
            Dict mapping parameter names to type hints
        """
        type_hints = {}
        
        for arg in node.args.args:
            if arg.annotation:
                type_hints[arg.arg] = ast.unparse(arg.annotation)
                
        if node.returns:
            type_hints['return'] = ast.unparse(node.returns)
            
        return type_hints