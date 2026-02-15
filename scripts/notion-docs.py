"""Build Notion documentation for Dual AI Chat project."""
import json
import os
import time
import urllib.request

TOKEN = os.environ.get("NOTION_TOKEN", "")
PARENT = "3086efb9-58c3-8036-a0a2-f772f5e59158"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}

def api(method, url, body=None):
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, headers=HEADERS, method=method)
    time.sleep(0.35)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())

def create_page(parent_id, title, icon, children):
    body = {
        "parent": {"page_id": parent_id},
        "icon": {"type": "emoji", "emoji": icon},
        "properties": {"title": [{"text": {"content": title}}]},
        "children": children[:100],  # API limit
    }
    r = api("POST", "https://api.notion.com/v1/pages", body)
    pid = r["id"]
    print(f"  Created: {title} ({pid})")
    # If more than 100 blocks, append the rest
    if len(children) > 100:
        append_blocks(pid, children[100:])
    return pid

def append_blocks(page_id, blocks):
    api("PATCH", f"https://api.notion.com/v1/blocks/{page_id}/children", {"children": blocks})

# -- Block helpers --
def rt(text, bold=False):
    r = {"type": "text", "text": {"content": text}}
    if bold:
        r["annotations"] = {"bold": True}
    return r

def h1(t): return {"object": "block", "type": "heading_1", "heading_1": {"rich_text": [rt(t)]}}
def h2(t): return {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [rt(t)]}}
def h3(t): return {"object": "block", "type": "heading_3", "heading_3": {"rich_text": [rt(t)]}}
def p(t): return {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [rt(t)]}}
def p_bold(b, t): return {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [rt(b, True), rt(t)]}}
def bullet(t): return {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [rt(t)]}}
def bullet_bold(b, t): return {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [rt(b, True), rt(t)]}}
def num(t): return {"object": "block", "type": "numbered_list_item", "numbered_list_item": {"rich_text": [rt(t)]}}
def divider(): return {"object": "block", "type": "divider", "divider": {}}
def callout(t, icon): return {"object": "block", "type": "callout", "callout": {"rich_text": [rt(t)], "icon": {"type": "emoji", "emoji": icon}}}
def code(t, lang="plain text"): return {"object": "block", "type": "code", "code": {"rich_text": [rt(t)], "language": lang}}
def quote(t): return {"object": "block", "type": "quote", "quote": {"rich_text": [rt(t)]}}

# ============================================================
print("Adding intro to main page...")
append_blocks(PARENT, [
    callout("Enterprise-grade side-by-side AI comparison platform powered by Azure OpenAI (GPT-4o) and Azure AI Foundry (DeepSeek-R1).", "\U0001F680"),
    divider(),
    h2("Project Status"),
    p_bold("Current Phase: ", "Phase 1 \u2014 Foundation & Core Features (COMPLETED)"),
    p_bold("Next Phase: ", "Phase 2 \u2014 Advanced Features & Production Hardening"),
    divider(),
    h2("Quick Navigation"),
    p("Browse the subpages below for detailed documentation on every aspect of the project."),
    divider(),
])

