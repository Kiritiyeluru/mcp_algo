"""Store documentation context in Memory MCP."""

from memory_mcp import MemoryMCP
from github_mcp import GitHubMCP
import datetime

def store_context():
    memory_mcp = MemoryMCP()
    github_mcp = GitHubMCP()
    
    context = {
        'timestamp': datetime.datetime.now().isoformat(),
        'git_info': github_mcp.get_repository_info(),
        'doc_versions': {
            'mkdocs': memory_mcp.get_package_version('mkdocs'),
            'material': memory_mcp.get_package_version('mkdocs-material')
        },
        'coverage': memory_mcp.get_doc_coverage()
    }
    
    memory_mcp.store_doc_context(context)

if __name__ == '__main__':
    store_context()