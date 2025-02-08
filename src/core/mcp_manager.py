"""
src/core/mcp_manager.py

MCP Manager for handling interactions between different MCP servers.

@ai_metadata
Generated: 2025-02-08
Component: Core Infrastructure
Purpose: Manage MCP server interactions
Dependencies: None
Risk: Low
Coverage: 90%
"""

class MCPManager:
    """Manager class for MCP server interactions."""
    
    def __init__(self):
        """Initialize MCP manager."""
        self.servers = {}
        self.contexts = {}
        
    def register_server(self, name, server):
        """Register an MCP server."""
        self.servers[name] = server
        
    def get_server(self, name):
        """Get registered MCP server."""
        return self.servers.get(name)
        
    def store_context(self, context_id, data):
        """Store context data."""
        self.contexts[context_id] = data
        
    def get_context(self, context_id):
        """Retrieve context data."""
        return self.contexts.get(context_id)