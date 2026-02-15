$token = $env:NOTION_TOKEN
$parentId = "3086efb9-58c3-8036-a0a2-f772f5e59158"
$headers = @{
    "Authorization" = "Bearer $token"
    "Notion-Version" = "2022-06-28"
    "Content-Type" = "application/json"
}

function New-NotionPage($parentId, $title, $icon, $blocks) {
    $body = @{
        parent = @{ page_id = $parentId }
        icon = @{ type = "emoji"; emoji = $icon }
        properties = @{
            title = @(@{ text = @{ content = $title } })
        }
        children = $blocks
    } | ConvertTo-Json -Depth 20 -Compress
    
    Start-Sleep -Milliseconds 400
    $result = Invoke-RestMethod -Uri "https://api.notion.com/v1/pages" -Method POST -Headers $headers -Body ([System.Text.Encoding]::UTF8.GetBytes($body))
    Write-Host "  Created: $title ($($result.id))"
    return $result.id
}

function Add-Blocks($pageId, $blocks) {
    $body = @{ children = $blocks } | ConvertTo-Json -Depth 20 -Compress
    Start-Sleep -Milliseconds 400
    Invoke-RestMethod -Uri "https://api.notion.com/v1/blocks/$pageId/children" -Method PATCH -Headers $headers -Body ([System.Text.Encoding]::UTF8.GetBytes($body)) | Out-Null
}

function H1($text) { @{ object="block"; type="heading_1"; heading_1=@{ rich_text=@(@{type="text";text=@{content=$text}}) } } }
function H2($text) { @{ object="block"; type="heading_2"; heading_2=@{ rich_text=@(@{type="text";text=@{content=$text}}) } } }
function H3($text) { @{ object="block"; type="heading_3"; heading_3=@{ rich_text=@(@{type="text";text=@{content=$text}}) } } }
function P($text) { @{ object="block"; type="paragraph"; paragraph=@{ rich_text=@(@{type="text";text=@{content=$text}}) } } }
function PBold($boldText, $normalText) { @{ object="block"; type="paragraph"; paragraph=@{ rich_text=@(@{type="text";text=@{content=$boldText};annotations=@{bold=$true}}, @{type="text";text=@{content=$normalText}}) } } }
function Bullet($text) { @{ object="block"; type="bulleted_list_item"; bulleted_list_item=@{ rich_text=@(@{type="text";text=@{content=$text}}) } } }
function BulletBold($boldText, $normalText) { @{ object="block"; type="bulleted_list_item"; bulleted_list_item=@{ rich_text=@(@{type="text";text=@{content=$boldText};annotations=@{bold=$true}}, @{type="text";text=@{content=$normalText}}) } } }
function Num($text) { @{ object="block"; type="numbered_list_item"; numbered_list_item=@{ rich_text=@(@{type="text";text=@{content=$text}}) } } }
function Divider { @{ object="block"; type="divider"; divider=@{} } }
function Callout($text, $icon) { @{ object="block"; type="callout"; callout=@{ rich_text=@(@{type="text";text=@{content=$text}}); icon=@{type="emoji";emoji=$icon} } } }
function CodeBlock($text, $lang) { @{ object="block"; type="code"; code=@{ rich_text=@(@{type="text";text=@{content=$text}}); language=$lang } } }
function Quote($text) { @{ object="block"; type="quote"; quote=@{ rich_text=@(@{type="text";text=@{content=$text}}) } } }
function Toggle($text) { @{ object="block"; type="toggle"; toggle=@{ rich_text=@(@{type="text";text=@{content=$text}}) } } }

# ============================================================
# 0. ADD INTRO TO MAIN PAGE
# ============================================================
Write-Host "Adding intro to main page..."
Add-Blocks $parentId @(
    (Callout "Enterprise-grade side-by-side AI comparison platform powered by Azure OpenAI (GPT-4o) and Azure AI Foundry (DeepSeek-R1)." "`u{1F680}")
    (Divider)
    (H2 "Project Status")
    (PBold "Current Phase: " "Phase 1 - Foundation & Core Features (COMPLETED)")
    (PBold "Next Phase: " "Phase 2 - Advanced Features & Production Hardening")
    (Divider)
    (H2 "Quick Navigation")
    (P "Browse the subpages below for detailed documentation on every aspect of the project.")
    (Divider)
)

