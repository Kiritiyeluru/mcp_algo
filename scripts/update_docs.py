"""
scripts/update_docs.py

Automated documentation update script for MCP Algo project.
Updates API documentation, readmes, and ensures documentation consistency.
"""

import os
import sys
import glob
import re
from typing import List, Dict
import json

def update_api_docs():
    """Update API documentation for all Python modules."""
    src_dir = 'src'
    docs_dir = 'docs/api'
    
    if not os.path.exists(docs_dir):
        os.makedirs(docs_dir)
        
    for root, _, files in os.walk(src_dir):
        for file in files:
            if file.endswith('.py'):
                module_path = os.path.join(root, file)
                doc_path = os.path.join(docs_dir, 
                    f"{os.path.splitext(file)[0]}.md")
                
                # Generate markdown documentation
                os.system(f'pydoc-markdown {module_path} > {doc_path}')

def update_readme_links():
    """Update links in README.md to point to correct documentation."""
    with open('README.md', 'r') as f:
        content = f.read()
        
    # Update links to documentation
    content = re.sub(
        r'\[([^\]]+)\]\(docs/[^\)]+\)',
        lambda m: f'[{m.group(1)}](docs/{m.group(1).lower().replace(" ", "_")}.md)',
        content
    )
    
    with open('README.md', 'w') as f:
        f.write(content)

def update_context_docs():
    """Update AI context documentation."""
    context_dir = 'docs/ai_context'
    if not os.path.exists(context_dir):
        os.makedirs(context_dir)
        
    # Get all Python files
    python_files = glob.glob('src/**/*.py', recursive=True)
    
    for file in python_files:
        # Extract context from docstrings
        with open(file, 'r') as f:
            content = f.read()
            context = re.findall(r'@ai_metadata(.*?)"""', content, re.DOTALL)
            
        if context:
            context_file = os.path.join(
                context_dir, 
                f"{os.path.splitext(os.path.basename(file))[0]}_context.md"
            )
            with open(context_file, 'w') as f:
                f.write(f"# AI Context for {file}\n\n")
                for ctx in context:
                    f.write(f"```python\n{ctx.strip()}\n```\n\n")

def main():
    """Main execution function."""
    print("Updating API documentation...")
    update_api_docs()
    
    print("Updating README links...")
    update_readme_links()
    
    print("Updating context documentation...")
    update_context_docs()
    
    print("Documentation update complete!")

if __name__ == '__main__':
    main()