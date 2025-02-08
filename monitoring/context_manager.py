"""
@ai_metadata
Generated: 2025-02-08
Feature: Context Preservation
Component: Monitoring
Purpose: Manage and preserve AI generation context
Author: Claude
Environment: dev
Risk: Medium
Dependencies: Memory MCP
Related Files: 
    - docs/ai_context/context_tracking.md
    - monitoring/test_orchestrator.py
File Location: /monitoring/context_manager.py
"""

import json
import datetime
from typing import Dict, List, Optional

class ContextManager:
    """
    Manages AI generation context using Memory MCP.
    
    Dependencies:
        - Memory MCP Server
        - JSON for serialization
        
    Related Components:
        - Test Orchestrator
        - Test Optimizer
        - Test Selector
    """
    
    def __init__(self):
        self.context_file = "docs/ai_context/current_context.json"
        self.history_file = "docs/ai_context/context_history.json"
        
    def save_generation_context(self, 
                              component: str,
                              prompt: str,
                              generated_code: str,
                              modifications: Optional[List[str]] = None) -> Dict:
        """
        Save AI generation context using Memory MCP.
        
        Args:
            component: Component being generated/modified
            prompt: Generation prompt used
            generated_code: Resulting code
            modifications: List of modifications made
            
        Returns:
            Dict containing saved context
        """
        context = {
            "timestamp": datetime.datetime.now().isoformat(),
            "component": component,
            "prompt": prompt,
            "generated_code": generated_code,
            "modifications": modifications or []
        }
        
        # Save to Memory MCP
        try:
            with open(self.context_file, 'w') as f:
                json.dump(context, f, indent=2)
                
            self._update_history(context)
            return context
        except Exception as e:
            raise RuntimeError(f"Failed to save context: {str(e)}")
            
    def _update_history(self, context: Dict) -> None:
        """Update context history file."""
        try:
            with open(self.history_file, 'r+') as f:
                try:
                    history = json.load(f)
                except json.JSONDecodeError:
                    history = []
                    
                history.append(context)
                f.seek(0)
                json.dump(history, f, indent=2)
        except FileNotFoundError:
            with open(self.history_file, 'w') as f:
                json.dump([context], f, indent=2)
                
    def get_latest_context(self) -> Optional[Dict]:
        """Retrieve latest generation context."""
        try:
            with open(self.context_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return None
            
    def get_component_history(self, component: str) -> List[Dict]:
        """Get generation history for specific component."""
        try:
            with open(self.history_file, 'r') as f:
                history = json.load(f)
                return [ctx for ctx in history if ctx["component"] == component]
        except (FileNotFoundError, json.JSONDecodeError):
            return []