# ============================================================
# 1. PHASE 1 - WHAT WE BUILT
# ============================================================
Write-Host "`nCreating Phase 1 page..."
$phase1Id = New-NotionPage $parentId "Phase 1 - What We Built" "`u{2705}" @(
    (Callout "Phase 1 is the foundation layer. Everything built here establishes the core architecture, UI/UX, and AI integrations that all future phases build upon." "`u{1F4CB}")
    (Divider)
    (H2 "Summary of Work Completed")
    (P "Phase 1 covered the complete build-out of a dual-AI chat platform from scratch, including backend API development, frontend UI, Azure AI integrations, enterprise project structure, and DevOps tooling.")
    (Divider)
    (H2 "1. Backend API (FastAPI)")
    (Bullet "Built a Python FastAPI backend with versioned REST API endpoints (/api/v1/)")
    (Bullet "Integrated Azure OpenAI SDK (AsyncAzureOpenAI) for GPT-4o-mini completions")
    (Bullet "Integrated Azure AI Foundry SDK (AsyncOpenAI) for DeepSeek-R1 reasoning model")
    (Bullet "Implemented Server-Sent Events (SSE) streaming for real-time token-by-token responses")
    (Bullet "Added Pydantic-settings for type-safe environment configuration from .env")
    (Bullet "Built centralized logging with structured output and request/response middleware")
    (Bullet "Added global exception handler to prevent credential leakage in error responses")
    (Bullet "Created health check endpoint reporting model availability status")
    (Divider)
    (H2 "2. Frontend UI (React + TypeScript)")
    (Bullet "Built a React 18 SPA with TypeScript and Vite for fast development")
    (Bullet "Designed an Abacus AI-inspired dark/light theme with professional typography (Inter font)")
    (Bullet "Implemented side-by-side dual chat panels comparing GPT-4o and DeepSeek-R1 simultaneously")
    (Bullet "Added collapsible sidebar with chat history, new conversation, and settings")
    (Bullet "Built real-time streaming message display with markdown rendering and syntax highlighting")
    (Bullet "Added model selection pills (Dual View / GPT-4o only / DeepSeek-R1 only)")
    (Bullet "Implemented copy-to-clipboard, retry failed messages, thumbs up/down feedback")
    (Bullet "Added backend health monitoring with offline banner")
    (Bullet "Built multi-line input with Shift+Enter support and auto-resize")
    (Bullet "Added suggested prompts for empty state and smooth scroll-to-bottom")
    (Divider)
    (H2 "3. Enterprise Project Structure")
    (Bullet "Migrated to monorepo pattern with apps/ and packages/ directories")
    (Bullet "Added npm workspaces for shared package management")
    (Bullet "Created @dualai/shared-types package for TypeScript API contracts")
    (Bullet "Created @dualai/typescript-config for shared compiler settings")
    (Bullet "Added Turborepo config (turbo.json) for build pipeline orchestration")
    (Bullet "Organized frontend with feature-based component grouping (chat/, layout/, ui/)")
    (Bullet "Added barrel exports (index.ts) for clean imports")
    (Bullet "Added __init__.py to every Python package for proper packaging")
    (Divider)
    (H2 "4. DevOps & Infrastructure")
    (Bullet "Multi-stage Dockerfiles for both backend (Python) and frontend (Nginx)")
    (Bullet "docker-compose.yml for one-command production deployment")
    (Bullet "GitHub Actions CI pipeline (backend tests + frontend lint/build)")
    (Bullet "Makefile with common developer commands")
    (Bullet "Comprehensive .gitignore and .dockerignore")
    (Bullet ".env.example template (no secrets committed)")
    (Divider)
    (H2 "5. Testing Foundation")
    (Bullet "pytest setup with conftest.py and shared fixtures")
    (Bullet "Test skeletons for API endpoints (health, chat validation)")
    (Bullet "Test skeletons for service layer (LLM service instantiation)")
    (Divider)
    (H2 "6. Bug Fixes & Troubleshooting")
    (Bullet "Fixed CORS blocking frontend-backend communication (405 on OPTIONS)")
    (Bullet "Fixed Pydantic-settings JSON parsing for BACKEND_CORS_ORIGINS")
    (Bullet "Fixed light mode contrast issues (low-opacity text unreadable on white)")
    (Bullet "Fixed sidebar delete button overlapping chat history titles")
    (Bullet "Fixed CSS @import order warnings in Vite")
    (Bullet "Fixed PowerShell command syntax compatibility")
)

