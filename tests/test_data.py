"""
@ai_metadata
Generated: 2025-02-08
Feature: Test Data Management
Component: Test Infrastructure
Purpose: Manage test data lifecycle and isolation
Environment: test
Risk: Low
Dependencies: GitHub MCP, Memory MCP
"""

def setup_test_data():
    """Initialize test data in Memory MCP"""
    # Create test issues
    issues = create_entities({
        "entities": [
            {
                "name": "test_issue_1",
                "entityType": "github_issue",
                "observations": ["Test issue for integration testing"]
            },
            {
                "name": "test_pr_1",
                "entityType": "github_pr",
                "observations": ["Test PR for integration testing"]
            }
        ]
    })

    # Create test thought process
    thoughts = create_entities({
        "entities": [
            {
                "name": "test_thought_1",
                "entityType": "sequential_thinking",
                "observations": ["Initial test thought process"]
            }
        ]
    })

    return {"issues": issues, "thoughts": thoughts}

def cleanup_test_data(test_run_id):
    """Remove test data after tests complete"""
    # Get all test entities
    test_entities = search_nodes({
        "query": f"test_{test_run_id}"
    })

    # Delete test entities
    if test_entities:
        delete_entities({
            "entityNames": [entity["name"] for entity in test_entities]
        })

    return True

def isolate_test_context(test_name):
    """Create isolated test context"""
    return create_entities({
        "entities": [{
            "name": f"test_context_{test_name}",
            "entityType": "test_context",
            "observations": [f"Isolated context for {test_name}"]
        }]
    })

def get_test_fixtures():
    """Get standard test fixtures"""
    return {
        "github": {
            "owner": "Kiritiyeluru",
            "repo": "mcp_algo",
            "issue_number": 1,
            "pr_number": 1
        },
        "sequential": {
            "context_id": "test_1",
            "problem": "Test integration problem"
        },
        "monitoring": {
            "component": "TestComponent",
            "error_type": "TestError",
            "details": "Test error details"
        }
    }