# AI Context Storage

Stores generation context and history for AI-assisted code generation.

## Structure
- current_context.json: Latest generation context
- context_history.json: Historical context data

## Format
```json
{
    "timestamp": "ISO datetime",
    "component": "component_name",
    "prompt": "generation prompt",
    "generated_code": "code",
    "modifications": ["list of modifications"]
}
```