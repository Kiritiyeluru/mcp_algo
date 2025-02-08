# {{ name }}

## Overview

{{ description }}

{% if metadata %}
## Metadata
{% for key, value in metadata.items() %}
- **{{ key }}**: {{ value }}
{% endfor %}
{% endif %}

{% if docstring %}
## Detailed Documentation

{% if docstring.description %}
### Description
{{ docstring.description }}
{% endif %}

{% if docstring.args %}
### Parameters
{{ docstring.args }}
{% endif %}

{% if docstring.returns %}
### Returns
{{ docstring.returns }}
{% endif %}

{% if docstring.raises %}
### Exceptions
{{ docstring.raises }}
{% endif %}
{% endif %}

{% if references %}
## Dependencies
{% for module, deps in references.items() %}
- **{{ module }}**:
  {% for dep in deps %}
  * {{ dep }}
  {% endfor %}
{% endfor %}
{% endif %}
