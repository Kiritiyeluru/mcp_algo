"""
@ai_metadata
Generated: 2025-02-08
Feature: Test Monitoring Dashboard
Component: Test Infrastructure
Purpose: Monitor and report test execution and results
Environment: test
Risk: Low
Dependencies: GitHub MCP, Memory MCP
"""

def create_test_report(test_results):
    """Create GitHub issue with test results"""
    return create_issue({
        "owner": "Kiritiyeluru",
        "repo": "mcp_algo",
        "title": "Test Execution Report",
        "body": format_test_results(test_results),
        "labels": ["test-report", "monitoring"]
    })

def store_test_metrics(metrics):
    """Store test metrics in Memory MCP"""
    return create_entities({
        "entities": [{
            "name": f"test_metrics_{metrics['run_id']}",
            "entityType": "test_metrics",
            "observations": [
                f"Total tests: {metrics['total']}",
                f"Passed: {metrics['passed']}",
                f"Failed: {metrics['failed']}",
                f"Duration: {metrics['duration']}s"
            ]
        }]
    })

def track_performance_metrics(metrics):
    """Track test performance metrics"""
    return create_entities({
        "entities": [{
            "name": f"performance_metrics_{metrics['timestamp']}",
            "entityType": "performance_metrics",
            "observations": [
                f"Memory usage: {metrics['memory_usage']}MB",
                f"CPU usage: {metrics['cpu_usage']}%",
                f"Network calls: {metrics['network_calls']}"
            ]
        }]
    })

def send_failure_notification(failure_data):
    """Create GitHub issue for test failures"""
    return create_issue({
        "owner": "Kiritiyeluru",
        "repo": "mcp_algo",
        "title": f"Test Failure Alert: {failure_data['test_name']}",
        "body": format_failure_details(failure_data),
        "labels": ["test-failure", "high-priority"]
    })