"""
scripts/update_context.py

Automated context documentation and tracking script for MCP Algo project.
Updates AI context documentation and tracks changes in context over time.
"""

import os
import sys
import json
import re
from typing import Dict, List
from datetime import datetime
import glob

def extract_context_from_file(filepath: str) -> Dict:
    """Extract AI context information from a file."""
    context = {
        'file': filepath,
        'metadata': [],
        'changes': [],
        'last_updated': datetime.now().isoformat()
    }
    
    try:
        with open(filepath, 'r') as f:
            content = f.read()
            
        # Extract AI metadata
        metadata = re.findall(r'@ai_metadata(.*?)"""', content, re.DOTALL)
        if metadata:
            context['metadata'] = [m.strip() for m in metadata]
            
        # Extract context-related comments
        context_comments = re.findall(r'#\s*Context:(.*?)$', 
                                    content, 
                                    re.MULTILINE)
        if context_comments:
            context['context_notes'] = [c.strip() for c in context_comments]
            
        # Get file history
        if os.path.exists(filepath + '.history'):
            with open(filepath + '.history', 'r') as f:
                context['changes'] = json.load(f)
                
    except Exception as e:
        print(f"Error processing {filepath}: {str(e)}")
        
    return context

def generate_context_doc(contexts: List[Dict]):
    """Generate comprehensive context documentation."""
    docs_dir = 'docs/ai_context'
    if not os.path.exists(docs_dir):
        os.makedirs(docs_dir)
        
    # Generate main context document
    with open(os.path.join(docs_dir, 'context.md'), 'w') as f:
        f.write('# AI Context Documentation\n\n')
        f.write(f'Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n\n')
        
        for context in contexts:
            f.write(f'## {context["file"]}\n\n')
            
            if context['metadata']:
                f.write('### AI Metadata\n\n')
                for metadata in context['metadata']:
                    f.write(f'```python\n{metadata}\n```\n\n')
                    
            if context.get('context_notes'):
                f.write('### Context Notes\n\n')
                for note in context['context_notes']:
                    f.write(f'- {note}\n')
                f.write('\n')
                
            if context['changes']:
                f.write('### Change History\n\n')
                for change in context['changes']:
                    f.write(f'- {change}\n')
                f.write('\n')

def update_context_history(filepath: str, context: Dict):
    """Update the context history file."""
    history_file = filepath + '.history'
    
    try:
        if os.path.exists(history_file):
            with open(history_file, 'r') as f:
                history = json.load(f)
        else:
            history = []
            
        # Add new entry
        history.append({
            'timestamp': datetime.now().isoformat(),
            'metadata_count': len(context['metadata']),
            'context_notes_count': len(context.get('context_notes', [])),
            'file_path': filepath
        })
        
        # Save updated history
        with open(history_file, 'w') as f:
            json.dump(history, f, indent=2)
            
    except Exception as e:
        print(f"Error updating history for {filepath}: {str(e)}")

def main():
    """Main execution function."""
    print("Updating AI context documentation...")
    
    # Get all Python files
    python_files = glob.glob('src/**/*.py', recursive=True)
    
    # Extract context from all files
    contexts = []
    for filepath in python_files:
        context = extract_context_from_file(filepath)
        contexts.append(context)
        update_context_history(filepath, context)
    
    # Generate documentation
    generate_context_doc(contexts)
    
    print("Context documentation update complete!")

if __name__ == '__main__':
    main()