# ============================================================
print("\n1/8 Phase 1...")
create_page(PARENT, "Phase 1 \u2014 What We Built", "\u2705", [
    callout("Phase 1 is the foundation layer. Everything built here establishes the core architecture, UI/UX, and AI integrations that all future phases build upon.", "\U0001F4CB"),
    divider(),
    h2("Summary"),
    p("Phase 1 covered the complete build-out of a dual-AI chat platform from scratch, including backend API development, frontend UI, Azure AI integrations, enterprise project structure, and DevOps tooling."),
    divider(),
    h2("1. Backend API (FastAPI)"),
    bullet("Built a Python FastAPI backend with versioned REST API endpoints (/api/v1/)"),
    bullet("Integrated Azure OpenAI SDK (AsyncAzureOpenAI) for GPT-4o-mini completions"),
    bullet("Integrated Azure AI Foundry SDK (AsyncOpenAI) for DeepSeek-R1 reasoning model"),
    bullet("Implemented Server-Sent Events (SSE) streaming for real-time token-by-token responses"),
    bullet("Added Pydantic-settings for type-safe environment configuration from .env"),
    bullet("Built centralized logging with structured output and request/response middleware"),
    bullet("Added global exception handler to prevent credential leakage in error responses"),
    bullet("Created health check endpoint reporting model availability status"),
    divider(),
    h2("2. Frontend UI (React + TypeScript)"),
    bullet("Built a React 18 SPA with TypeScript and Vite for fast development"),
    bullet("Designed an Abacus AI-inspired dark/light theme with professional typography (Inter font)"),
    bullet("Implemented side-by-side dual chat panels comparing GPT-4o and DeepSeek-R1 simultaneously"),
    bullet("Added collapsible sidebar with chat history, new conversation, and settings"),
    bullet("Built real-time streaming message display with markdown rendering and syntax highlighting"),
    bullet("Added model selection pills (Dual View / GPT-4o only / DeepSeek-R1 only)"),
    bullet("Implemented copy-to-clipboard, retry failed messages, thumbs up/down feedback"),
    bullet("Added backend health monitoring with offline banner"),
    bullet("Built multi-line input with Shift+Enter support and auto-resize"),
    bullet("Added suggested prompts for empty state and smooth scroll-to-bottom"),
    divider(),
    h2("3. Enterprise Project Structure"),
    bullet("Migrated to monorepo pattern with apps/ and packages/ directories"),
    bullet("Added npm workspaces for shared package management"),
    bullet("Created @dualai/shared-types package for TypeScript API contracts"),
    bullet("Created @dualai/typescript-config for shared compiler settings"),
    bullet("Added Turborepo config (turbo.json) for build pipeline orchestration"),
    bullet("Organized frontend with feature-based component grouping (chat/, layout/, ui/)"),
    bullet("Added barrel exports (index.ts) for clean imports"),
    bullet("Added __init__.py to every Python package for proper packaging"),
    divider(),
    h2("4. DevOps & Infrastructure"),
    bullet("Multi-stage Dockerfiles for both backend (Python) and frontend (Nginx)"),
    bullet("docker-compose.yml for one-command production deployment"),
    bullet("GitHub Actions CI pipeline (backend tests + frontend lint/build)"),
    bullet("Makefile with common developer commands"),
    bullet("Comprehensive .gitignore and .dockerignore"),
    bullet(".env.example template (no secrets committed)"),
    divider(),
    h2("5. Testing Foundation"),
    bullet("pytest setup with conftest.py and shared fixtures"),
    bullet("Test skeletons for API endpoints (health, chat validation)"),
    bullet("Test skeletons for service layer (LLM service instantiation)"),
    divider(),
    h2("6. Bug Fixes & Troubleshooting"),
    bullet("Fixed CORS blocking frontend-backend communication (405 on OPTIONS)"),
    bullet("Fixed Pydantic-settings JSON parsing for BACKEND_CORS_ORIGINS"),
    bullet("Fixed light mode contrast issues (low-opacity text unreadable on white)"),
    bullet("Fixed sidebar delete button overlapping chat history titles"),
    bullet("Fixed CSS @import order warnings in Vite"),
    bullet("Fixed PowerShell command syntax compatibility"),
])

