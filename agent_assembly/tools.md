# Tool Catalog: Drupal Website Assembly Agent

## Tool: analyze_requirements

**Description**: Analyze business requirements and produce a structured website brief.

**Parameters**:
```json
{
  "type": "object",
  "properties": {
    "business_type": {
      "type": "string",
      "enum": ["b2b", "b2c", "nonprofit", "ecommerce", "education", "government"]
    },
    "industry": { "type": "string" },
    "brand_style": {
      "type": "string",
      "enum": ["corporate", "modern", "creative", "minimal", "premium"]
    },
    "target_audience": { "type": "string" },
    "goals": {
      "type": "array",
      "items": {
        "type": "string",
        "enum": ["lead_generation", "sales", "information", "community", "support", "branding"]
      }
    }
  },
  "required": ["business_type", "industry", "brand_style", "goals"]
}
```

**Returns**: Structured website brief with recommendation summary

---

## Tool: create_sitemap

**Description**: Create the site information architecture including sitemap, navigation, and page hierarchy.

**Parameters**:
```json
{
  "type": "object",
  "properties": {
    "website_brief": { "type": "object" },
    "max_depth": { "type": "integer", "default": 3 },
    "include_utility_pages": { "type": "boolean", "default": true },
    "include_legal_pages": { "type": "boolean", "default": true }
  },
  "required": ["website_brief"]
}
```

**Returns**: Sitemap with page hierarchy and navigation structure

---

## Tool: select_theme

**Description**: Select the best matching theme from the theme library with confidence scoring.

**Parameters**:
```json
{
  "type": "object",
  "properties": {
    "website_brief": { "type": "object" },
    "require_explanation": { "type": "boolean", "default": true },
    "min_confidence": { "type": "number", "minimum": 0, "maximum": 100, "default": 70 }
  },
  "required": ["website_brief"]
}
```

**Returns**: Theme selection with confidence score, match rationale, and available components

---

## Tool: select_components

**Description**: Select required components for each page from the component library.

**Parameters**:
```json
{
  "type": "object",
  "properties": {
    "page_spec": { "type": "object" },
    "theme_id": { "type": "string" },
    "available_components": {
      "type": "array",
      "items": { "type": "string" }
    },
    "max_components_per_page": { "type": "integer", "default": 8 }
  },
  "required": ["page_spec", "theme_id"]
}
```

**Returns**: Component selection for the page with variant recommendations

---

## Tool: generate_content

**Description**: Generate all content for a page including headlines, metadata, and structured body content.

**Parameters**:
```json
{
  "type": "object",
  "properties": {
    "page_spec": { "type": "object" },
    "component_mapping": { "type": "array", "items": { "type": "object" } },
    "website_brief": { "type": "object" },
    "tone": {
      "type": "string",
      "enum": ["professional", "friendly", "authoritative", "casual", "technical"]
    },
    "seo_optimization": { "type": "boolean", "default": true }
  },
  "required": ["page_spec", "website_brief"]
}
```

**Returns**: Content package for the page (headlines, body, meta, image specs)

---

## Tool: create_drupal_plan

**Description**: Generate the complete Drupal assembly plan with entities, fields, and configurations.

**Parameters**:
```json
{
  "type": "object",
  "properties": {
    "website_blueprint": { "type": "object" },
    "content_package": { "type": "object" },
    "include_content_types": { "type": "boolean", "default": true },
    "include_paragraphs": { "type": "boolean", "default": true },
    "include_layout_builder": { "type": "boolean", "default": true },
    "include_menus": { "type": "boolean", "default": true },
    "include_taxonomies": { "type": "boolean", "default": true },
    "include_views": { "type": "boolean", "default": true }
  },
  "required": ["website_blueprint"]
}
```

**Returns**: Step-by-step Drupal assembly plan with ordered steps and dependencies

---

## Tool: generate_jsonapi_payloads

**Description**: Generate JSON:API payloads for publishing content to Drupal.

**Parameters**:
```json
{
  "type": "object",
  "properties": {
    "content_package": { "type": "object" },
    "drupal_base_url": { "type": "string" },
    "entity_order": {
      "type": "array",
      "items": { "type": "string" },
      "default": ["taxonomy_term", "media", "paragraph", "node"]
    }
  },
  "required": ["content_package"]
}
```

**Returns**: Ordered JSON:API payloads with endpoints, methods, and data

---

## Tool: generate_drupal_config_payloads

**Description**: Generate Drupal administrative API payloads for configuration entities.

**Parameters**:
```json
{
  "type": "object",
  "properties": {
    "drupal_plan": { "type": "object" },
    "drupal_base_url": { "type": "string" },
    "include_block_placement": { "type": "boolean", "default": true },
    "include_view_config": { "type": "boolean", "default": true },
    "include_permissions": { "type": "boolean", "default": false }
  },
  "required": ["drupal_plan"]
}
```

