# Tool Catalog: Drupal Component Development Agent

## Tool: search_component_library

**Description**: Search the existing component library for matching or similar components before creating new ones.

**Parameters**:
```json
{
  "type": "object",
  "properties": {
    "query": { "type": "string" },
    "category": {
      "type": "string",
      "enum": ["hero", "content", "conversion", "trust", "navigation", "media", "all"],
      "default": "all"
    },
    "include_variants": { "type": "boolean", "default": true }
  },
  "required": ["query"]
}
```

**Returns**: List of matching components with similarity scores

---

## Tool: create_component_spec

**Description**: Generate a structured component specification document.

**Parameters**:
```json
{
  "type": "object",
  "properties": {
    "component_name": { "type": "string" },
    "category": {
      "type": "string",
      "enum": ["hero", "content", "conversion", "trust", "navigation", "media"]
    },
    "purpose": { "type": "string" },
    "variants": {
      "type": "array",
      "items": { "type": "string" }
    },
    "visual_variants": {
      "type": "array",
      "items": {
        "type": "string",
        "enum": ["light", "dark", "neutral", "accent"]
      },
      "default": ["light", "dark"]
    },
    "layout_variants": {
      "type": "array",
      "items": {
        "type": "string",
        "enum": ["left", "center", "right", "split"]
      },
      "default": ["left", "center"]
    }
  },
  "required": ["component_name", "category", "purpose"]
}
```

**Returns**: Complete component specification JSON

---

## Tool: define_data_model

**Description**: Define the field structure for a component's data model.

**Parameters**:
```json
{
  "type": "object",
  "properties": {
    "component_name": { "type": "string" },
    "fields": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": { "type": "string" },
          "type": {
            "type": "string",
            "enum": ["text", "rich_text", "media", "cta", "select", "boolean", "link", "image", "video", "reference"]
          },
          "required": { "type": "boolean", "default": false },
          "description": { "type": "string" },
          "cardinality": { "type": "integer", "default": 1 },
          "allowed_values": {
            "type": "array",
            "items": { "type": "string" }
          }
        },
        "required": ["name", "type"]
      }
    }
  },
  "required": ["component_name", "fields"]
}
```

**Returns**: Data model specification with field definitions

---

## Tool: map_to_drupal

**Description**: Map a component specification to Drupal architecture (Paragraph type, fields, display modes).

**Parameters**:
```json
{
  "type": "object",
  "properties": {
    "component_spec": { "type": "object" },
    "paragraph_type_name": { "type": "string" },
    "enable_layout_builder": { "type": "boolean", "default": true },
    "display_modes": {
      "type": "array",
      "items": { "type": "string" },
      "default": ["default", "teaser"]
    }
  },
  "required": ["component_spec"]
}
```

**Returns**: Drupal schema with Paragraph config, field config, and display mode config

---

## Tool: generate_twig_component

**Description**: Generate a Twig template for a component with proper inheritance and accessibility markup.

**Parameters**:
```json
{
  "type": "object",
  "properties": {
    "component_name": { "type": "string" },
    "category": { "type": "string" },
    "fields": {
      "type": "array",
      "items": { "type": "string" }
    },
    "variants": {
      "type": "array",
      "items": { "type": "string" }
    },
    "use_design_tokens": { "type": "boolean", "default": true },
    "semantic_html": { "type": "boolean", "default": true },
    "aria_labels": { "type": "boolean", "default": true }
  },
  "required": ["component_name", "category"]
}
```

**Returns**: Twig template code with variant handling and accessibility attributes

---

## Tool: generate_component_css

**Description**: Generate CSS architecture for a component using BEM naming and design tokens.

**Parameters**:
```json
{
  "type": "object",
  "properties": {
    "component_name": { "type": "string" },
    "variants": {
      "type": "array",
      "items": { "type": "string" }
    },
    "responsive": { "type": "boolean", "default": true },
    "breakpoints": {
      "type": "array",
      "items": { "type": "string" },
      "default": ["mobile", "tablet", "desktop", "wide"]
    },
    "use_container_queries": { "type": "boolean", "default": false }
  },
  "required": ["component_name"]
}
```

**Returns**: CSS specification with BEM classes, token references, and responsive rules

---

## Tool: generate_component_js

