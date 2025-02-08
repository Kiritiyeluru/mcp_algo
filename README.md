# MCP Algo Documentation System

## Overview

The MCP Algo Documentation System is an advanced, automated documentation generation pipeline that leverages the Model Context Protocol (MCP) to create comprehensive, context-aware documentation for Python projects.

## Features

- 🔍 Automatic docstring parsing
- 🌐 Cross-reference generation
- 📊 Dependency graph visualization
- 🧪 Robust testing framework
- 🤖 GitHub Actions integration

## Components

### Documentation Generators

1. **DocStringParser**
   - Extracts metadata and structured information from Python docstrings
   - Supports complex docstring formats

2. **TemplateProcessor**
   - Converts parsed docstrings into formatted documentation
   - Supports multiple output formats (Markdown, HTML)

3. **CrossReferenceManager**
   - Analyzes dependencies between modules
   - Generates cross-reference links
   - Exports dependency graphs

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Running Tests

```bash
pytest tests/documentation/
```

### Generating Documentation

```bash
python run_tests.py
```

## Workflow

1. Docstrings are parsed by `DocStringParser`
2. Cross-references are analyzed by `CrossReferenceManager`
3. Documentation is generated using `TemplateProcessor`
4. Output is saved in `docs/generated/`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push and create a Pull Request

## License

MIT License

## Acknowledgments

- MCP Protocol
- GitHub Actions
- pytest
