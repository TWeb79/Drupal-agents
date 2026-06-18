# Implementation Plan: Drupal Website Assembly Agent

## Phase 1: Requirement Analysis

### Step 1.1: Collect Business Requirements
- Use `analyze_requirements` with: business_type, industry, brand_style, target_audience, goals
- Output: `website_brief.json`

### Step 1.2: Validate Requirements
- Ensure all required fields are present
- Identify missing information
- Ask targeted questions if needed
- Output: `validated_brief.json`

## Phase 2: Information Architecture

### Step 2.1: Create Sitemap
- Use `create_sitemap` with the website brief
- Define: primary pages, utility pages (404, search), legal pages (privacy, terms)
- Output: `sitemap.json`

### Step 2.2: Define Navigation
- Primary navigation (max 7 items)
- Footer navigation (legal, utility, sitemap)
- Utility navigation (login, search, language)
- Output: `navigation.json`

### Step 2.3: URL Structure
- Define URL aliases for all pages
- Follow Drupal Pathauto patterns
- Output: `url_structure.json`

## Phase 3: Theme Selection

### Step 3.1: Search Theme Library
- Use `search_theme_library` with industry and style filters
- Review available themes and their component lists
- Output: `theme_candidates.json`

### Step 3.2: Select Theme
- Use `select_theme` with the website brief
- Require confidence score >= 70%
- Document matching rationale
- Output: `theme_selection.json`

### Step 3.3: Verify Component Availability
- Cross-reference required components against theme's available components
- Identify any gaps that need custom components
- Output: `component_gap_analysis.json`

## Phase 4: Component Selection

### Step 4.1: Select Components Per Page
For each page in the sitemap:
- Use `select_components` with page spec and theme ID
- Map each section to a component from the library
- Specify variant (light/dark/neutral/accent) per component
- Output: `component_mapping/{page_name}.json`

### Step 4.2: Verify Component Compatibility
- Ensure all selected components are available in the chosen theme
- Verify input requirements are met by available content
- Output: `compatibility_report.json`

### Step 4.3: Apply Layout Library
- Use `search_layout_library` for each page type
- Map layout sections to component selections
- Output: `layout_mapping/{page_name}.json`

## Phase 5: Content Generation

### Step 5.1: Generate Page Content
For each page:
- Use `generate_content` with page spec, component mapping, and website brief
- Generate: H1, H2s, body paragraphs, CTA text, image alt text
- Apply SEO optimization (meta titles, descriptions)
- Output: `content/{page_name}.json`

### Step 5.2: Generate Media Specifications
- Define image requirements per component
- Specify: dimensions, aspect ratio, alt text, lazy loading
- Output: `content/media_specifications.json`

### Step 5.3: Generate Taxonomy Terms
- Define terms for: categories, industries, tags
- Map terms to content nodes
- Output: `content/taxonomy_terms.json`

## Phase 6: Drupal Assembly Plan

### Step 6.1: Content Types
- Use `create_drupal_plan` with include_content_types
- Configure: Page, Article, Service, Product, Team Member, Case Study
- Define fields per content type
- Output: `drupal/config/content_types.yml`

### Step 6.2: Paragraph Bundles
- Map component selections to Paragraph bundle configurations
- Define field configuration per bundle
- Configure form display and view display
- Output: `drupal/config/paragraphs.yml`

### Step 6.3: Layout Builder Configuration
- Use `create_drupal_plan` with include_layout_builder
- Define section types and block restrictions
- Configure per-content-type Layout Builder settings
- Output: `drupal/config/layout_builder.yml`

### Step 6.4: Menu Structure
- Configure: main-menu, footer-menu, utilities-menu
- Define menu link hierarchy matching sitemap
- Output: `drupal/config/menus.yml`

### Step 6.5: Taxonomy Configuration
- Configure vocabularies: categories, industries, tags
- Define field references on content types
- Output: `drupal/config/taxonomies.yml`

### Step 6.6: View Configuration
- Configure views for: blog listing, service listing, team grid
- Define: filters, sorting, pagination, exposed filters
- Output: `drupal/config/views.yml`

### Step 6.7: Block Placements
- Place blocks per region per content type
- Configure visibility conditions
- Output: `drupal/config/blocks.yml`

### Step 6.8: Assembly Sequence
- Use `create_drupal_plan` to generate ordered steps
- Ensure dependency order: config → content types → paragraphs → nodes
- Output: `drupal/assembly_sequence.json`

## Phase 7: Publication

### Step 7.1: Generate JSON:API Payloads
- Use `generate_jsonapi_payloads` with content package
- Order: taxonomy_term → media → paragraph → node
- Include authentication headers specification
- Output: `publication/jsonapi_payloads.json`

