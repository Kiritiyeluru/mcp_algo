"""Smoke Test Suite

Basic functionality verification.
"""

import unittest
from monitoring.context_manager import ContextManager

class TestSmoke(unittest.TestCase):
    def setUp(self):
        self.context_manager = ContextManager()
        
    def test_context_manager_creation(self):
        """Verify context manager instantiation."""
        self.assertIsNotNone(self.context_manager)
        
    def test_save_retrieve_cycle(self):
        """Verify basic save/retrieve functionality."""
        component = "smoke_test"
        prompt = "test prompt"
        code = "print('smoke test')"
        
        # Save context
        self.context_manager.save_generation_context(
            component, prompt, code, ["test"]
        )
        
        # Retrieve context
        context = self.context_manager.get_latest_context()
        self.assertIsNotNone(context)
        self.assertEqual(context["component"], component)
        
    def test_history_basics(self):
        """Verify basic history functionality."""
        component = "smoke_test"
        history = self.context_manager.get_component_history(component)
        self.assertIsNotNone(history)