# ============================================================
# 2. TECH STACK & TOOLS REFERENCE
# ============================================================
Write-Host "Creating Tech Stack page..."
$techId = New-NotionPage $parentId "Tech Stack & Tools Reference" "`u{1F6E0}" @(
    (Callout "Complete reference of every technology, library, and tool used in the project with its specific purpose." "`u{1F4DA}")
    (Divider)
    (H2 "Backend Technologies")
    (Divider)
    (H3 "Python 3.12")
    (P "The core runtime for the backend. Chosen for its async/await support, rich AI/ML ecosystem, and strong typing with type hints.")
    (H3 "FastAPI")
    (P "Modern, high-performance Python web framework. Purpose: Serves the REST API endpoints, handles request validation via Pydantic, provides automatic OpenAPI documentation, and supports async request handling for non-blocking AI API calls.")
    (H3 "Uvicorn")
    (P "ASGI server that runs FastAPI in production. Purpose: Serves the application with async support, hot-reload in development, and multi-worker capability for production.")
    (H3 "OpenAI Python SDK (openai >= 1.50)")
    (P "Official SDK for OpenAI-compatible APIs. Purpose: Provides AsyncAzureOpenAI client for GPT-4o-mini and AsyncOpenAI client for DeepSeek-R1. Handles authentication, streaming, retries, and error handling for both Azure endpoints.")
    (H3 "Pydantic & Pydantic-Settings")
    (P "Data validation and settings management. Purpose: Pydantic validates all API request/response schemas with type checking. Pydantic-Settings loads and validates environment variables from .env files with type coercion.")
    (H3 "python-dotenv")
    (P "Environment variable loader. Purpose: Reads the root .env file and injects variables into the process environment for Pydantic-Settings to consume.")
    (H3 "pytest")
    (P "Testing framework. Purpose: Runs backend unit and integration tests with fixtures, parametrize, and async support.")
    (H3 "httpx")
    (P "Async HTTP client. Purpose: Used by FastAPI's TestClient for integration testing and as a dependency for the OpenAI SDK's async operations.")
    (H3 "flake8")
    (P "Python linter. Purpose: Enforces code style consistency (PEP 8) across the backend codebase.")
)

Start-Sleep -Milliseconds 400
Add-Blocks $techId @(
    (Divider)
    (H2 "Frontend Technologies")
    (Divider)
    (H3 "React 18")
    (P "UI component library. Purpose: Renders the entire chat interface using a component-based architecture with hooks for state management. React 18's concurrent features enable smooth streaming updates.")
    (H3 "TypeScript")
    (P "Typed JavaScript superset. Purpose: Provides compile-time type safety across all frontend code, catching errors before runtime. Shared types in @dualai/shared-types ensure API contract consistency.")
    (H3 "Vite")
    (P "Build tool and dev server. Purpose: Provides instant hot-module replacement (HMR) during development and optimized production builds with tree-shaking, code splitting, and asset hashing.")
    (H3 "Tailwind CSS")
    (P "Utility-first CSS framework. Purpose: Styles the entire UI with composable utility classes. Enables rapid iteration on design without writing custom CSS files. Supports dark/light theme via CSS custom properties.")
    (H3 "Radix UI")
    (P "Headless UI component primitives. Purpose: Provides accessible, unstyled components (Dialog, ScrollArea, Button, etc.) that we style with Tailwind. Handles keyboard navigation, focus management, and ARIA attributes automatically.")
    (H3 "Lucide React")
    (P "Icon library. Purpose: Provides all UI icons (Send, Copy, Settings, Sparkles, BrainCircuit, etc.) as tree-shakeable React components.")
    (H3 "Framer Motion")
    (P "Animation library. Purpose: Powers all UI animations - sidebar slide in/out, message fade-in, model switching transitions, and the offline banner appearance.")
    (H3 "React Markdown + remark-gfm")
    (P "Markdown renderer. Purpose: Renders AI responses as rich formatted text with GitHub Flavored Markdown support (tables, strikethrough, task lists).")
    (H3 "react-syntax-highlighter (Prism)")
    (P "Code syntax highlighting. Purpose: Renders code blocks in AI responses with language-specific syntax coloring using the VS Code Dark+ theme.")
)

