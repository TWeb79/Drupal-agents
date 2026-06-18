"""
Component Agent - Drupal Component Development Functions
"""

author = "Inventions4All - github:TWeb79"

import json
import os


def generate_twig_template(component_name: str, fields: list, variants: list = None) -> str:
    """
    Generate Twig template for Drupal component.
    
    Args:
        component_name: Name of the component
        fields: List of field names to include
        variants: Optional list of component variants
    
    Returns:
        Twig template string
    """
    variant_conditions = ""
    if variants:
        for variant in variants:
            variant_conditions += "{% if attributes.hasClass('" + variant + "') %}...{% endif %}\n"
    
    field_markup = "\n".join(["{{ " + f + " }}\n<p class=\"" + component_name + "__" + f.replace('_', '-') + "\">{{ " + f + " }}</p>" for f in fields])
    
    return "<div class=\"" + component_name + "\">\n" + variant_conditions + field_markup + "\n</div>"


def generate_component_library(theme_name: str, component_name: str) -> dict:
    """
    Generate component library definition.
    
    Returns YAML config for component attachment.
    """
    return {
        "library": {
            "theme": {
                theme_name: {
                    "version": "VERSION",
                    "components": {
                        component_name: {
                            "css": [f"css/components/{component_name}.css"],
                            "js": [f"js/components/{component_name}.js"],
                        }
                    }
                }
            }
        }
    }


def create_yaml_config(component_name: str, bundle_config: dict) -> str:
    """Generate YAML config for Paragraph bundle or content type."""
    return f"""langcode: en
status: true
dependencies:
  module:
    - paragraphs
id: {component_name}
label: {bundle_config.get('label', component_name)}
icon: {bundle_config.get('icon', 'paragraphs-i18n')}
"""