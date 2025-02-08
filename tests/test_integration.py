"""Integration Test Suite

Verifies core system integration points.
"""

import unittest
from monitoring.context_manager import ContextManager

class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.context_manager = ContextManager()
        
    def test_context_persistence(self):
        """Verify context persistence across components."""
        test_context = {
            "component": "integration_test",
            "prompt": "test integration",
            "generated_code": "def test(): pass",
            "modifications": ["initial"]
        }
        
        # Save context
        saved = self.context_manager.save_generation_context(
            test_context["component"],
            test_context["prompt"],
            test_context["generated_code"],
            test_context["modifications"]
        )
        
        # Verify persistence
        retrieved = self.context_manager.get_latest_context()
        self.assertEqual(saved["component"], retrieved["component"])
        
    def test_history_tracking(self):
        """Verify history tracking functionality."""
        component = "history_test"
        
        # Create multiple contexts
        contexts = [
            ("prompt 1", "code 1", ["mod 1"]),
            ("prompt 2", "code 2", ["mod 2"])
        ]
        
        for prompt, code, mods in contexts:
            self.context_manager.save_generation_context(
                component, prompt, code, mods
            )
            
        # Verify history
        history = self.context_manager.get_component_history(component)
        self.assertEqual(len(history), len(contexts))
