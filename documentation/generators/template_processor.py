"""
File: documentation/generators/template_processor.py
Purpose: Process documentation templates and generate formatted output
Author: AI Assistant
Environment: Production
Dependencies: jinja2, markdown
"""

import os
from typing import Dict, Optional, List
from jinja2 import Environment, FileSystemLoader, Template
import markdown

class TemplateProcessor:
    """Process documentation templates and generate formatted output.
    
    This class handles loading template files, substituting variables,
    and generating formatted documentation in Markdown and HTML formats.
    
    Attributes:
        template_dir (str): Directory containing template files
        env (Environment): Jinja2 environment for template processing
        default_template (str): Name of default template to use
    """
    
    def __init__(self, template_dir: str, default_template: str = 'class_template.md'):
        """Initialize TemplateProcessor with template directory.
        
        Args:
            template_dir: Path to directory containing templates
            default_template: Name of default template file
        """
        self.template_dir = template_dir
        self.default_template = default_template
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
    def load_template(self, template_name: Optional[str] = None) -> Template:
        """Load a template file.
        
        Args:
            template_name: Name of template file to load (default: use default_template)
            
        Returns:
            Loaded Jinja2 template
            
        Raises:
            FileNotFoundError: If template file doesn't exist
        """
        template_name = template_name or self.default_template
        return self.env.get_template(template_name)
        
    def process_template(self, data: Dict, template_name: Optional[str] = None) -> str:
        """Process template with provided data.
        
        Args:
            data: Dictionary of variables to substitute in template
            template_name: Optional template name to use
            
        Returns:
            Processed template content as string
        """
        template = self.load_template(template_name)
        return template.render(**data)
        
    def generate_markdown(self, data: Dict, template_name: Optional[str] = None) -> str:
        """Generate Markdown documentation.
        
        Args:
            data: Documentation data to include
            template_name: Optional template to use
            
        Returns:
            Generated Markdown content
        """
        return self.process_template(data, template_name)
        
    def generate_html(self, data: Dict, template_name: Optional[str] = None) -> str:
        """Generate HTML documentation.
        
        Args:
            data: Documentation data to include
            template_name: Optional template to use
            
        Returns:
            Generated HTML content
        """
        markdown_content = self.generate_markdown(data, template_name)
        return markdown.markdown(markdown_content, extensions=['fenced_code', 'tables'])
        
    def validate_template_data(self, data: Dict, template_name: Optional[str] = None) -> List[str]:
        """Validate that all required template variables are provided.
        
        Args:
            data: Template data to validate
            template_name: Optional template to validate against
            
        Returns:
            List of missing required variables (empty if all present)
        """
        template = self.load_template(template_name)
        template_vars = self.env.parse(template.source).find_all(Template)
        
        missing_vars = []
        for var in template_vars:
            if var.name not in data:
                missing_vars.append(var.name)
                
        return missing_vars