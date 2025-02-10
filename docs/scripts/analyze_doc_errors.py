"""Analyze documentation errors and store insights."""

from memory_mcp import MemoryMCP
from sequential_mcp import SequentialMCP
from github_mcp import GitHubMCP

def analyze_errors():
    memory_mcp = MemoryMCP()
    sequential_mcp = SequentialMCP()
    github_mcp = GitHubMCP()
    
    # Get error context
    errors = memory_mcp.get_doc_errors()
    
    # Analyze patterns
    analysis = sequential_mcp.analyze_error_patterns(errors)
    
    # Store insights
    memory_mcp.store_error_analysis(analysis)
    
    # Create GitHub issue if needed
    if analysis['severity'] == 'high':
        github_mcp.create_doc_error_issue(analysis)

if __name__ == '__main__':
    analyze_errors()