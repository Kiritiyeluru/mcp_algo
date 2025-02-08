"""
@ai_metadata
Generated: 2025-02-08
Feature: Intelligent Test Selection
Component: Test Infrastructure
Purpose: Intelligently select tests based on changes and context
Environment: test
Risk: Low
Dependencies: All MCP servers
"""

def analyze_code_changes():
    """Analyze code changes to determine relevant tests"""
    # Use Sequential Thinking for change analysis
    analysis = sequentialthinking({
        "thought": "Analyzing code changes and impact",
        "thoughtNumber": 1,
        "totalThoughts": 3,
        "nextThoughtNeeded": True
    })

    # Store analysis results
    create_entities({
        "entities": [{
            "name": "change_analysis",
            "entityType": "code_analysis",
            "observations": [
                f"Change impact: {analysis['thought']}",
                "Test coverage required: High"
            ]
        }]
    })

    return analysis

def select_critical_tests():
    """Select critical tests based on impact analysis"""
    # Get historical data
    history = search_nodes({
        "query": "test_execution_history"
    })

    # Analyze using Sequential Thinking
    selection = sequentialthinking({
        "thought": "Selecting critical tests",
        "thoughtNumber": 1,
        "totalThoughts": 2,
        "nextThoughtNeeded": True
    })

    # Create test selection report
    create_issue({
        "owner": "Kiritiyeluru",
        "repo": "mcp_algo",
        "title": "Critical Test Selection Report",
        "body": format_test_selection(selection),
        "labels": ["test-selection", "critical"]
    })

    return selection

def prioritize_test_suite():
    """Prioritize tests based on various factors"""
    factors = {
        "impact": analyze_code_changes(),
        "history": get_test_history(),
        "coverage": analyze_coverage()
    }

    # Create prioritization plan
    prioritization = sequentialthinking({
        "thought": "Prioritizing test suite execution",
        "thoughtNumber": 1,
        "totalThoughts": 3,
        "nextThoughtNeeded": True
    })

    return prioritization

def suggest_test_additions():
    """Suggest new tests based on coverage analysis"""
    suggestions = sequentialthinking({
        "thought": "Analyzing test coverage gaps",
        "thoughtNumber": 1,
        "totalThoughts": 2,
        "nextThoughtNeeded": True
    })

    # Store suggestions
    create_entities({
        "entities": [{
            "name": "test_suggestions",
            "entityType": "coverage_analysis",
            "observations": [
                f"Coverage gaps: {suggestions['thought']}",
                "Priority: High"
            ]
        }]
    })

    return suggestions