# ============================================================
print("2/8 Tech Stack...")
tech_id = create_page(PARENT, "Tech Stack & Tools Reference", "\U0001F6E0", [
    callout("Complete reference of every technology, library, and tool used in the project with its specific purpose.", "\U0001F4DA"),
    divider(),
    h2("Backend Technologies"),
    divider(),
    h3("Python 3.12"),
    p("The core runtime for the backend. Chosen for its async/await support, rich AI/ML ecosystem, and strong typing with type hints."),
    h3("FastAPI"),
    p("Modern, high-performance Python web framework. Purpose: Serves the REST API endpoints, handles request validation via Pydantic, provides automatic OpenAPI documentation, and supports async request handling for non-blocking AI API calls."),
    h3("Uvicorn"),
    p("ASGI server that runs FastAPI in production. Purpose: Serves the application with async support, hot-reload in development, and multi-worker capability for production."),
    h3("OpenAI Python SDK (openai >= 1.50)"),
    p("Official SDK for OpenAI-compatible APIs. Purpose: Provides AsyncAzureOpenAI client for GPT-4o-mini and AsyncOpenAI client for DeepSeek-R1. Handles authentication, streaming, retries, and error handling."),
    h3("Pydantic & Pydantic-Settings"),
    p("Data validation and settings management. Purpose: Pydantic validates all API request/response schemas. Pydantic-Settings loads and validates environment variables from .env files with type coercion."),
    h3("python-dotenv"),
    p("Environment variable loader. Purpose: Reads the root .env file and injects variables into the process environment."),
    h3("pytest"),
    p("Testing framework. Purpose: Runs backend unit and integration tests with fixtures, parametrize, and async support."),
    h3("httpx"),
    p("Async HTTP client. Purpose: Used by FastAPI TestClient for integration testing and as dependency for the OpenAI SDK."),
    h3("flake8"),
    p("Python linter. Purpose: Enforces code style consistency (PEP 8) across the backend codebase."),
    divider(),
    h2("Frontend Technologies"),
    divider(),
    h3("React 18"),
    p("UI component library. Purpose: Renders the chat interface using component-based architecture with hooks. React 18 concurrent features enable smooth streaming updates."),
    h3("TypeScript"),
    p("Typed JavaScript superset. Purpose: Provides compile-time type safety across all frontend code, catching errors before runtime."),
    h3("Vite"),
    p("Build tool and dev server. Purpose: Provides instant hot-module replacement during development and optimized production builds with tree-shaking and code splitting."),
    h3("Tailwind CSS"),
    p("Utility-first CSS framework. Purpose: Styles the entire UI with composable utility classes. Supports dark/light theme via CSS custom properties."),
    h3("Radix UI"),
    p("Headless UI primitives. Purpose: Provides accessible, unstyled components (Dialog, ScrollArea, Button) that we style with Tailwind. Handles keyboard navigation and ARIA."),
    h3("Lucide React"),
    p("Icon library. Purpose: Provides all UI icons as tree-shakeable React components."),
    h3("Framer Motion"),
    p("Animation library. Purpose: Powers sidebar slide, message fade-in, model switching transitions, and offline banner animations."),
    h3("React Markdown + remark-gfm"),
    p("Markdown renderer. Purpose: Renders AI responses as rich formatted text with GitHub Flavored Markdown support."),
    h3("react-syntax-highlighter (Prism)"),
    p("Code syntax highlighting. Purpose: Renders code blocks with language-specific coloring using VS Code Dark+ theme."),
])

append_blocks(tech_id, [
    divider(),
    h2("Monorepo & Build Tools"),
    divider(),
    h3("npm Workspaces"),
    p("Native Node.js monorepo support. Purpose: Links apps and packages into a single dependency tree. One npm install at root installs everything."),
    h3("Turborepo"),
    p("Build orchestrator. Purpose: Defines task pipelines (build, lint, dev) with dependency ordering and caching."),
    divider(),
    h2("DevOps & Infrastructure Tools"),
    divider(),
    h3("Docker"),
    p("Containerization. Purpose: Packages backend and frontend into isolated containers. Multi-stage builds minimize image size."),
    h3("Docker Compose"),
    p("Multi-container orchestration. Purpose: Defines both services in one file. Single command starts the entire stack."),
    h3("Nginx"),
    p("Reverse proxy. Purpose: Serves frontend SPA, proxies /api/ to backend, handles SPA routing fallback, adds caching headers."),
    h3("GitHub Actions"),
    p("CI/CD. Purpose: Runs backend tests and frontend lint/build on every push/PR to main."),
    h3("Makefile"),
    p("Task runner. Purpose: Short commands (make dev-backend, make test) that abstract long shell commands. Self-documenting."),
])