**Description**: Generate JavaScript behavior specification for a component (progressive enhancement).

**Parameters**:
```json
{
  "type": "object",
  "properties": {
    "component_name": { "type": "string" },
    "interactions": {
      "type": "array",
      "items": {
        "type": "string",
        "enum": ["click", "hover", "scroll", "resize", "keyboard", "touch", "animation"]
      }
    },
    "framework": {
      "type": "string",
      "enum": ["vanilla", "alpine", "stimulus"],
      "default": "vanilla"
    },
    "progressive_enhancement": { "type": "boolean", "default": true }
  },
  "required": ["component_name"]
}
```

**Returns**: JavaScript behavior specification with event handling and state management

---

## Tool: generate_theme_mapping

**Description**: Map component visual properties to design system tokens.

**Parameters**:
```json
{
  "type": "object",
  "properties": {
    "component_name": { "type": "string" },
    "token_types": {
      "type": "array",
      "items": {
        "type": "string",
        "enum": ["colors", "spacing", "typography", "radius", "shadow"]
      },
      "default": ["colors", "spacing", "typography", "radius", "shadow"]
    }
  },
  "required": ["component_name"]
}
```

**Returns**: Theme mapping specification with token references for all visual properties

---

## Tool: validate_accessibility

**Description**: Validate a component specification against WCAG 2.2 AA requirements.

**Parameters**:
```json
{
  "type": "object",
  "properties": {
    "component_spec": { "type": "object" },
    "check_contrast": { "type": "boolean", "default": true },
    "check_keyboard": { "type": "boolean", "default": true },
    "check_screen_reader": { "type": "boolean", "default": true },
    "check_semantic_html": { "type": "boolean", "default": true },
    "check_focus_management": { "type": "boolean", "default": true }
  },
  "required": ["component_spec"]
}
```

**Returns**: Accessibility validation report with pass/fail items and remediation

---

## Tool: validate_responsiveness

**Description**: Validate component design across all responsive breakpoints.

**Parameters**:
```json
{
  "type": "object",
  "properties": {
    "component_spec": { "type": "object" },
    "breakpoints": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": { "type": "string" },
          "width": { "type": "integer" }
        }
      },
      "default": [
        {"name": "mobile", "width": 320},
        {"name": "tablet", "width": 768},
        {"name": "desktop", "width": 1024},
        {"name": "wide", "width": 1440}
      ]
    }
  },
  "required": ["component_spec"]
}
```

**Returns**: Responsiveness validation report per breakpoint

---

## Tool: generate_documentation

**Description**: Generate comprehensive component documentation.

**Parameters**:
```json
{
  "type": "object",
  "properties": {
    "component_spec": { "type": "object" },
    "include_examples": { "type": "boolean", "default": true },
    "example_count": { "type": "integer", "default": 2 },
    "include_accessibility_notes": { "type": "boolean", "default": true },
    "include_drupal_config": { "type": "boolean", "default": true }
  },
  "required": ["component_spec"]
}
```

**Returns**: Component documentation with purpose, use cases, configuration, and examples

---

## Tool: generate_usage_examples

**Description**: Generate example configurations for a component.

**Parameters**:
```json
{
  "type": "object",
  "properties": {
    "component_spec": { "type": "object" },
    "contexts": {
      "type": "array",
      "items": { "type": "string" },
      "default": ["homepage", "landing_page", "inner_page"]
    },
    "industries": {
      "type": "array",
      "items": { "type": "string" },
      "default": ["technology", "healthcare", "finance"]
    }
  },
  "required": ["component_spec"]
}
```

**Returns**: Usage examples with sample data for different contexts and industries

---

## Tool: quality_review

**Description**: Run the complete quality review suite on a component.

**Parameters**:
```json
{
  "type": "object",
  "properties": {
    "component_spec": { "type": "object" },
    "run_accessibility": { "type": "boolean", "default": true },
    "run_responsiveness": { "type": "boolean", "default": true },
    "run_drupal_review": { "type": "boolean", "default": true },
    "run_design_system_review": { "type": "boolean", "default": true },
    "run_reusability_review": { "type": "boolean", "default": true }
  },
  "required": ["component_spec"]
}
```

**Returns**: Complete quality review report with all gate results
