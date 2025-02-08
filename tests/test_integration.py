"""
@ai_metadata
Generated: 2025-02-08
Feature: Integration Tests
Component: Testing
Purpose: Test MCP integration functionality
Environment: test
Risk: Low
Dependencies: pytest, MCP servers
Related Files: github_memory_integration.py, sequential_integration.py, monitoring.py
"""

import pytest
from mcp_integration import (
    github_memory_integration as gm,
    sequential_integration as si,
    monitoring as mon
)

# Test fixtures
@pytest.fixture
def test_issue():
    return {
        "owner": "Kiritiyeluru",
        "repo": "mcp_algo",
        "issue_number": 1
    }

@pytest.fixture
def test_pr():
    return {
        "owner": "Kiritiyeluru",
        "repo": "mcp_algo",
        "pull_number": 1
    }

@pytest.fixture
def test_thought():
    return {
        "context_id": "test_1",
        "problem": "Test integration problem"
    }

# GitHub-Memory Integration Tests
def test_store_issue_context(test_issue):
    result = gm.store_issue_context(**test_issue)
    assert result == True
    
    # Verify storage
    context = gm.get_issue_context(test_issue["issue_number"])
    assert context is not None

def test_store_pr_context(test_pr):
    result = gm.store_pr_context(**test_pr)
    assert result == True
    
    # Verify storage
    context = gm.get_pr_context(test_pr["pull_number"])
    assert context is not None

def test_link_issue_pr(test_issue, test_pr):
    result = gm.link_issue_pr(
        test_issue["issue_number"],
        test_pr["pull_number"]
    )
    assert result == True

# Sequential Thinking Integration Tests
def test_store_thought_process(test_thought):
    context_id = si.store_thought_process(**test_thought)
    assert context_id is not None
    
    # Verify storage
    thought = si.get_thought_process(context_id)
    assert thought is not None

def test_add_thought_step(test_thought):
    context_id = test_thought["context_id"]
    thought = si.add_thought_step(
        context_id,
        step_number=2,
        previous_thought="Initial test thought"
    )
    assert thought is not None

def test_link_thought_to_issue(test_thought, test_issue):
    result = si.link_thought_to_issue(
        test_thought["context_id"],
        test_issue["issue_number"]
    )
    assert result == True

# Monitoring System Tests
def test_check_github_health():
    status = mon.check_github_health()
    assert status["status"] in ["healthy", "error"]
    if status["status"] == "healthy":
        assert "latency" in status

def test_check_memory_health():
    status = mon.check_memory_health()
    assert status["status"] in ["healthy", "error"]
    if status["status"] == "healthy":
        assert "latency" in status

def test_check_sequential_health():
    status = mon.check_sequential_health()
    assert status["status"] in ["healthy", "error"]
    if status["status"] == "healthy":
        assert "latency" in status

def test_create_system_alert():
    result = mon.create_system_alert(
        component="TestComponent",
        error_type="TestError",
        details="Test alert details"
    )
    assert result == True

def test_check_integration_health():
    status = mon.check_integration_health()
    assert all(key in status for key in ["github", "memory", "sequential"])
    for component in status.values():
        assert component["status"] in ["healthy", "error"]