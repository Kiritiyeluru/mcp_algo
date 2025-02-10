"""Generate dependency graphs for documentation."""

import os
from documentation.generators.cross_reference_manager import CrossReferenceManager

def generate_graphs():
    ref_manager = CrossReferenceManager('.')
    ref_manager.analyze_dependencies()
    
    # Generate Mermaid graph
    mermaid = ['graph TD;']
    for node in ref_manager.dependency_graph.nodes():
        for neighbor in ref_manager.dependency_graph.neighbors(node):
            mermaid.append(f'    {node}-->{neighbor};')
    
    os.makedirs('docs/graphs', exist_ok=True)
    
    # Save Mermaid graph
    with open('docs/graphs/dependencies.mmd', 'w') as f:
        f.write('\n'.join(mermaid))
    
    # Save DOT graph
    with open('docs/graphs/dependencies.dot', 'w') as f:
        f.write(ref_manager.export_dependency_graph())

if __name__ == '__main__':
    generate_graphs()