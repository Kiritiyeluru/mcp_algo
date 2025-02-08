"""
@ai_metadata
Generated: 2025-02-08
Feature: GitHub-Memory MCP Integration
Component: Integration Core
Purpose: Manage GitHub and Memory MCP interactions
Environment: dev
Risk: Medium
Dependencies: GitHub MCP, Memory MCP
Related Files: sequential_integration.py, monitoring.py
"""

def store_issue_context(owner, repo, issue_number):
    """Store GitHub issue context in Memory MCP"""
    # Get issue data using GitHub MCP
    issue_data = {
        "owner": owner,
        "repo": repo,
        "issue_number": issue_number
    }
    
    # Create entities in Memory MCP
    entities = [{
        "name": f"issue_{issue_number}",
        "entityType": "github_issue",
        "observations": [
            f"Repository: {owner}/{repo}",
            f"Issue number: {issue_number}"
        ]
    }]
    
    create_entities({"entities": entities})
    return True

def store_pr_context(owner, repo, pull_number):
    """Store GitHub PR context in Memory MCP"""
    # Get PR data using GitHub MCP
    pr_data = {
        "owner": owner,
        "repo": repo,
        "pull_number": pull_number
    }
    
    # Create entities in Memory MCP
    entities = [{
        "name": f"pr_{pull_number}",
        "entityType": "github_pr",
        "observations": [
            f"Repository: {owner}/{repo}",
            f"PR number: {pull_number}"
        ]
    }]
    
    create_entities({"entities": entities})
    return True

def link_issue_pr(issue_number, pr_number):
    """Create relation between issue and PR in Memory MCP"""
    relations = [{
        "from": f"issue_{issue_number}",
        "to": f"pr_{pr_number}",
        "relationType": "linked_to"
    }]
    
    create_relations({"relations": relations})
    return True

def get_issue_context(issue_number):
    """Retrieve issue context from Memory MCP"""
    result = search_nodes({"query": f"issue_{issue_number}"})
    return result

def get_pr_context(pr_number):
    """Retrieve PR context from Memory MCP"""
    result = search_nodes({"query": f"pr_{pr_number}"})
    return result