Start-Sleep -Milliseconds 400
Add-Blocks $techId @(
    (Divider)
    (H2 "Monorepo & Build Tools")
    (Divider)
    (H3 "npm Workspaces")
    (P "Native Node.js monorepo support. Purpose: Links apps/frontend, packages/shared-types, and packages/typescript-config into a single dependency tree. Running npm install at the root installs everything.")
    (H3 "Turborepo")
    (P "Monorepo build orchestrator. Purpose: Defines task pipelines (build, lint, dev) with dependency ordering and caching. Ensures shared packages build before apps that depend on them.")
    (Divider)
    (H2 "DevOps & Infrastructure Tools")
    (Divider)
    (H3 "Docker")
    (P "Containerization platform. Purpose: Packages backend and frontend into isolated, reproducible containers. Multi-stage builds minimize image size (build stage discarded, only runtime artifacts kept).")
    (H3 "Docker Compose")
    (P "Multi-container orchestration. Purpose: Defines both services (backend + frontend) in one file. Single command (docker compose up) starts the entire stack with health checks, restart policies, and environment injection.")
    (H3 "Nginx")
    (P "Reverse proxy and static file server. Purpose: Serves the built frontend SPA, proxies /api/ requests to the backend, handles SPA client-side routing fallback, and adds caching headers for static assets.")
    (H3 "GitHub Actions")
    (P "CI/CD platform. Purpose: Automatically runs backend tests (pytest) and frontend quality checks (lint + build) on every push/PR to main. Catches regressions before merge.")
    (H3 "Makefile")
    (P "Developer task runner. Purpose: Provides short memorable commands (make dev-backend, make test, make docker-up) that abstract away long shell commands. Self-documenting with make help.")
)