# ============================================================
print("3/8 Architecture...")
create_page(PARENT, "Architecture & Monorepo Structure", "\U0001F3D7", [
    callout("How the system is designed, how data flows, and how the codebase is organized.", "\U0001F527"),
    divider(),
    h2("System Architecture"),
    code("Frontend (React SPA)  --HTTP/SSE-->  Backend (FastAPI)  --SDK-->  Azure AI Services\n     localhost:5173                    localhost:8000              Azure endpoints", "plain text"),
    divider(),
    h2("Request Flow"),
    num("User types a message in the frontend chat input"),
    num("Frontend sends POST /api/v1/chat/stream with message, model, system_prompt"),
    num("Backend routes to AzureOpenAIService or DeepSeekService based on model"),
    num("Service calls Azure API via OpenAI SDK with streaming enabled"),
    num("Backend yields SSE events with delta content for each token"),
    num("Frontend reads the stream, appending tokens to the message bubble in real-time"),
    num("Stream ends: backend sends done event with latency and model name"),
    num("Frontend displays final latency badge"),
    divider(),
    h2("Monorepo Layout"),
    code("DualAIChat-WebApp/\n|\n+-- apps/\n|   +-- backend/          # Python FastAPI service\n|   |   +-- app/\n|   |   |   +-- api/v1/endpoints/   # Route handlers\n|   |   |   +-- core/               # Config, logging\n|   |   |   +-- middleware/         # Request logging\n|   |   |   +-- schemas/           # Pydantic models\n|   |   |   +-- services/          # AI SDK clients\n|   |   +-- tests/                  # pytest suite\n|   |   +-- Dockerfile\n|   |   +-- requirements.txt\n|   |\n|   +-- frontend/         # React + Vite SPA\n|       +-- src/\n|       |   +-- api/              # Fetch + SSE client\n|       |   +-- components/\n|       |   |   +-- chat/         # ChatWindow, MessageBubble\n|       |   |   +-- layout/       # ErrorBoundary, ThemeToggle\n|       |   |   +-- ui/           # Radix primitives\n|       |   +-- constants/\n|       |   +-- hooks/            # useChat\n|       |   +-- styles/           # Global CSS\n|       |   +-- types/\n|       +-- Dockerfile\n|       +-- nginx.conf\n|\n+-- packages/\n|   +-- shared-types/     # @dualai/shared-types\n|   +-- typescript-config/ # @dualai/typescript-config\n|\n+-- docs/\n+-- .github/workflows/    # CI pipeline\n+-- docker-compose.yml\n+-- turbo.json\n+-- package.json          # Root workspaces\n+-- Makefile", "plain text"),
    divider(),
    h2("Why Monorepo?"),
    bullet("Single source of truth - all code in one repository"),
    bullet("Shared packages - TypeScript types reusable across future apps"),
    bullet("Atomic changes - backend + frontend changes in one commit/PR"),
    bullet("Unified CI - one pipeline tests everything"),
    bullet("Consistent tooling - shared configs and build scripts"),
])

# ============================================================
print("4/8 Backend...")
create_page(PARENT, "Backend \u2014 FastAPI Service", "\u2699", [
    callout("Deep dive into the Python backend: endpoints, AI services, and configuration.", "\U0001F40D"),
    divider(),
    h2("Entry Point: main.py"),
    p("The FastAPI application configures:"),
    bullet("CORS middleware - allows frontend origins (localhost:5173, localhost:3000)"),
    bullet("Request logging middleware - logs every request with method, path, status, duration"),
    bullet("Global exception handler - catches unhandled errors, returns generic 500"),
    bullet("API router - mounts chat endpoints at /api/v1/chat/"),
    bullet("Health endpoint - reports model availability"),
    divider(),
    h2("API Endpoints"),
    h3("POST /api/v1/chat/completions"),
    p("Non-streaming completion. Sends full message to selected AI model, returns complete response as JSON."),
    h3("POST /api/v1/chat/stream"),
    p("SSE streaming. Returns text/event-stream with three event types:"),
    bullet("delta - chunk of generated text (token by token)"),
    bullet("done - signals completion with latency and model name"),
    bullet("error - signals generation error"),
    divider(),
    h2("Services: llm_service.py"),
    h3("AzureOpenAIService"),
    p("Uses AsyncAzureOpenAI from openai SDK. Connects to Azure Cognitive Services for GPT-4o-mini. Handles streaming/non-streaming with timeout and error handling."),
    h3("DeepSeekService"),
    p("Uses AsyncOpenAI pointed at Azure AI Foundry. Connects to DeepSeek-R1. Appends /openai/v1 to endpoint. Falls back to AZURE_KEY if DEEPSEEK_API_KEY not set."),
    divider(),
    h2("Configuration: config.py"),
    p("Pydantic-Settings loads env vars from root .env. Path calculated dynamically (5 levels up from app/core/config.py). All settings type-validated with defaults."),
    divider(),
    h2("Schemas"),
    bullet("ModelName enum: gpt-4 or deepseek (rejects others with 422)"),
    bullet("ChatRequest: message (1-32000 chars), model, stream, system_prompt (max 4000)"),
    bullet("ChatResponse: reply, model, usage stats, latency"),
])

