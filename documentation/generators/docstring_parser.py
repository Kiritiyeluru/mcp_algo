"""
File: documentation/generators/docstring_parser.py
Purpose: Parse docstrings from Python source code
Author: AI Assistant
Environment: Production
Dependencies: ast, typing
"""

import ast
from typing import Dict, Any, Optional
from sequential_mcp import SequentialMCP

class DocStringParser:
    """Parse and extract documentation from Python docstrings."""
    
    def __init__(self, file_path: str):
        """
        Initialize DocStringParser.
        
        Args:
            file_path: Path to Python source file
        """
        self.file_path = file_path
        self.module_ast = self._parse_file()
        self.sequential_mcp = SequentialMCP()
        
    def _parse_file(self) -> ast.Module:
        """
        Parse Python file into AST.
        
        Returns:
            AST module node
        """
        with open(self.file_path, 'r') as f:
            return ast.parse(f.read())
            
    def extract_metadata(self) -> Dict[str, Any]:
        """
        Extract metadata from module-level docstring.
        
        Returns:
            Dictionary of metadata fields
        """
        try:
            # Get module docstring
            if not (isinstance(self.module_ast.body[0], ast.Expr) and 
                    isinstance(self.module_ast.body[0].value, ast.Str)):
                return {}
                
            docstring = self.module_ast.body[0].value.s
            
            # Use sequential thinking to parse metadata
            return self.sequential_mcp.analyze_metadata(docstring)
            
        except Exception as e:
            self.sequential_mcp.handle_error({
                'context': 'metadata_extraction',
                'file': self.file_path,
                'error': str(e)
            })
            raise
    
    def parse_docstring(self, node: ast.AST) -> Optional[Dict[str, Any]]:
        """
        Parse docstring from AST node.
        
        Args:
            node: AST node to parse
            
        Returns:
            Parsed docstring information
        """
        try:
            # Use sequential thinking for validation
            validation = self.sequential_mcp.validate_docstring(node)
            if not validation['valid']:
                return None
                
            result = {
                'description': '',
                'args': [],
                'returns': None,
                'raises': []
            }
            
            docstring = ast.get_docstring(node)
            if not docstring:
                return result
                
            # Parse with sequential thinking
            parsed = self.sequential_mcp.parse_docstring_content(docstring)
            
            result.update(parsed)
            return result
            
        except Exception as e:
            self.sequential_mcp.handle_error({
                'context': 'docstring_parsing', 
                'file': self.file_path,
                'node': node.__class__.__name__,
                'error': str(e)
            })
            raise
