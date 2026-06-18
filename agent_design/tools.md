# Tool Catalog: Drupal Theme Design Agent

## Tool: gather_requirements

**Description**: Collect business, content, design, and technical requirements from the user before any design work begins.

**Parameters**:
```json
{
  "type": "object",
  "properties": {
    "category": {
      "type": "string",
      "enum": ["business", "content", "design", "technical", "all"]
    },
    "questions": {
      "type": "array",
      "items": { "type": "string" }
    }
  },
  "required": ["category"]
}
```

**Returns**: Requirement specification object

---

## Tool: create_design_system

**Description**: Generate a complete design system specification including colors, typography, spacing, grid, and breakpoints.

**Parameters**:
```json
{
  "type": "object",
  "properties": {
    "brand_colors": {
      "type": "array",
      "items": { "type": "string", "pattern": "^#[0-9A-Fa-f]{6}$" }
    },
    "industry": { "type": "string" },
    "style_direction": {
      "type": "string",
      "enum": ["minimal", "corporate", "creative", "premium", "playful"]
    },
    "accessibility_level": {
      "type": "string",
      "enum": ["AA", "AAA"],
      "default": "AA"
    }
  },
  "required": ["industry", "style_direction"]
}
```

**Returns**: Design system specification with tokens

---

## Tool: define_theme_architecture

**Description**: Define the Drupal theme file structure, base theme, asset strategy, and library configuration.

**Parameters**:
```json
{
  "type": "object",
  "properties": {
    "theme_name": { "type": "string" },
    "base_theme": {
      "type": "string",
      "enum": ["classy", "stable", "olivero", "claro", "custom"]
    },
    "use_layout_builder": { "type": "boolean", "default": true },
    "use_paragraphs": { "type": "boolean", "default": true },
    "css_framework": {
      "type": "string",
      "enum": ["none", "tailwind", "bootstrap", "custom"]
    },
    "js_framework": {
      "type": "string",
      "enum": ["none", "alpine", "stimulus", "custom"]
    }
  },
  "required": ["theme_name", "base_theme"]
}
```

**Returns**: Theme architecture specification with file tree

---

## Tool: design_component

**Description**: Design a specific Drupal component with Twig template, CSS architecture, and accessibility notes.

**Parameters**:
```json
{
  "type": "object",
  "properties": {
    "component_name": { "type": "string" },
    "component_type": {
      "type": "string",
      "enum": ["header", "footer", "navigation", "hero", "card", "teaser", "article", "form", "search", "cta", "gallery", "other"]
    },
    "variants": {
      "type": "array",
      "items": { "type": "string" }
    },
    "responsive": { "type": "boolean", "default": true },
    "accessibility_notes": { "type": "boolean", "default": true }
  },
  "required": ["component_name", "component_type"]
}
```

**Returns**: Component specification with Twig, CSS, and ARIA guidance

---

## Tool: generate_twig_template

**Description**: Generate a Drupal 11 Twig template with proper inheritance, template suggestions, and accessibility markup.

**Parameters**:
```json
{
  "type": "object",
  "properties": {
    "template_name": { "type": "string" },
    "content_type": { "type": "string" },
    "view_mode": { "type": "string", "default": "default" },
    "fields": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": { "type": "string" },
          "type": { "type": "string" },
          "label": { "type": "string" },
          "required": { "type": "boolean" }
        }
      }
    },
    "semantic_markup": { "type": "boolean", "default": true }
  },
  "required": ["template_name"]
}
```

**Returns**: Twig template code with documentation

---

## Tool: audit_accessibility

**Description**: Review a design or component specification against WCAG 2.2 AA requirements.

**Parameters**:
```json
{
  "type": "object",
  "properties": {
    "target": { "type": "string" },
    "target_type": {
      "type": "string",
      "enum": ["design_system", "component", "template", "full_theme"]
    },
    "level": {
      "type": "string",
      "enum": ["AA", "AAA"],
      "default": "AA"
    }
  },
  "required": ["target", "target_type"]
}
```

**Returns**: Accessibility audit report with pass/fail items and remediation guidance

---

## Tool: audit_performance

**Description**: Evaluate theme architecture and design decisions against Core Web Vitals and Drupal performance best practices.

**Parameters**:
```json
{
  "type": "object",
  "properties": {
    "theme_architecture": { "type": "object" },
    "check_critical_css": { "type": "boolean", "default": true },
    "check_image_strategy": { "type": "boolean", "default": true },
    "check_js_budget": { "type": "boolean", "default": true },
    "check_cache_strategy": { "type": "boolean", "default": true }
  },
  "required": ["theme_architecture"]
}
```

**Returns**: Performance audit report with recommendations

---

## Tool: define_layout_strategy

**Description**: Define the Layout Builder strategy including section types, block restrictions, and editor permissions.

**Parameters**:
```json
{
  "type": "object",
  "properties": {
    "use_layout_builder": { "type": "boolean", "default": true },
    "layout_plugins": {
      "type": "array",
      "items": {
        "type": "string",
        "enum": ["one_col", "two_col", "three_col", "four_col", "custom"]
      }
    },
    "allowed_block_categories": {
      "type": "array",
      "items": { "type": "string" }
    },
    "editor_restrictions": {
      "type": "object",
      "properties": {
        "restrict_layouts": { "type": "boolean" },
        "restrict_blocks": { "type": "boolean" },
        "restrict_colors": { "type": "boolean" }
      }
    }
  }
}
```

**Returns**: Layout strategy specification

---

## Tool: generate_libraries_yml

**Description**: Generate Drupal libraries.yml definitions for component-level CSS/JS asset loading.

**Parameters**:
```json
{
  "type": "object",
  "properties": {
    "theme_name": { "type": "string" },
    "components": {
      "type": "array",
      "items": { "type": "string" }
    },
    "global_css": { "type": "boolean", "default": true },
    "global_js": { "type": "boolean", "default": true },
    "use_external_dependencies": {
      "type": "array",
      "items": { "type": "string" }
    }
  },
  "required": ["theme_name"]
}
```

**Returns**: libraries.yml content

---

## Tool: review_theme_spec

**Description**: Perform a comprehensive review of the complete theme specification against Drupal 11 best practices.

**Parameters**:
```json
{
  "type": "object",
  "properties": {
    "theme_spec": { "type": "object" },
    "check_coding_standards": { "type": "boolean", "default": true },
    "check_security": { "type": "boolean", "default": true },
    "check_scalability": { "type": "boolean", "default": true },
    "check_editor_experience": { "type": "boolean", "default": true }
  },
  "required": ["theme_spec"]
}
```

**Returns**: Comprehensive review report with severity-rated findings