# ============================================================
print("5/8 Frontend...")
create_page(PARENT, "Frontend \u2014 React Application", "\U0001F3A8", [
    callout("UI structure, state management, and streaming message rendering.", "\u269B"),
    divider(),
    h2("Component Architecture"),
    h3("components/chat/"),
    bullet_bold("ChatWindow.tsx", " \u2014 Main interface: sidebar, header with model pills, dual panels, input area, suggested prompts"),
    bullet_bold("MessageBubble.tsx", " \u2014 Renders messages: markdown, code highlighting, copy/retry/feedback buttons"),
    h3("components/layout/"),
    bullet_bold("ErrorBoundary.tsx", " \u2014 Catches JS crashes, shows friendly fallback with reload"),
    bullet_bold("ThemeToggle.tsx", " \u2014 Dark/light toggle with sun/moon animation"),
    bullet_bold("theme-provider.tsx", " \u2014 Theme context, persists to localStorage"),
    h3("components/ui/"),
    p("Radix UI primitives (Button, Dialog, ScrollArea, Textarea) styled with Tailwind."),
    divider(),
    h2("State Management: useChat Hook"),
    bullet("messages[] \u2014 all messages with unique IDs"),
    bullet("loadingModels \u2014 Set tracking which models are generating"),
    bullet("sendMessage() \u2014 sends to selected models, streams responses"),
    bullet("cancelRequest() \u2014 aborts via AbortController"),
    bullet("retryMessage() \u2014 re-sends for failed AI response"),
    divider(),
    h2("API Client: api/chat.ts"),
    bullet("sendMessage() \u2014 POST /completions for non-streaming"),
    bullet("streamMessage() \u2014 POST /stream, reads SSE via ReadableStream"),
    bullet("checkHealth() \u2014 GET /health with 5s timeout"),
    divider(),
    h2("Styling"),
    bullet("Ultra-dark theme (zinc-950) for dark mode, clean white for light"),
    bullet("CSS custom properties (HSL) toggled via .dark class"),
    bullet("Inter font for professional typography"),
    bullet("Light mode contrast: all text opacity >= 60% for readability"),
    bullet("Custom scrollbar styling and smooth focus-visible outlines"),
])

