# Drupal AI Agents

AI agents for designing, developing, and assembling Drupal websites. Powered by Ollama (`qwen3.5:9b`).

## Quick Start

```bash
# List available agents
./agent-exe list

# Run an agent interactively
./agent-exe run design

# Run with a single goal
./agent-exe run design --goal "Create a healthcare theme with WCAG AA compliance"
./agent-exe run component --goal "Build a pricing table component"
./agent-exe run assembly --goal "Assemble a SaaS startup website"

# Publish directly to Drupal (requires JSON:API access)
./agent-exe run assembly --publish --drupal-url "https://example.com" --api-token "TOKEN" --goal "Build my site"
```

## Agent Types

| Agent | Purpose |
|-------|---------|
| `design` | Design systems, themes, and Twig templates |
| `component` | Reusable Drupal components and Paragraph bundles |
| `assembly` | Assemble complete websites via JSON:API |

## Architecture

### Why Agents Are Markdown Files

Agents are defined as markdown (`agent.md`, `system_prompt.md`, `tools.md`, `implementation_plan.md`) because:

1. **Human-readable contracts** - Developers can read and modify agent behavior without code
2. **Version control friendly** - Plain text diff and merge
3. **Separation of concerns** - System prompts, tools, and plans are independently maintainable
4. **Framework agnostic** - The same agent definition works with any LLM provider

### How It Works

```
┌─────────────────┐
│   agent-exe     │  CLI launcher (Python)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   system_prompt │  LLM instructions (readable plan)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│     Ollama      │  Local LLM (qwen3.5:9b)
│   (port 11434)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   tools.md      │  Tool definitions (JSON schema)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  implementation │  Output artifacts (JSON, Twig, config)
│     plan.md     │
└─────────────────┘
```

### API Calls

The `agent-exe` CLI handles three types of API interactions:

#### 1. Ollama API (Local LLM)

```python
# POST http://localhost:11434/api/generate
{
  "model": "qwen3.5:9b",
  "system": "...system prompt...",
  "prompt": "...user request...",
  "stream": false
}
```

#### 2. Drupal JSON:API (Content Publication)

When `--publish` flag is used:

```bash
# POST https://drupal-site/jsonapi/node/page
-H "Content-Type: application/vnd.api+json"
-H "Authorization: Bearer TOKEN"
-d '{"data":{"type":"node--page",...}}'
```

#### 3. Drupal Admin API (Configuration)

For configuration entities (menus, views, paragraphs):

```bash
# POST https://drupal-site/admin/config
-H "Content-Type: application/json"
-H "Authorization: Bearer TOKEN"
```

## Agent Structure

Each agent folder contains:

```
agent_*/
├── agent.md              # Agent identity, config, state schema
├── system_prompt.md      # LLM instructions (role, workflow, rules)
├── tools.md              # Tool catalog with JSON parameters
└── implementation_plan.md # Drupal-specific implementation steps
```

### agent.md
- Agent ID and version
- LLM provider/model configuration
- State schema (TypeScript interfaces)
- Working principles and constraints

### system_prompt.md
- Role definition
- Workflow steps
- Response format (JSON with thinking/action/justification)
- Quality gates

### tools.md
- Tool name and description
- JSON parameters schema
- Return format
- Drupal-specific notes

### implementation_plan.md
- Phase-by-phase execution plan
- Drupal file structure
- YAML config examples
- API payloads

## Output

Agents generate artifacts in `output/`:

```
output/
├── {agent}_{goal}.json     # Raw LLM response
├── website_brief.json        # Requirements analysis
├── sitemap.json              # Information architecture
├── theme_selection.json      # Selected theme with confidence score
├── component_mapping/        # Per-page component selections
├── content/                  # Generated content and media specs
├── drupal/config/            # Drupal configuration (YAML)
├── publication/              # JSON:API payloads
└── quality/                  # Validation reports
```

## Requirements

- Python 3.8+
- Ollama with `qwen3.5:9b` model
- Drupal 9/10/11 site with JSON:API enabled (for publication)

## Configuration

Environment variables (optional):

```bash
export OLLAMA_URL="http://localhost:11434"
export OLLAMA_MODEL="qwen3.5:9b"
export DRUPAL_BASE_URL="https://example.com"
export DRUPAL_API_TOKEN="your-token"
```

Or pass via CLI:

```bash
./agent-exe run design --ollama-url "http://localhost:11434" --model "qwen3.5:9b"
```

## Development

To add a new agent:

1. Create `agent_xxx/` folder
2. Copy structure from existing agent
3. Define `agent.md` with identity and config
4. Write `system_prompt.md` with workflow
5. Add tools to `tools.md`
6. Create `implementation_plan.md` with Drupal steps
7. Register in `agent-exe` under `AGENTS` dict

## License

MIT - Inventions4All - github:TWeb79# Drupal-agents