### Step 7.2: Generate Drupal Config Payloads
- Use `generate_drupal_config_payloads` with Drupal plan
- Include: block placement, view config, permissions
- Output: `publication/drupal_config_payloads.json`

### Step 7.3: Publication Sequence
- Use `generate_publication_sequence`
- Define ordered batches with dependencies
- Include rollback plan per step
- Output: `publication/publication_sequence.json`

### Step 7.4: Execute Publication (Optional)
- Use `publish_to_drupal` if `drupal_base_url` and `api_token` are provided
- Execute payloads in ordered batches
- Handle authentication and rate limiting
- Output: `publication/publication_results.json`

### Step 7.5: Publication Verification
- Define verification steps per publication batch
- Include: entity existence checks, field value checks, URL alias checks
- Output: `publication/verification_plan.json`

## Phase 8: Quality Assurance

### Step 8.1: UX Validation
- Use `validate_ux` for each page
- Check: visual hierarchy, CTA visibility, mobile-first
- Output: `quality/ux_report.md`

### Step 8.2: SEO Validation
- Use `validate_seo` with content package
- Check: meta titles, descriptions, heading structure, alt text
- Output: `quality/seo_report.md`

### Step 8.3: Accessibility Validation
- Verify all components meet WCAG AA
- Check: alt text, keyboard navigation, semantic HTML
- Output: `quality/accessibility_report.md`

### Step 8.4: Performance Validation
- Use `validate_performance` with website blueprint
- Check: unused components, image optimization, lazy loading
- Output: `quality/performance_report.md`

### Step 8.5: Full Quality Review
- Use `quality_gate_review` for comprehensive assessment
- All gates must pass before publication
- Output: `quality/full_review_report.md`

## Drupal JSON:API Publication Pattern

### Authentication
```bash
# Use Drupal user with content management permissions
curl -X POST \
  -H "Content-Type: application/vnd.api+json" \
  -H "Authorization: Bearer ${DRUPAL_API_TOKEN}" \
  ${DRUPAL_BASE_URL}/jsonapi/node/page \
  -d @payload.json
```

### Entity Creation Order
1. Taxonomy terms (categories, industries, tags)
2. Media entities (images, files)
3. Paragraph entities (components)
4. Node entities (pages, articles, etc.)

### Drupal JSON:API Payload Examples

### Taxonomy Term
```json
{
  "data": {
    "type": "taxonomy_term--tags",
    "attributes": {
      "name": "Customer Success"
    }
  }
}
```

### Media Entity (requires file upload first)
```json
{
  "data": {
    "type": "media--image",
    "attributes": {
      "field_media_image": null,
      "name": "Hero background image"
    }
  }
}
```

### Paragraph Bundle
```json
{
  "data": {
    "type": "paragraph--hero_split",
    "attributes": {
      "field_headline": "Transform Your Digital Presence",
      "field_subheadline": "Professional Drupal solutions for growing businesses",
      "field_cta_text": "Get Started",
      "field_cta_url": "/contact"
    }
  }
}
```

### Node with Paragraph Reference
```json
{
  "data": {
    "type": "node--page",
    "attributes": {
      "title": "Home",
      "body": {"value": "<p>Welcome to our platform</p>", "format": "basic_html"},
      "field_meta_title": "Home - Professional Drupal Solutions",
      "field_meta_description": "Transform your digital presence with our expert Drupal development services",
      "path": {"alias": "/"}
    },
    "relationships": {
      "field_components": {
        "data": [
          {"type": "paragraph--hero_split", "id": "NEW_ENTITY"},
          {"type": "paragraph--feature_grid", "id": "NEW_ENTITY"}
        ]
      }
    }
  }
}
```

### Menu Link
```json
{
  "data": {
    "type": "menu_link_content--menu_link_content",
    "attributes": {
      "title": "Services",
      "url": "/services",
      "weight": 2
    }
  }
}
```

## Publication Commands

```bash
# Verify Ollama endpoint
curl -s http://localhost:11434/api/tags | jq '.models[].name' | grep qwen3.5

# Test Drupal API (requires authentication)
curl -s -H "Authorization: Bearer $TOKEN" \
  "$DRUPAL_URL/jsonapi/node/page" | jq '.data[0].attributes.title'
```

## Error Handling
- Retry with exponential backoff on 429/503
- Log all 400 errors with full request context
- Stop publication on validation errors (fix before retry)
- Continue on non-critical warnings

## Multi-Site Generation Support

For white-label or multi-site scenarios:
- Parameterize: theme, content, taxonomy
- Support per-site content overrides
- Maintain shared component library reference
- Generate separate publication packages per site