# ============================================================
print("6/8 AI Models...")
create_page(PARENT, "AI Models & Azure Integration", "\U0001F916", [
    callout("How the two AI models are configured and what makes each one different.", "\u2601"),
    divider(),
    h2("GPT-4o-mini (Azure OpenAI)"),
    bullet_bold("Provider: ", "Azure Cognitive Services (OpenAI)"),
    bullet_bold("Endpoint: ", "*.cognitiveservices.azure.com"),
    bullet_bold("SDK Client: ", "AsyncAzureOpenAI from openai package"),
    bullet_bold("API Version: ", "2024-12-01-preview"),
    bullet_bold("Deployment: ", "gpt-4o-mini"),
    bullet_bold("Strengths: ", "Fast, versatile, great for general tasks and coding"),
    divider(),
    h2("DeepSeek-R1 (Azure AI Foundry)"),
    bullet_bold("Provider: ", "Azure AI Foundry (Model-as-a-Service)"),
    bullet_bold("Endpoint: ", "*.services.ai.azure.com"),
    bullet_bold("SDK Client: ", "AsyncOpenAI (standard, not Azure-specific)"),
    bullet_bold("Deployment: ", "DeepSeek-R1"),
    bullet_bold("Strengths: ", "Advanced reasoning, chain-of-thought, math and logic"),
    divider(),
    h2("Side-by-Side Value"),
    bullet("GPT-4o responds faster, may give more generic answers"),
    bullet("DeepSeek-R1 takes longer but provides deeper reasoning"),
    bullet("Users see which model handles specific tasks better"),
    bullet("Enterprise teams evaluate models before committing to one"),
    divider(),
    h2("Environment Variables"),
    code("# Azure OpenAI (GPT-4o-mini)\nAZURE_ENDPOINT=https://your-resource.cognitiveservices.azure.com/\nAZURE_KEY=your-api-key\nAZURE_API_VERSION=2024-12-01-preview\nAZURE_DEPLOYMENT=gpt-4o-mini\n\n# Azure AI Foundry (DeepSeek-R1)\nDEEPSEEK_ENDPOINT=https://your-resource.services.ai.azure.com\nDEEPSEEK_API_KEY=your-key-or-leave-empty\nDEEPSEEK_DEPLOYMENT=DeepSeek-R1", "plain text"),
])

# ============================================================
print("7/8 DevOps...")
create_page(PARENT, "DevOps & Infrastructure", "\U0001F433", [
    callout("Docker containers, CI/CD pipelines, and production deployment.", "\u2699"),
    divider(),
    h2("Docker Setup"),
    h3("Backend Dockerfile (Multi-stage)"),
    p("Stage 1 (Builder): Installs Python deps. Stage 2 (Runtime): Copies packages + code only. Runs as non-root user."),
    h3("Frontend Dockerfile (Multi-stage)"),
    p("Stage 1: npm ci + npm run build. Stage 2: nginx:alpine serves /dist with custom config."),
    h3("docker-compose.yml"),
    bullet("Backend: builds from apps/backend, loads .env, port 8000, health check"),
    bullet("Frontend: builds from apps/frontend, port 80, depends on backend health"),
    bullet("One command: docker compose up --build -d"),
    divider(),
    h2("Nginx Configuration"),
    num("SPA Fallback: try_files with /index.html for client-side routing"),
    num("API Proxy: /api/ proxies to backend:8000 with SSE support"),
    num("Static Caching: 30-day Cache-Control for JS/CSS/images"),
    divider(),
    h2("GitHub Actions CI"),
    h3("Backend Job"),
    bullet("Python 3.12 with pip caching"),
    bullet("Install requirements + pytest + httpx"),
    bullet("Run pytest tests/ -v"),
    h3("Frontend Job"),
    bullet("Node 20 with npm caching"),
    bullet("npm ci, npm run lint, npm run build"),
    divider(),
    h2("Makefile Commands"),
    code("make dev-backend     # Start FastAPI dev server\nmake dev-frontend    # Start Vite dev server\nmake install         # Install all dependencies\nmake docker-up       # Build & start Docker stack\nmake docker-down     # Stop Docker stack\nmake test-backend    # Run pytest\nmake lint-frontend   # Run ESLint\nmake clean           # Remove caches\nmake help            # Show all commands", "plain text"),
])

