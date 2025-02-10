"""Validate documentation content quality and completeness."""

from memory_mcp import MemoryMCP
from sequential_mcp import SequentialMCP

def validate_content():
    memory_mcp = MemoryMCP()
    sequential_mcp = SequentialMCP()
    
    # Get documentation context
    doc_context = memory_mcp.get_doc_context()
    
    # Validate with sequential thinking
    validation = sequential_mcp.validate_documentation(doc_context)
    
    # Store results
    memory_mcp.store_validation_results(validation)
    
    # Return status
    return validation['status']

if __name__ == '__main__':
    validate_content()