"""Generate API documentation from Python docstrings."""

import os
import sys
from documentation.generators.docstring_parser import DocStringParser
from documentation.generators.template_processor import TemplateProcessor
from documentation.generators.cross_reference_manager import CrossReferenceManager
from memory_mcp import MemoryMCP
from sequential_mcp import SequentialMCP

def generate_api_docs():
    memory_mcp = MemoryMCP()
    sequential_mcp = SequentialMCP()
    
    # Process each Python module
    for root, _, files in os.walk('documentation'):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                try:
                    # Parse docstrings
                    parser = DocStringParser(file_path)
                    data = {
                        'metadata': parser.extract_metadata(),
                        'docstring': parser.parse_docstring(parser.module_ast),
                        'file_path': file_path
                    }
                    
                    # Store context in memory
                    memory_mcp.store_doc_context(data)
                    
                    # Generate markdown
                    template = sequential_mcp.select_template(data)
                    processor = TemplateProcessor('docs/templates')
                    markdown = processor.generate_markdown(data, template)
                    
                    # Save API documentation
                    module_path = os.path.relpath(file_path, 'documentation')
                    out_path = f'docs/api/{module_path[:-3]}.md'
                    os.makedirs(os.path.dirname(out_path), exist_ok=True)
                    
                    with open(out_path, 'w') as f:
                        f.write(markdown)
                        
                except Exception as e:
                    sequential_mcp.handle_error({
                        'context': 'api_doc_generation',
                        'file': file_path,
                        'error': str(e)
                    })

if __name__ == '__main__':
    generate_api_docs()