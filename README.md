# Drupal AI Agents

AI agents for designing, developing, and assembling Drupal websites. Powered by Ollama (`qwen3.5:9b`) or NVIDIA (`openai/gpt-oss-20b`).

## Quick Start

```bash
# List available agents
./agent-exe list

# List LLM providers
./agent-exe models

# Run an agent interactively (default: ollama)
./agent-exe run design

# Run with NVIDIA provider
./agent-exe run --llm nvidia design

# Run with a single goal
./agent-exe run design --goal "Create a healthcare theme with WCAG AA compliance"
./agent-exe run component --goal "Build a pricing table component"
./agent-exe run assembly --goal "Assemble a SaaS startup website"

# Publish to Drupal (token auth)
./agent-exe run assembly --publish --drupal-url "https://example.com" --api-token "TOKEN" --goal "Build my site"

# Publish to Drupal (basic auth)
./agent-exe run assembly --publish --drupal-url "https://example.com" --username "admin" --password "secret" --goal "Build my site"
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
│ LLM Provider    │  Ollama (local) or NVIDIA (cloud)
│ (--llm flag)    │
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

The `agent-exe` CLI handles API interactions:

#### 1. LLM API (Ollama or NVIDIA)

**Ollama (local):**
```python
# POST http://localhost:11434/api/generate
{
  "model": "qwen3.5:9b",
  "system": "...system prompt...",
  "prompt": "...user request...",
  "stream": false
}
```

**NVIDIA (cloud):**
```python
# POST https://integrate.api.nvidia.com/v1/chat/completions
{
  "model": "openai/gpt-oss-20b",
  "messages": [
    {"role": "system", "content": "...system prompt..."},
    {"role": "user", "content": "...user request..."}
  ],
  "max_tokens": 8192
}
```

Use `--llm nvidia` to select NVIDIA provider.

#### 2. Drupal JSON:API (Content Publication)

When `--publish` flag is used, agents can return payloads that are executed against Drupal:

```bash
# POST https://drupal-site/jsonapi/node/page
-H "Content-Type: application/vnd.api+json"
-H "Authorization: Bearer TOKEN"  # or Basic auth
-d '{"data":{"type":"node--page",...}}'
```

## Agent API Call Process

### How Agents Call External APIs

Agents receive prompts and return structured JSON responses. When an agent needs to publish content to Drupal, it includes a special `action` field:

```json
{
  "thinking": "Design complete, now publishing the theme.",
  "phase": "publication",
  "action": "publish_to_drupal",
  "parameters": {
    "payloads": [
      {
        "endpoint": "/jsonapi/node/page",
        "data": {"data": {"type": "node--page", "attributes": {"title": "..."}}}
      }
    ]
  }
}
```

The `agent-exe` CLI detects this action and executes the payloads via HTTP POST to your Drupal site.

### Complete Example: Task to API Call

**1. User Task:**
```bash
./agent-exe run --llm nvidia design --goal "Create homepage for luxury fashion brand"
```

**2. CLI Builds Prompt (from `system_prompt.md`):**
```
You are a senior Drupal Frontend Architect...
User: Create homepage for luxury fashion brand
Assistant:
```

**3. LLM Response (JSON):**
```json
{
  "thinking": "Creating homepage with hero banner, product grid, and brand story section.",
  "phase": "design",
  "action": "publish_to_drupal",
  "parameters": {
    "payloads": [
      {
        "endpoint": "/jsonapi/node/page",
        "data": {
          "data": {
            "type": "node--page",
            "attributes": {
              "title": "Home",
              "body": {"value": "<h1>Welcome to Luxury Brand</h1>..."}
            }
          }
        }
      }
    ]
  },
  "output": {
    "deliverable_type": "theme_design",
    "content": "Black and gold luxury theme with responsive grid layout."
  }
}
```

**4. CLI Executes API Call (Python function):**
```python
def publish_to_drupal(drupal_url, api_token, payloads):
    headers = {
        "Content-Type": "application/vnd.api+json",
        "Authorization": f"Bearer {api_token}",
    }
    for payload in payloads:
        url = f"{drupal_url}{payload['endpoint']}"
        data = json.dumps(payload["data"]).encode("utf-8")
        req = urllib.request.Request(
            url, data=data, headers=headers, method="POST"
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            print(f"Published: {resp.read()}")
```

**5. Result:**
- Page created in Drupal at `/jsonapi/node/page`
- Output saved to `output/design_Create_homepage_for_luxury_fashion_brand.json`

### Authentication Flow

1. **LLM Provider Selection**: `--llm ollama` (default) or `--llm nvidia`
2. **Drupal Authentication**: Choose one method
   - **Token**: `--api-token TOKEN` (recommended for production)
   - **Basic Auth**: `--username admin --password secret` (development)
   - **Environment**: Variables loaded from `.env` file automatically

### Processing Steps

1. User runs `./agent-exe run design --goal "Create theme"`
2. CLI loads `system_prompt.md` from `agent_design/`
3. CLI sends request to selected LLM provider (Ollama or NVIDIA)
4. LLM responds with JSON containing `action`, `thinking`, `output`
5. CLI saves response to `output/design_*.json`
6. If `action: publish_to_drupal`, CLI executes payloads against Drupal

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

## Configuration

### Environment File (Recommended)

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
# Edit .env with your credentials
```

### Environment Variables

```bash
export NVIDIA_API_KEY="nvapi-your-key"     # For NVIDIA provider
export DRUPAL_BASE_URL="https://example.com"
export DRUPAL_API_TOKEN="your-token"     # Bearer token auth
# OR
export DRUPAL_USERNAME="admin"           # Basic auth
export DRUPAL_PASSWORD="secret"
```

Or pass via CLI:

```bash
./agent-exe run --llm nvidia design -g "Create theme"
./agent-exe run --publish --drupal-url "https://site.com" --username admin --password secret --goal "Build site"
```

## Requirements

- Python 3.8+
- **Ollama** with `qwen3.5:9b` model (for local LLM) OR **NVIDIA API key** (for cloud LLM)
- Drupal 9/10/11 site with JSON:API enabled (for publication)

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
