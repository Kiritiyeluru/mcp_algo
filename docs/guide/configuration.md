# Configuration Guide

## MCP Configuration

### GitHub MCP
```yaml
github_mcp:
  repo: mcp_algo
  branch: main
  auto_update: true
```

### Memory MCP
```yaml
memory_mcp:
  context_retention: 30d
  auto_cleanup: true
```

### Sequential MCP
```yaml
sequential_mcp:
  validation_depth: 3
  error_threshold: 0.01
```

## Documentation Settings

- Template customization
- Output formats
- Auto-generation rules