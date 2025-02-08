"""
@ai_metadata
Generated: 2025-02-08
Feature: Sequential Thinking Integration
Component: Integration Core
Purpose: Manage Sequential Thinking MCP interactions
Environment: dev
Risk: Medium
Dependencies: Sequential Thinking MCP, Memory MCP
Related Files: github_memory_integration.py, monitoring.py
"""

def store_thought_process(context_id, problem):
    """Store sequential thinking process in Memory MCP"""
    # Generate thought process using Sequential Thinking MCP
    thought = sequentialthinking({
        "thought": f"Analyzing problem: {problem}",
        "thoughtNumber": 1,
        "totalThoughts": 5,
        "nextThoughtNeeded": True
    })
    
    # Create entity in Memory MCP
    entities = [{
        "name": f"thought_process_{context_id}",
        "entityType": "sequential_thinking",
        "observations": [
            f"Problem: {problem}",
            f"Initial thought: {thought['thought']}"
        ]
    }]
    
    create_entities({"entities": entities})
    return context_id

def add_thought_step(context_id, step_number, previous_thought):
    """Add new thought step to existing process"""
    # Generate next thought
    thought = sequentialthinking({
        "thought": f"Building on: {previous_thought}",
        "thoughtNumber": step_number,
        "totalThoughts": 5,
        "nextThoughtNeeded": step_number < 5
    })
    
    # Add observation to existing entity
    add_observations({
        "observations": [{
            "entityName": f"thought_process_{context_id}",
            "contents": [f"Step {step_number}: {thought['thought']}"]
        }]
    })
    
    return thought

def link_thought_to_issue(thought_id, issue_number):
    """Link thought process to GitHub issue"""
    relations = [{
        "from": f"thought_process_{thought_id}",
        "to": f"issue_{issue_number}",
        "relationType": "analysis_for"
    }]
    
    create_relations({"relations": relations})
    return True

def get_thought_process(context_id):
    """Retrieve complete thought process"""
    result = search_nodes({"query": f"thought_process_{context_id}"})
    return result