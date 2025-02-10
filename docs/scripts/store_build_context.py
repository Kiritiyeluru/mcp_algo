"""Store documentation build context in Memory MCP with retry logic."""

from memory_mcp import MemoryMCP
from github_mcp import GitHubMCP
import os
import time
import datetime

def store_build_context():
    # Get retry settings from environment
    retry_count = int(os.getenv('MEMORY_MCP_RETRY_COUNT', '3'))
    retry_delay = int(os.getenv('MEMORY_MCP_RETRY_DELAY', '1'))
    
    memory_mcp = MemoryMCP()
    github_mcp = GitHubMCP()
    
    # Build context data
    context = {
        'timestamp': datetime.datetime.now().isoformat(),
        'commit': github_mcp.get_current_commit(),
        'status': 'success',
        'build_info': {
            'mkdocs_version': memory_mcp.get_package_version('mkdocs'),
            'python_version': memory_mcp.get_python_version()
        }
    }
    
    # Store with retry
    for attempt in range(retry_count):
        try:
            memory_mcp.store_doc_context(context)
            print('Successfully stored build context')
            return
        except Exception as e:
            if attempt == retry_count - 1:
                raise
            print(f'Retry {attempt + 1}/{retry_count}: {str(e)}')
            time.sleep(retry_delay)

if __name__ == '__main__':
    store_build_context()