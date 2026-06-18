# Implementation Plan: Drupal Component Development Agent

## Phase 1: Requirement Analysis

### Step 1.1: Receive Component Request
- Parse the input: goal, business problem, expected outcome
- Identify the component category (hero, content, conversion, trust, navigation, media)
- Output: `component_request.json`

### Step 1.2: Requirement Validation
- Validate that the request is within scope (component, not full website)
- Identify missing information
- Ask targeted questions if needed
- Output: `validated_requirement.json`

## Phase 2: Component Discovery

### Step 2.1: Library Search
- Use `search_component_library` to find existing matches
- Search by: category, purpose, keyword
- Include variant search
- Output: `discovery_results.json`

### Step 2.2: Reuse Decision
Based on search results:
- **Exact match found**: Return existing component with usage instructions
- **Partial match found**: Extend existing component or create variant
- **No match found**: Proceed to new component creation
- Output: `reuse_decision.json`

## Phase 3: Component Specification

### Step 3.1: Create Specification
- Use `create_component_spec`
- Define: name, category, purpose, variants
- Define visual variants (light, dark, neutral, accent)
- Define layout variants (left, center, right, split)
- Output: `component_spec.json`

### Step 3.2: Define Data Model
- Use `define_data_model`
- For each field: name, type, required, description, cardinality
- Map field types to Drupal field types
- Output: `data_model.json`

### Step 3.3: UX Design Specification
- Define layout structure (grid, flex, container queries)
- Define visual hierarchy (reading order, focal points)
- Define interactions (hover states, click targets, animations)
- Define mobile behavior (stacking order, content priority)
- Output: `ux_design.json`

## Phase 4: Drupal Mapping

### Step 4.1: Paragraph Type Definition
- Use `map_to_drupal`
- Generate Paragraph bundle configuration
- Map data model fields to Drupal fields
- Define display modes (default, teaser, full)
- Output: `drupal_schema/paragraph_type.yml`

### Step 4.2: Field Configuration
For each field in the data model:
- Generate field storage config (base_field_override)
- Generate field instance config (required, cardinality, widget)
- Generate form display config (widget type, settings)
- Generate view display config (formatter, settings)
- Output: `drupal_schema/fields/{field_name}.yml`

### Step 4.3: Layout Builder Integration
- Define Layout Builder section for the component
- Map component fields to Layout Builder block fields
- Configure block restrictions and allowed blocks
- Output: `drupal_schema/layout_builder.yml`

## Phase 5: Implementation

### Step 5.1: Twig Template
- Use `generate_twig_component`
- Template naming: `paragraph--{bundle}--{variant}.html.twig`
- Include variant handling with CSS class toggles
- Include ARIA attributes and semantic markup
- Use design tokens for all visual properties
- Output: `templates/paragraph/{component_name}.html.twig`

### Step 5.2: CSS Architecture
- Use `generate_component_css`
- BEM naming: `.component-name__element--modifier`
- CSS custom properties for all design tokens
- Responsive rules per breakpoint
- Container query support where appropriate
- Output: `css/components/{component_name}.css`

### Step 5.3: JavaScript Behavior
- Use `generate_component_js`
- Progressive enhancement approach
- Event delegation for dynamic content
- Keyboard interaction support
- Reduced motion preference respect
- Output: `js/components/{component_name}.js`

### Step 5.4: Theme Mapping
- Use `generate_theme_mapping`
- Map all visual properties to design system tokens
- Ensure no hardcoded values
- Output: `theme_mapping/{component_name}.json`

## Phase 6: Quality Assurance

### Step 6.1: Accessibility Validation
- Use `validate_accessibility`
- Check: contrast, keyboard, screen reader, semantic HTML, focus management
- Remediate any failures
- Output: `quality/accessibility_report.md`

### Step 6.2: Responsiveness Validation
- Use `validate_responsiveness`
- Test at: 320px, 768px, 1024px, 1440px
- Verify content hierarchy is maintained
- Output: `quality/responsiveness_report.md`

### Step 6.3: Design System Compliance
- Verify all visual values use design tokens
- Verify no hardcoded colors, fonts, or spacing
- Verify variant strategy is complete
- Output: `quality/design_system_report.md`

### Step 6.4: Reusability Validation
- Verify component name is industry-neutral
- Verify data model is generic enough for cross-industry use
- Verify no business-specific logic in templates
- Output: `quality/reusability_report.md`

### Step 6.5: Full Quality Review
- Use `quality_review` for comprehensive assessment
- All gates must pass before component is approved
- Output: `quality/full_review_report.md`

## Phase 7: Documentation

### Step 7.1: Component Documentation
- Use `generate_documentation`
- Include: purpose, use cases, field descriptions, configuration options
- Include accessibility notes and ARIA patterns
- Include Drupal configuration instructions
- Output: `docs/{component_name}.md`

### Step 7.2: Usage Examples
- Use `generate_usage_examples`
- Generate examples for: homepage, landing page, inner page
- Generate examples for: technology, healthcare, finance industries
- Output: `docs/{component_name}_examples.md`

### Step 7.3: Developer Guide
- Document: file structure, template hierarchy, CSS class reference
- Include: how to add new variants, how to extend the component
- Output: `docs/{component_name}_developer_guide.md`

## Phase 8: Library Registration

### Step 8.1: Register Component
- Add component to the component library index
- Update category listings
- Update variant registry
- Output: `library/component_index.json` (updated)

### Step 8.2: Update Assembly Agent Catalog
- Notify the Website Assembly Agent of the new component
- Provide: component spec, usage examples, configuration guide
- Output: `library/assembly_catalog.json` (updated)

## Drupal 11 Specific Implementation Notes

### Paragraph Bundle Structure
```
config/
  install/
    paragraphs_type.{bundle_name}.yml
    field.field.paragraph.{bundle_name}.{field_name}.yml
    core.entity_form_display.paragraph.{bundle_name}.default.yml
    core.entity_view_display.paragraph.{bundle_name}.default.yml
```

### Twig Template Hierarchy
```
templates/
  paragraph/
    paragraph--{bundle}--default.html.twig
    paragraph--{bundle}--{variant}.html.twig
  field/
    field--paragraph--{field_name}--{bundle}.html.twig
```

### Library Registration
```yaml
# {component_name}.libraries.yml
{css_name}:
  css:
    component:
      css/components/{component_name}.css: {}
  js:
    js/components/{component_name}.js: {}
  dependencies:
    - core/drupal
    - core/once
```

### Design Token Integration
```css
/* Component CSS uses only tokens */
.{component_name} {
  color: var(--color-text-primary);
  background: var(--color-bg-{variant});
  padding: var(--space-md);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
  font-family: var(--font-body);
}
```