**Returns**: Configuration payloads for Drupal admin API

---

## Tool: validate_ux

**Description**: Validate assembled pages against UX quality gates.

**Parameters**:
```json
{
  "type": "object",
  "properties": {
    "page_spec": { "type": "object" },
    "check_hierarchy": { "type": "boolean", "default": true },
    "check_cta_visibility": { "type": "boolean", "default": true },
    "check_mobile_first": { "type": "boolean", "default": true }
  },
  "required": ["page_spec"]
}
```

**Returns**: UX validation report with pass/fail per gate

---

## Tool: validate_seo

**Description**: Validate content against SEO requirements.

**Parameters**:
```json
{
  "type": "object",
  "properties": {
    "content_package": { "type": "object" },
    "check_meta_title": { "type": "boolean", "default": true },
    "check_meta_description": { "type": "boolean", "default": true },
    "check_heading_structure": { "type": "boolean", "default": true },
    "check_alt_text": { "type": "boolean", "default": true }
  },
  "required": ["content_package"]
}
```

**Returns**: SEO validation report with per-page findings

---

## Tool: validate_performance

**Description**: Validate assembly against performance best practices.

**Parameters**:
```json
{
  "type": "object",
  "properties": {
    "website_blueprint": { "type": "object" },
    "check_unused_components": { "type": "boolean", "default": true },
    "check_image_optimization": { "type": "boolean", "default": true },
    "check_lazy_loading": { "type": "boolean", "default": true },
    "check_asset_aggregation": { "type": "boolean", "default": true }
  },
  "required": ["website_blueprint"]
}
```

**Returns**: Performance validation report with recommendations

---

## Tool: quality_gate_review

**Description**: Run all quality gates (UX, Accessibility, SEO, Performance) on the complete assembly.

**Parameters**:
```json
{
  "type": "object",
  "properties": {
    "website_blueprint": { "type": "object" },
    "content_package": { "type": "object" },
    "drupal_plan": { "type": "object" },
    "run_ux": { "type": "boolean", "default": true },
    "run_accessibility": { "type": "boolean", "default": true },
    "run_seo": { "type": "boolean", "default": true },
    "run_performance": { "type": "boolean", "default": true }
  },
  "required": ["website_blueprint"]
}
```

**Returns**: Complete quality gate report with all findings and overall pass/fail

---

## Tool: search_theme_library

**Description**: Browse and search the theme library for matching themes.

**Parameters**:
```json
{
  "type": "object",
  "properties": {
    "industry": { "type": "string" },
    "style": { "type": "string" },
    "components_needed": {
      "type": "array",
      "items": { "type": "string" }
    }
  }
}
```

**Returns**: Matching themes with metadata and component lists

---

## Tool: search_component_library

**Description**: Search the component library for components matching a purpose or input requirements.

**Parameters**:
```json
{
  "type": "object",
  "properties": {
    "purpose": { "type": "string" },
    "required_inputs": {
      "type": "array",
      "items": { "type": "string" }
    },
    "category": { "type": "string" }
  }
}
```

**Returns**: Matching components with input specifications and variants

---

## Tool: search_layout_library

**Description**: Search the layout library for page layout templates.

**Parameters**:
```json
{
  "type": "object",
  "properties": {
    "page_type": {
      "type": "string",
      "enum": ["homepage", "landing", "about", "services", "contact", "blog", "listing"]
    }
  }
}
```

**Returns**: Layout template with section structure and component placement

---

## Tool: publish_to_drupal

**Description**: Execute actual publication of JSON:API payloads to a live Drupal site.

**Parameters**:
```json
{
  "type": "object",
  "properties": {
    "drupal_base_url": { "type": "string" },
    "api_token": { "type": "string" },
    "payloads": {
      "type": "array",
      "items": { "type": "object" }
    },
    "batch_size": { "type": "integer", "default": 10 },
    "continue_on_error": { "type": "boolean", "default": false }
  },
  "required": ["drupal_base_url", "api_token", "payloads"]
}
```

**Returns**: Publication results with success/failure status per entity and created UUIDs

**Notes**: Requires Ollama for payload generation, then curl/php for actual API calls

---

## Tool: publish_to_drupal

**Description**: Generate the ordered publication sequence with dependencies and rollback plan.

**Parameters**:
```json
{
  "type": "object",
  "properties": {
    "drupal_plan": { "type": "object" },
    "publication_package": { "type": "object" },
    "include_rollback": { "type": "boolean", "default": true },
    "batch_size": { "type": "integer", "default": 10 }
  },
  "required": ["drupal_plan", "publication_package"]
}
```

**Returns**: Ordered publication sequence with dependency graph and rollback steps