# ============================================================
# 3. ARCHITECTURE & MONOREPO STRUCTURE
# ============================================================
Write-Host "Creating Architecture page..."
$archId = New-NotionPage $parentId "Architecture & Monorepo Structure" "`u{1F3D7}" @(
    (Callout "How the system is designed, how data flows, and how the codebase is organized." "`u{1F527}")
    (Divider)
    (H2 "System Architecture")
    (P "The system follows a clean client-server architecture with streaming support:")
    (CodeBlock "Frontend (React SPA)  --HTTP/SSE-->  Backend (FastAPI)  --SDK-->  Azure AI Services
     localhost:5173                    localhost:8000              cognitiveservices.azure.com
                                                                  services.ai.azure.com" "plain text")
    (Divider)
    (H2 "Request Flow")
    (Num "User types a message in the frontend chat input")
    (Num "Frontend sends POST /api/v1/chat/stream with { message, model, system_prompt }")
    (Num "Backend routes to AzureOpenAIService or DeepSeekService based on model field")
    (Num "Service calls Azure API via OpenAI SDK with streaming enabled")
    (Num "Backend yields SSE events: { type: 'delta', content: '...' } for each token")
    (Num "Frontend reads the stream, appending tokens to the message bubble in real-time")
    (Num "When stream ends, backend sends { type: 'done', latency: 1.234, model: 'gpt-4' }")
    (Num "Frontend displays final latency badge")
    (Divider)
    (H2 "Monorepo Layout")
    (CodeBlock "DualAIChat-WebApp/
+-- apps/
|   +-- backend/          # Python FastAPI service
|   |   +-- app/
|   |   |   +-- api/v1/endpoints/   # Route handlers
|   |   |   +-- core/               # Config, logging
|   |   |   +-- middleware/         # Request logging
|   |   |   +-- schemas/           # Pydantic models
|   |   |   +-- services/          # AI SDK clients
|   |   +-- tests/                  # pytest test suite
|   |   +-- Dockerfile
|   |   +-- requirements.txt
|   |   +-- run.py
|   |
|   +-- frontend/         # React + Vite SPA
|       +-- src/
|       |   +-- api/              # Fetch + SSE client
|       |   +-- components/
|       |   |   +-- chat/         # ChatWindow, MessageBubble
|       |   |   +-- layout/       # ErrorBoundary, ThemeToggle
|       |   |   +-- ui/           # Radix primitives
|       |   +-- constants/        # App-wide constants
|       |   +-- hooks/            # useChat state hook
|       |   +-- styles/           # Global CSS + Tailwind
|       |   +-- types/            # Local TypeScript types
|       +-- Dockerfile
|       +-- nginx.conf
|
+-- packages/
|   +-- shared-types/     # @dualai/shared-types
|   +-- typescript-config/ # @dualai/typescript-config
|
+-- docs/                  # Architecture + setup docs
+-- .github/workflows/    # CI pipeline
+-- .env.example           # Env template
+-- docker-compose.yml     # Production deploy
+-- turbo.json             # Build pipeline
+-- package.json           # Root workspaces
+-- Makefile               # Dev commands" "plain text")
    (Divider)
    (H2 "Why Monorepo?")
    (Bullet "Single source of truth - all code in one repository")
    (Bullet "Shared packages - TypeScript types used by frontend can be shared with future apps")
    (Bullet "Atomic changes - backend + frontend changes in one commit/PR")
    (Bullet "Unified CI - one pipeline tests everything")
    (Bullet "Consistent tooling - shared configs, linting rules, build scripts")
)

# ============================================================
# 4. BACKEND - FASTAPI SERVICE
# ============================================================
Write-Host "Creating Backend page..."
$backendId = New-NotionPage $parentId "Backend - FastAPI Service" "`u{2699}" @(
    (Callout "Deep dive into the Python backend: how endpoints work, how AI services are called, and how configuration is managed." "`u{1F40D}")
    (Divider)
    (H2 "Entry Point: main.py")
    (P "The FastAPI application is created in apps/backend/app/main.py. It configures:")
    (Bullet "CORS middleware - allows frontend origins (localhost:5173, localhost:3000)")
    (Bullet "Request logging middleware - logs every request with method, path, status, duration")
    (Bullet "Global exception handler - catches unhandled errors, returns generic 500 (no credential leaks)")
    (Bullet "API router - mounts chat endpoints at /api/v1/chat/")
    (Bullet "Health endpoint - reports model availability based on API key presence")
    (Divider)
    (H2 "API Endpoints: chat.py")
    (P "Two endpoints handle all chat functionality:")
    (H3 "POST /api/v1/chat/completions")
    (P "Non-streaming completion. Sends the full message to the selected AI model and returns the complete response as JSON with reply, model, usage, and latency fields.")
    (H3 "POST /api/v1/chat/stream")
    (P "SSE streaming completion. Returns a text/event-stream response where each token is sent as a Server-Sent Event. Three event types:")
    (Bullet "delta - contains a chunk of generated text (streamed token by token)")
    (Bullet "done - signals completion with total latency and model name")
    (Bullet "error - signals an error during generation")
    (Divider)
    (H2 "Services: llm_service.py")
    (P "Two service classes abstract the AI model interactions:")
    (H3 "AzureOpenAIService")
    (P "Uses AsyncAzureOpenAI client from the openai SDK. Connects to Azure Cognitive Services endpoint for GPT-4o-mini. Handles both streaming and non-streaming completions with timeout protection and specific error handling for APITimeoutError and APIError.")
    (H3 "DeepSeekService")
    (P "Uses AsyncOpenAI client pointed at Azure AI Foundry endpoint. Connects to DeepSeek-R1 model. Automatically appends /openai/v1 to the endpoint if not present. Falls back to AZURE_KEY if DEEPSEEK_API_KEY is not set.")
    (Divider)
    (H2 "Configuration: config.py")
    (P "Uses Pydantic-Settings to load environment variables from the root .env file. The path is calculated dynamically: app/core/config.py traverses up 5 levels to reach the project root. All settings are type-validated and have sensible defaults.")
    (Divider)
    (H2 "Schemas: chat.py")
    (P "Pydantic models enforce request validation:")
    (Bullet "ModelName enum: 'gpt-4' or 'deepseek' (rejects anything else with 422)")
    (Bullet "ChatRequest: message (1-32000 chars), model, stream flag, system_prompt (max 4000 chars)")
    (Bullet "ChatResponse: reply text, model name, usage stats, latency")
)

# ============================================================
# 5. FRONTEND - REACT APPLICATION
# ============================================================
Write-Host "Creating Frontend page..."
$frontendId = New-NotionPage $parentId "Frontend - React Application" "`u{1F3A8}" @(
    (Callout "How the UI is structured, how state is managed, and how streaming messages are rendered." "`u{269B}")
    (Divider)
    (H2 "Component Architecture")
    (P "Components are organized by feature following enterprise patterns:")
    (H3 "components/chat/")
    (BulletBold "ChatWindow.tsx" " - Main chat interface. Contains the sidebar, header with model pills, dual chat panels, input area, and suggested prompts. Manages chat history in localStorage.")
    (BulletBold "MessageBubble.tsx" " - Renders individual messages. User messages show right-aligned with dark bubble. AI messages show with model avatar, markdown content, code blocks with syntax highlighting, and action buttons (copy, retry, thumbs up/down).")
    (H3 "components/layout/")
    (BulletBold "ErrorBoundary.tsx" " - React error boundary. Catches any JavaScript crash in the component tree and shows a friendly 'Something went wrong' fallback with reload button.")
    (BulletBold "ThemeToggle.tsx" " - Dark/light mode toggle button with sun/moon icon animation.")
    (BulletBold "theme-provider.tsx" " - React context provider that manages the current theme, persists preference to localStorage, and applies the correct CSS class to the document root.")
    (H3 "components/ui/")
    (P "Radix UI primitives (Button, Dialog, ScrollArea, Textarea, etc.) styled with Tailwind. These are reusable building blocks used across all feature components.")
    (Divider)
    (H2 "State Management: useChat Hook")
    (P "The useChat hook (hooks/useChat.ts) manages all chat state:")
    (Bullet "messages[] - array of all messages (user + AI) with unique IDs")
    (Bullet "loadingModels - Set tracking which models are currently generating")
    (Bullet "systemPrompt - configurable system prompt applied to both models")
    (Bullet "sendMessage() - sends user message to selected model(s), creates placeholder AI messages, streams responses")
    (Bullet "cancelRequest() - aborts in-flight requests via AbortController")
    (Bullet "retryMessage() - re-sends the last user message for a failed AI response")
    (Divider)
    (H2 "API Client: api/chat.ts")
    (P "The API client handles all backend communication:")
    (Bullet "sendMessage() - POST to /completions for non-streaming responses")
    (Bullet "streamMessage() - POST to /stream, reads SSE via ReadableStream, parses JSON events, calls onEvent callback for each delta/done/error")
    (Bullet "checkHealth() - GET /health with 5s timeout, returns boolean for online status")
    (Divider)
    (H2 "Styling Approach")
    (Bullet "Ultra-dark theme (zinc-950) for dark mode, clean white for light mode")
    (Bullet "CSS custom properties (HSL) for theme colors, toggled via .dark class")
    (Bullet "Inter font family for professional typography")
    (Bullet "Light mode contrast fixes: all text opacity values >= 60% for readability")
    (Bullet "Custom scrollbar styling (thin, muted colors)")
    (Bullet "Smooth focus-visible outlines for accessibility")
)

# ============================================================
# 6. AI MODELS & AZURE INTEGRATION
# ============================================================
Write-Host "Creating AI Models page..."
$aiId = New-NotionPage $parentId "AI Models & Azure Integration" "`u{1F916}" @(
    (Callout "How the two AI models are configured, called, and what makes each one different." "`u{2601}")
    (Divider)
    (H2 "GPT-4o-mini (Azure OpenAI)")
    (BulletBold "Provider: " "Azure Cognitive Services (OpenAI)")
    (BulletBold "Endpoint: " "*.cognitiveservices.azure.com")
    (BulletBold "SDK Client: " "AsyncAzureOpenAI from openai package")
    (BulletBold "API Version: " "2024-12-01-preview")
    (BulletBold "Deployment Name: " "gpt-4o-mini")
    (BulletBold "Strengths: " "Fast responses, versatile, good at general tasks, coding, and conversation")
    (P "This is Microsoft's hosted version of OpenAI's GPT-4o-mini model. It uses Azure-specific authentication (API key + azure_endpoint) and the Azure API versioning scheme.")
    (Divider)
    (H2 "DeepSeek-R1 (Azure AI Foundry)")
    (BulletBold "Provider: " "Azure AI Foundry (Model-as-a-Service)")
    (BulletBold "Endpoint: " "*.services.ai.azure.com")
    (BulletBold "SDK Client: " "AsyncOpenAI from openai package (not Azure-specific)")
    (BulletBold "Deployment Name: " "DeepSeek-R1")
    (BulletBold "Strengths: " "Advanced reasoning, chain-of-thought, mathematical and logical problem solving")
    (P "DeepSeek-R1 is hosted through Azure AI Foundry's Model-as-a-Service. Unlike Azure OpenAI, it uses the standard OpenAI SDK client with base_url pointed at the Azure endpoint + /openai/v1 path. The API key can be the same Azure key or a separate one.")
    (Divider)
    (H2 "Side-by-Side Value Proposition")
    (P "The dual-panel design lets users compare both models on the same prompt simultaneously. This is valuable because:")
    (Bullet "GPT-4o responds faster but may give more generic answers")
    (Bullet "DeepSeek-R1 takes longer but provides deeper reasoning with chain-of-thought")
    (Bullet "Users can see which model handles specific tasks better (code, math, creative writing)")
    (Bullet "Enterprise teams can evaluate models before committing to one for production use")
    (Divider)
    (H2 "Environment Variables")
    (CodeBlock "# Azure OpenAI (GPT-4o-mini)
AZURE_ENDPOINT=https://your-resource.cognitiveservices.azure.com/
AZURE_KEY=your-api-key
AZURE_API_VERSION=2024-12-01-preview
AZURE_DEPLOYMENT=gpt-4o-mini

# Azure AI Foundry (DeepSeek-R1)
DEEPSEEK_ENDPOINT=https://your-resource.services.ai.azure.com
DEEPSEEK_API_KEY=your-deepseek-key  (or leave empty to use AZURE_KEY)
DEEPSEEK_DEPLOYMENT=DeepSeek-R1" "plain text")
)

# ============================================================
# 7. DEVOPS & INFRASTRUCTURE
# ============================================================
Write-Host "Creating DevOps page..."
$devopsId = New-NotionPage $parentId "DevOps & Infrastructure" "`u{1F433}" @(
    (Callout "Docker containers, CI/CD pipelines, and production deployment configuration." "`u{2699}")
    (Divider)
    (H2 "Docker Setup")
    (H3 "Backend Dockerfile (Multi-stage)")
    (P "Stage 1 (Builder): Installs Python dependencies into a clean prefix directory. Stage 2 (Runtime): Copies only the installed packages and app code. Runs as non-root 'app' user for security. Final image is minimal (no build tools, no pip cache).")
    (H3 "Frontend Dockerfile (Multi-stage)")
    (P "Stage 1 (Builder): Runs npm ci and npm run build to produce static files in /dist. Stage 2 (Serve): Uses nginx:alpine to serve the built files. Copies custom nginx.conf for SPA routing and API proxying.")
    (H3 "docker-compose.yml")
    (P "Defines both services with proper configuration:")
    (Bullet "Backend: builds from apps/backend, loads .env, exposes port 8000, health check every 30s")
    (Bullet "Frontend: builds from apps/frontend, exposes port 80, depends on backend being healthy")
    (Bullet "One command deploy: docker compose up --build -d")
    (Divider)
    (H2 "Nginx Configuration")
    (P "The frontend nginx.conf handles three responsibilities:")
    (Num "SPA Fallback: try_files with /index.html fallback for client-side routing")
    (Num "API Proxy: /api/ and /health routes proxy_pass to backend:8000 with SSE support (proxy_buffering off)")
    (Num "Static Caching: JS/CSS/images get 30-day Cache-Control headers with immutable flag")
    (Divider)
    (H2 "GitHub Actions CI")
    (P "The .github/workflows/ci.yml pipeline runs on every push/PR to main:")
    (H3 "Backend Job")
    (Bullet "Sets up Python 3.12 with pip caching")
    (Bullet "Installs requirements.txt + pytest + httpx")
    (Bullet "Runs python -m pytest tests/ -v")
    (H3 "Frontend Job")
    (Bullet "Sets up Node 20 with npm caching")
    (Bullet "Runs npm ci (clean install)")
    (Bullet "Runs npm run lint (ESLint)")
    (Bullet "Runs npm run build (Vite production build)")
    (Divider)
    (H2 "Makefile Commands")
    (CodeBlock "make dev-backend     # Start FastAPI dev server
make dev-frontend    # Start Vite dev server
make install         # Install all dependencies
make docker-up       # Build & start Docker stack
make docker-down     # Stop Docker stack
make test-backend    # Run pytest
make lint-frontend   # Run ESLint
make clean           # Remove caches and node_modules
make help            # Show all commands" "plain text")
)

# ============================================================
# 8. API REFERENCE
# ============================================================
Write-Host "Creating API Reference page..."
$apiId = New-NotionPage $parentId "API Reference" "`u{1F4E1}" @(
    (Callout "Complete API documentation for all backend endpoints." "`u{1F4C4}")
    (Divider)
    (H2 "Base URL")
    (CodeBlock "http://localhost:8000" "plain text")
    (Divider)
    (H2 "GET /")
    (P "Returns API info and version.")
    (CodeBlock '{"message": "Welcome to Dual AI Chat API", "version": "2.1"}' "json")
    (Divider)
    (H2 "GET /health")
    (P "Health check with model availability status.")
    (CodeBlock '{
  "status": "healthy",
  "models": {
    "azure_openai": true,
    "deepseek": true
  }
}' "json")
    (Divider)
    (H2 "POST /api/v1/chat/completions")
    (P "Non-streaming chat completion.")
    (H3 "Request Body")
    (CodeBlock '{
  "message": "Explain quantum computing",
  "model": "gpt-4",
  "system_prompt": "You are a helpful assistant."
}' "json")
    (H3 "Response")
    (CodeBlock '{
  "reply": "Quantum computing uses quantum bits...",
  "model": "gpt-4",
  "usage": {"prompt_tokens": 15, "completion_tokens": 120, "total_tokens": 135},
  "latency": 2.341
}' "json")
    (Divider)
    (H2 "POST /api/v1/chat/stream")
    (P "SSE streaming chat completion. Returns text/event-stream.")
    (H3 "Request Body")
    (CodeBlock '{
  "message": "Write a Python function",
  "model": "deepseek",
  "stream": true,
  "system_prompt": "You are a helpful assistant."
}' "json")
    (H3 "SSE Events")
    (CodeBlock 'data: {"type": "delta", "content": "Here"}
data: {"type": "delta", "content": " is"}
data: {"type": "delta", "content": " a"}
...
data: {"type": "done", "latency": 3.456, "model": "deepseek"}' "plain text")
    (H3 "Error Event")
    (CodeBlock 'data: {"type": "error", "content": "An error occurred during streaming."}' "json")
    (Divider)
    (H2 "Validation Rules")
    (Bullet "model: must be 'gpt-4' or 'deepseek' (422 otherwise)")
    (Bullet "message: required, 1-32000 characters")
    (Bullet "system_prompt: optional, max 4000 characters")
)

# ============================================================
# 9. PHASE 2 - ROADMAP
# ============================================================
Write-Host "Creating Phase 2 Roadmap page..."
$roadmapId = New-NotionPage $parentId "Phase 2 - Roadmap" "`u{1F5FA}" @(
    (Callout "Planned features and improvements for Phase 2. Phase 1 established the foundation - Phase 2 takes it to production-grade." "`u{1F680}")
    (Divider)
    (H2 "Authentication & User Management")
    (Bullet "User signup/login with OAuth (Google, GitHub, Microsoft)")
    (Bullet "Session management with JWT tokens")
    (Bullet "User-specific chat history stored in database")
    (Bullet "Role-based access control (admin, user, viewer)")
    (Divider)
    (H2 "Database & Persistence")
    (Bullet "PostgreSQL for user data, chat history, and analytics")
    (Bullet "SQLAlchemy/Prisma ORM for type-safe database operations")
    (Bullet "Redis for session caching and rate limiting")
    (Bullet "Database migrations with Alembic")
    (Divider)
    (H2 "Advanced AI Features")
    (Bullet "Model temperature and max_tokens controls in the UI")
    (Bullet "Conversation context (multi-turn chat with full history sent)")
    (Bullet "File upload support (images, documents, code files)")
    (Bullet "Add more models (Claude, Gemini, Llama) as comparison options")
    (Bullet "Model response rating and analytics dashboard")
    (Divider)
    (H2 "Production Hardening")
    (Bullet "Rate limiting per user and per IP")
    (Bullet "API key rotation and secrets management (Azure Key Vault)")
    (Bullet "Structured logging with correlation IDs for request tracing")
    (Bullet "Prometheus metrics + Grafana dashboard")
    (Bullet "Load testing with locust or k6")
    (Divider)
    (H2 "UI/UX Enhancements")
    (Bullet "Conversation branching (fork from any message)")
    (Bullet "Markdown editor for input (preview mode)")
    (Bullet "Export conversations (PDF, Markdown, JSON)")
    (Bullet "Keyboard shortcuts panel")
    (Bullet "Mobile-responsive design improvements")
    (Bullet "Accessibility audit and WCAG 2.1 AA compliance")
    (Divider)
    (H2 "Infrastructure")
    (Bullet "Kubernetes deployment manifests (Helm charts)")
    (Bullet "Terraform for Azure infrastructure provisioning")
    (Bullet "CDN for frontend static assets")
    (Bullet "Blue-green or canary deployment strategy")
    (Bullet "Automated E2E tests with Playwright")
)

Write-Host "`n========================================"
Write-Host "ALL PAGES CREATED SUCCESSFULLY"
Write-Host "========================================"
Write-Host "Open your Notion page to see the docs:"
Write-Host "https://www.notion.so/Dual-AI-Chat-Project-Docs-3086efb958c38036a0a2f772f5e59158"
