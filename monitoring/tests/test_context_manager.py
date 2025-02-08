"""Test suite for ContextManager class."""

import pytest
import json
import os
from monitoring.context_manager import ContextManager

@pytest.fixture
def context_manager():
    manager = ContextManager()
    # Clean up test files after tests
    yield manager
    for file in [manager.context_file, manager.history_file]:
        if os.path.exists(file):
            os.remove(file)

def test_save_generation_context(context_manager):
    """Test saving generation context."""
    test_context = {
        "component": "test_component",
        "prompt": "test prompt",
        "generated_code": "print('test')",
        "modifications": ["initial implementation"]
    }
    
    result = context_manager.save_generation_context(
        component=test_context["component"],
        prompt=test_context["prompt"],
        generated_code=test_context["generated_code"],
        modifications=test_context["modifications"]
    )
    
    assert result["component"] == test_context["component"]
    assert result["prompt"] == test_context["prompt"]
    assert result["generated_code"] == test_context["generated_code"]
    assert result["modifications"] == test_context["modifications"]

def test_get_latest_context(context_manager):
    """Test retrieving latest context."""
    test_context = {
        "component": "test_component",
        "prompt": "test prompt",
        "generated_code": "print('test')",
        "modifications": ["initial implementation"]
    }
    
    context_manager.save_generation_context(
        component=test_context["component"],
        prompt=test_context["prompt"],
        generated_code=test_context["generated_code"],
        modifications=test_context["modifications"]
    )
    
    latest = context_manager.get_latest_context()
    assert latest["component"] == test_context["component"]
    
def test_get_component_history(context_manager):
    """Test retrieving component history."""
    component = "test_component"
    
    # Save multiple contexts
    for i in range(3):
        context_manager.save_generation_context(
            component=component,
            prompt=f"test prompt {i}",
            generated_code=f"print('test {i}')",
            modifications=[f"modification {i}"]
        )
    
    history = context_manager.get_component_history(component)
    assert len(history) == 3
    assert all(ctx["component"] == component for ctx in history)