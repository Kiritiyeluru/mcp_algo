"""Context Manager Test Suite

Focuses on core context preservation functionality.
"""

import unittest
import json
import os
from monitoring.context_manager import ContextManager

class TestContextManager(unittest.TestCase):
    def setUp(self):
        self.context_manager = ContextManager()
        self.test_context = {
            "component": "test_component",
            "prompt": "test prompt",
            "generated_code": "print('test')",
            "modifications": ["initial implementation"]
        }
        
    def test_save_context(self):
        """Test basic context saving functionality."""
        context = self.context_manager.save_generation_context(
            self.test_context["component"],
            self.test_context["prompt"],
            self.test_context["generated_code"],
            self.test_context["modifications"]
        )
        
        self.assertIsNotNone(context)
        self.assertEqual(context["component"], self.test_context["component"])
        
    def test_get_latest_context(self):
        """Test context retrieval."""
        self.context_manager.save_generation_context(
            self.test_context["component"],
            self.test_context["prompt"],
            self.test_context["generated_code"],
            self.test_context["modifications"]
        )
        
        context = self.context_manager.get_latest_context()
        self.assertIsNotNone(context)
        self.assertEqual(context["component"], self.test_context["component"])
        
    def test_component_history(self):
        """Test component history tracking."""
        self.context_manager.save_generation_context(
            self.test_context["component"],
            self.test_context["prompt"],
            self.test_context["generated_code"],
            self.test_context["modifications"]
        )
        
        history = self.context_manager.get_component_history(self.test_context["component"])
        self.assertTrue(len(history) > 0)
        self.assertEqual(history[0]["component"], self.test_context["component"])
