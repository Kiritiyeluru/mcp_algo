"""
scripts/update_dependencies.py

Automated dependency documentation and tracking script for MCP Algo project.
Updates dependency documentation and generates dependency graphs.
"""

import os
import sys
import json
import subprocess
from typing import Dict, List
import pkg_resources
import networkx as nx
from datetime import datetime

def get_installed_packages() -> Dict[str, str]:
    """Get all installed Python packages and their versions."""
    return {pkg.key: pkg.version for pkg in pkg_resources.working_set}

def analyze_imports(directory: str) -> Dict[str, List[str]]:
    """Analyze Python imports in the project."""
    imports = {}
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r') as f:
                    content = f.read()
                    # Extract imports using AST or regex
                    # This is a simplified version
                    imports[filepath] = [
                        line.strip().split()[1] 
                        for line in content.split('\n') 
                        if line.strip().startswith('import') or 
                           line.strip().startswith('from')
                    ]
    return imports

def generate_dependency_doc():
    """Generate comprehensive dependency documentation."""
    docs_dir = 'docs/dependencies'
    if not os.path.exists(docs_dir):
        os.makedirs(docs_dir)
        
    # Get installed packages
    packages = get_installed_packages()
    
    # Analyze project imports
    imports = analyze_imports('src')
    
    # Generate markdown documentation
    with open(os.path.join(docs_dir, 'dependencies.md'), 'w') as f:
        f.write('# Project Dependencies\n\n')
        f.write(f'Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n\n')
        
        f.write('## Installed Packages\n\n')
        for pkg, version in sorted(packages.items()):
            f.write(f'- {pkg}: v{version}\n')
            
        f.write('\n## Project Import Analysis\n\n')
        for file, file_imports in imports.items():
            f.write(f'### {file}\n\n')
            for imp in sorted(set(file_imports)):
                f.write(f'- {imp}\n')
            f.write('\n')

def update_requirements():
    """Update requirements.txt file."""
    subprocess.run(['pip', 'freeze', '>', 'requirements.txt'], shell=True)
    
    # Also create a dev-requirements.txt for development dependencies
    with open('requirements.txt', 'r') as f:
        reqs = f.read().splitlines()
        
    with open('dev-requirements.txt', 'w') as f:
        f.write('# Development dependencies\n')
        dev_packages = [
            'pytest',
            'pytest-cov',
            'black',
            'flake8',
            'mypy',
            'pydoc-markdown',
            'mkdocs',
            'mkdocstrings',
        ]
        for pkg in dev_packages:
            matching = [r for r in reqs if r.startswith(pkg)]
            if matching:
                f.write(f'{matching[0]}\n')
            else:
                f.write(f'{pkg}\n')

def main():
    """Main execution function."""
    print("Generating dependency documentation...")
    generate_dependency_doc()
    
    print("Updating requirements files...")
    update_requirements()
    
    print("Dependency documentation update complete!")

if __name__ == '__main__':
    main()