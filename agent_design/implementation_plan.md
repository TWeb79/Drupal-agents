# Implementation Plan: Drupal Theme Design Agent

## Phase 1: Discovery & Requirements Gathering

### Step 1.1: Business Context Collection
- Use `gather_requirements` with category `business`
- Capture: company name, industry, target audience, geographic market, brand personality, business goals
- Output: `business_context.json`

### Step 1.2: Content Strategy Collection
- Use `gather_requirements` with category `content`
- Capture: content types, taxonomies, media strategy, editorial workflows
- Output: `content_strategy.json`

### Step 1.3: Design Preferences Collection
- Use `gather_requirements` with category `design`
- Capture: branding, logo, colors, typography, competitors, style direction
- Output: `design_preferences.json`

### Step 1.4: Technical Constraints Collection
- Use `gather_requirements` with category `technical`
- Capture: Drupal version, hosting, performance, multilingual, accessibility
- Output: `technical_constraints.json`

## Phase 2: Design System Creation

### Step 2.1: Color System
- Use `create_design_system` with brand colors and industry
- Generate: primary, secondary, neutral, semantic color tokens
- Ensure WCAG 2.2 AA contrast ratios (4.5:1 text, 3:1 large text)
- Output: `design_system/colors.json`

### Step 2.2: Typography Scale
- Define heading hierarchy (h1-h6), body, caption, overline
- Specify font families, weights, line heights, letter spacing
- Map to Drupal font settings and CSS custom properties
- Output: `design_system/typography.json`

### Step 2.3: Spacing & Grid
- Define 8px base spacing scale (4, 8, 12, 16, 24, 32, 48, 64, 96, 128)
- Define 12-column responsive grid with gutter widths
- Output: `design_system/spacing.json`, `design_system/grid.json`

### Step 2.4: Breakpoints
- Define: mobile (320px), tablet (768px), desktop (1024px), wide (1440px)
- Map to Drupal breakpoint configuration
- Output: `design_system/breakpoints.json`

## Phase 3: Theme Architecture

### Step 3.1: Base Theme Selection
- Use `define_theme_architecture`
- Evaluate: Classy (content), Stable (minimal), Olivero (modern frontend)
- Decision criteria: project complexity, team expertise, customization needs
- Output: `theme/architecture.json`

### Step 3.2: File Structure
```
THEME_NAME/
├── THEME_NAME.info.yml
├── THEME_NAME.libraries.yml
├── THEME_NAME.theme
├── config/
│   ├── install/
│   └── schema/
├── css/
│   ├── base/
│   ├── components/
│   ├── layout/
│   └── utilities/
├── js/
│   ├── components/
│   └── utilities/
├── templates/
│   ├── block/
│   ├── content/
│   ├── field/
│   ├── layout/
│   ├── node/
│   ├── page/
│   ├── region/
│   └── views/
├── images/
└── fonts/
```

### Step 3.3: Library Definitions
- Use `generate_libraries_yml`
- Define global (base CSS/JS) and per-component libraries
- Output: `THEME_NAME.libraries.yml`

### Step 3.4: Layout Strategy
- Use `define_layout_strategy`
- Configure Layout Builder sections, block restrictions, editor permissions
- Output: `theme/layout_strategy.json`

## Phase 4: Component Design

### Step 4.1: Core Components
For each component (header, footer, navigation, hero, card, teaser, article, form, search, CTA, gallery):
- Use `design_component`
- Generate Twig template with `generate_twig_template`
- Define CSS architecture (BEM naming)
- Document accessibility requirements
- Output: `components/{component_name}/`

### Step 4.2: Template Suggestions
- Define template naming conventions:
  - `node--{type}--{view-mode}.html.twig`
  - `block--{module}--{delta}.html.twig`
  - `field--{entity}--{field-name}.html.twig`
- Output: `templates/` directory structure

## Phase 5: Quality Assurance

### Step 5.1: Accessibility Audit
- Use `audit_accessibility` on each component and the full theme
- Check: color contrast, keyboard navigation, ARIA labels, semantic HTML
- Output: `audits/accessibility_report.md`

### Step 5.2: Performance Audit
- Use `audit_performance` on theme architecture
- Check: critical CSS, image strategy, JS budget, cache strategy
- Output: `audits/performance_report.md`

### Step 5.3: Theme Review
- Use `review_theme_spec` for comprehensive review
- Check: coding standards, security, scalability, editor experience
- Output: `audits/theme_review.md`

## Phase 6: Documentation

### Step 6.1: Theme README
- Document: theme purpose, file structure, design tokens, component list
- Include: setup instructions, build commands, deployment notes

### Step 6.2: Component Documentation
- For each component: purpose, usage, variants, accessibility notes
- Include: Twig template reference, CSS class documentation

### Step 6.3: Editor Guide
- Document: Layout Builder usage, Paragraph bundle usage
- Include: content governance rules, allowed configurations

## Drupal 11 Specific Considerations

### Required Modules (Core)
- Block, Layout Builder, Breakpoint, Responsive Image
- Media, Media Library, CKEditor 5
- Taxonomy, Pathauto (contrib but standard)

### Theme Hooks
- `hook_theme_suggestions_alter()` for custom template suggestions
- `hook_preprocess_HOOK()` for template variable manipulation
- `hook_library_info_alter()` for asset management

### Asset Loading
- Use Drupal's asset library system (not direct `<link>`/`<script>`)
- Leverage `drupalSettings` for passing PHP variables to JS
- Use `#attached` render array property for per-element assets

### Caching Strategy
- Define cache tags for all rendered entities
- Use cache contexts for per-user/per-role variations
- Implement lazy loading for below-fold content