# ============================================================
print("8/8 API Reference...")
create_page(PARENT, "API Reference", "\U0001F4E1", [
    callout("Complete API documentation for all backend endpoints.", "\U0001F4C4"),
    divider(),
    h2("Base URL"),
    code("http://localhost:8000", "plain text"),
    divider(),
    h2("GET /"),
    p("Returns API info and version."),
    code('{"message": "Welcome to Dual AI Chat API", "version": "2.1"}', "json"),
    divider(),
    h2("GET /health"),
    p("Health check with model availability."),
    code('{\n  "status": "healthy",\n  "models": {\n    "azure_openai": true,\n    "deepseek": true\n  }\n}', "json"),
    divider(),
    h2("POST /api/v1/chat/completions"),
    p("Non-streaming chat completion."),
    h3("Request"),
    code('{\n  "message": "Explain quantum computing",\n  "model": "gpt-4",\n  "system_prompt": "You are a helpful assistant."\n}', "json"),
    h3("Response"),
    code('{\n  "reply": "Quantum computing uses quantum bits...",\n  "model": "gpt-4",\n  "usage": {"prompt_tokens": 15, "completion_tokens": 120},\n  "latency": 2.341\n}', "json"),
    divider(),
    h2("POST /api/v1/chat/stream"),
    p("SSE streaming completion. Returns text/event-stream."),
    h3("Request"),
    code('{\n  "message": "Write a Python function",\n  "model": "deepseek",\n  "stream": true\n}', "json"),
    h3("SSE Events"),
    code('data: {"type": "delta", "content": "Here"}\ndata: {"type": "delta", "content": " is"}\n...\ndata: {"type": "done", "latency": 3.456, "model": "deepseek"}\ndata: {"type": "error", "content": "An error occurred."}', "plain text"),
    divider(),
    h2("Validation Rules"),
    bullet("model: must be gpt-4 or deepseek (422 otherwise)"),
    bullet("message: required, 1-32000 characters"),
    bullet("system_prompt: optional, max 4000 characters"),
])

# ============================================================
print("\n9/9 Phase 2 Roadmap...")
create_page(PARENT, "Phase 2 \u2014 Roadmap", "\U0001F5FA", [
    callout("Planned features for Phase 2. Phase 1 built the foundation \u2014 Phase 2 takes it to production-grade.", "\U0001F680"),
    divider(),
    h2("Authentication & User Management"),
    bullet("User signup/login with OAuth (Google, GitHub, Microsoft)"),
    bullet("Session management with JWT tokens"),
    bullet("User-specific chat history stored in database"),
    bullet("Role-based access control (admin, user, viewer)"),
    divider(),
    h2("Database & Persistence"),
    bullet("PostgreSQL for user data, chat history, and analytics"),
    bullet("SQLAlchemy ORM for type-safe database operations"),
    bullet("Redis for session caching and rate limiting"),
    bullet("Database migrations with Alembic"),
    divider(),
    h2("Advanced AI Features"),
    bullet("Temperature and max_tokens controls in UI"),
    bullet("Multi-turn conversation context (full history sent)"),
    bullet("File upload support (images, documents, code)"),
    bullet("Add more models (Claude, Gemini, Llama)"),
    bullet("Model response rating and analytics dashboard"),
    divider(),
    h2("Production Hardening"),
    bullet("Rate limiting per user and per IP"),
    bullet("API key rotation with Azure Key Vault"),
    bullet("Structured logging with correlation IDs"),
    bullet("Prometheus metrics + Grafana dashboard"),
    bullet("Load testing with locust or k6"),
    divider(),
    h2("UI/UX Enhancements"),
    bullet("Conversation branching (fork from any message)"),
    bullet("Markdown editor for input with preview"),
    bullet("Export conversations (PDF, Markdown, JSON)"),
    bullet("Keyboard shortcuts panel"),
    bullet("Mobile-responsive design improvements"),
    bullet("Accessibility audit (WCAG 2.1 AA)"),
    divider(),
    h2("Infrastructure"),
    bullet("Kubernetes deployment (Helm charts)"),
    bullet("Terraform for Azure provisioning"),
    bullet("CDN for frontend static assets"),
    bullet("Blue-green or canary deployment"),
    bullet("Automated E2E tests with Playwright"),
])

print("\n" + "=" * 50)
print("ALL PAGES CREATED SUCCESSFULLY!")
print("=" * 50)
print(f"https://www.notion.so/Dual-AI-Chat-Project-Docs-{PARENT.replace('-','')}")
