<div align="center">

<img src="docs/images/banner.png" alt="Dual AI Chat Banner" width="100%" />

<br />

[![License](https://img.shields.io/badge/license-Private-red.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=black)](https://react.dev)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.6-3178C6?logo=typescript&logoColor=white)](https://typescriptlang.org)
[![Tailwind](https://img.shields.io/badge/Tailwind_CSS-3.4-06B6D4?logo=tailwindcss&logoColor=white)](https://tailwindcss.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)](https://docker.com)
[![CI](https://img.shields.io/badge/CI-GitHub_Actions-2088FF?logo=githubactions&logoColor=white)](.github/workflows/ci.yml)

**Compare GPT-4o and DeepSeek-R1 side-by-side in real-time.**

[Getting Started](#-getting-started) &bull; [Architecture](#-architecture) &bull; [Features](#-features) &bull; [API Reference](#-api-reference) &bull; [Contributing](#-contributing)

</div>

---

## What is Dual AI Chat?

**Dual AI Chat** is an enterprise-grade web application that lets you send a single prompt to **two AI models simultaneously** and compare their responses in real-time, side-by-side. Built on **Azure AI Foundry**, it streams responses token-by-token using Server-Sent Events (SSE), so you see answers appear as they're generated.

### Why?

| Problem | Solution |
|---------|----------|
| Switching between ChatGPT and other AI tools is tedious | One prompt, two responses, one screen |
| Hard to evaluate which model is better for a task | Side-by-side comparison with latency metrics |
| No enterprise-ready open-source comparison tool exists | Production-grade monorepo with Docker, CI/CD, tests |
| AI responses feel slow waiting for completion | Real-time SSE streaming shows tokens as they arrive |

---

## Screenshots

<div align="center">

### Dark Mode
<img src="docs/images/ui-dark.png" alt="Dual AI Chat — Dark Mode" width="90%" />

<br /><br />

### Light Mode
<img src="docs/images/ui-light.png" alt="Dual AI Chat — Light Mode" width="90%" />

</div>

### UI Features at a Glance

- **Dual View** — See both AI responses simultaneously
- **Single View** — Focus on one model at a time (GPT-4o or DeepSeek-R1)
- **Dark/Light Theme** — Toggle with smooth transitions, persisted to localStorage
- **Streaming Responses** — Tokens appear in real-time as they're generated
- **Markdown Rendering** — Code blocks with syntax highlighting (Prism.js)
- **Chat History** — Conversations saved locally with quick-access sidebar
- **System Prompt Editor** — Customize the AI's behavior per conversation
- **Copy/Retry/Cancel** — Full message action toolbar
- **Responsive** — Works on desktop and tablet viewports
- **Keyboard Shortcuts** — `Enter` to send, `Shift+Enter` for new line

---

## Architecture

<div align="center">
<img src="docs/images/architecture.png" alt="System Architecture" width="90%" />
</div>

<br />

### How It Works

```
User types a message
       |
       v
  React Frontend (Vite SPA)
       |
       | POST /api/v1/chat/stream  (fetch + ReadableStream)
       v
  FastAPI Backend
       |
       |--- CORSMiddleware (validates origin)
       |--- RequestLoggingMiddleware (logs timing)
       |--- Pydantic validation (validates request body)
       v
  LLM Service Layer
       |
       +---> AzureOpenAIService ---> Azure AI Foundry (GPT-4o-mini)
       |         (AsyncAzureOpenAI SDK)
       |
       +---> DeepSeekService ------> Azure AI Foundry (DeepSeek-R1)
                 (AsyncOpenAI SDK)
       |
       v
  SSE Stream (token-by-token)
       |
       v
  React renders each token in real-time
```

### Request Flow

1. **Frontend** sends a `POST` request with the user's message and selected model
2. **CORS middleware** validates the request origin
3. **Request logging** captures method, path, and starts a timer
4. **Pydantic** validates the request body against the `ChatRequest` schema
5. **LLM Service** selects the correct Azure AI Foundry client for the chosen model
6. **Azure SDK** streams tokens back using async generators
7. **FastAPI** wraps each token in an SSE event (`data: {"type":"delta","content":"..."}`)
8. **Frontend** reads the stream and appends each token to the message bubble
9. **Done event** carries latency and model metadata for the UI badge

---

## Tech Stack

### Backend

| Technology | Version | Purpose |
|-----------|---------|---------|
| **Python** | 3.12 | Runtime — 25% faster than 3.11 |
| **FastAPI** | 0.115+ | Async web framework with auto-generated OpenAPI docs |
| **Pydantic** | 2.x | Request/response validation with type safety |
| **OpenAI SDK** | 1.x | `AsyncAzureOpenAI` + `AsyncOpenAI` for Azure endpoints |
| **Uvicorn** | 0.34+ | ASGI server with HTTP/1.1 support |
| **python-dotenv** | 1.x | Environment variable loading from `.env` |

### Frontend

| Technology | Version | Purpose |
|-----------|---------|---------|
| **React** | 18.x | UI library with concurrent rendering |
| **TypeScript** | 5.6 | Strict type safety across the codebase |
| **Vite** | 6.x | Build tool — instant HMR, optimized production builds |
| **Tailwind CSS** | 3.4 | Utility-first CSS with HSL custom property theming |
| **Radix UI** | Latest | Accessible, unstyled UI primitives (Dialog, ScrollArea) |
| **Framer Motion** | Latest | Smooth animations for sidebar, messages, transitions |
| **Prism.js** | Latest | Syntax highlighting in AI-generated code blocks |

### Infrastructure

| Technology | Purpose |
|-----------|---------|
| **Docker** | Multi-stage builds for both frontend and backend |
| **Docker Compose** | One-command orchestration with health checks |
| **Nginx** | Serves static frontend + reverse proxies API requests |
| **GitHub Actions** | CI pipeline — lint, test, build on every push/PR |
| **npm Workspaces** | Monorepo dependency management |
| **Turborepo** | Intelligent build caching and task orchestration |
| **Makefile** | Developer task shortcuts (`make dev-backend`, `make test`) |

### AI Models

| Model | Provider | Strengths |
|-------|----------|-----------|
| **GPT-4o-mini** | Azure AI Foundry | Fast, versatile, great for general tasks |
| **DeepSeek-R1** | Azure AI Foundry | Deep chain-of-thought reasoning, math, logic |

---

## Getting Started

### Prerequisites

- **Python 3.11+** ([python.org](https://python.org))
- **Node.js 18+** ([nodejs.org](https://nodejs.org))
- **Azure account** with an Azure AI Foundry resource (GPT-4o-mini and DeepSeek-R1 deployed)

### 1. Clone & Configure

```bash
git clone https://github.com/VamsiReddy17/DualAIChat-WebApp.git
cd DualAIChat-WebApp

# Create environment file from template
cp .env.example .env
```

Edit `.env` with your Azure credentials:

```env
# Azure AI Foundry — GPT-4o-mini
AZURE_ENDPOINT=https://your-resource.services.ai.azure.com/
AZURE_KEY=your-azure-api-key
AZURE_API_VERSION=2024-12-01-preview
AZURE_DEPLOYMENT=gpt-4o-mini

# Azure AI Foundry — DeepSeek-R1
DEEPSEEK_ENDPOINT=https://your-resource.services.ai.azure.com
DEEPSEEK_API_KEY=your-deepseek-api-key
DEEPSEEK_DEPLOYMENT=DeepSeek-R1
```

### 2. Install Dependencies

```bash
# Frontend + shared packages (from project root)
npm install

# Backend (Python)
cd apps/backend
pip install -r requirements.txt
cd ../..
```

### 3. Start Development Servers

**Option A — Using Makefile (recommended):**

```bash
make dev-backend    # Terminal 1 → http://localhost:8000
make dev-frontend   # Terminal 2 → http://localhost:5173
```

**Option B — Manual:**

```bash
# Terminal 1: Backend
cd apps/backend && python run.py

# Terminal 2: Frontend
cd apps/frontend && npm run dev
```

### 4. Open the App

Navigate to **http://localhost:5173** — you should see the Dual AI Chat interface.

---

## Docker Deployment

Deploy both services with a single command:

```bash
# Build and start
docker compose up --build -d

# Check status
docker compose ps

# View logs
docker compose logs -f

# Stop
docker compose down
```

| Service | URL | Container |
|---------|-----|-----------|
| Frontend | http://localhost | `dualai-frontend` (Nginx) |
| Backend | http://localhost:8000 | `dualai-backend` (Uvicorn) |

The frontend Nginx container proxies `/api/` and `/health` requests to the backend automatically.

---

## API Reference

### Health Check

```http
GET /health
```

**Response (200):**
```json
{
  "status": "healthy",
  "models": {
    "gpt-4o-mini": "available",
    "deepseek-r1": "available"
  }
}
```

### Chat Completion (Non-Streaming)

```http
POST /api/v1/chat/completions
Content-Type: application/json

{
  "message": "Explain quantum computing",
  "model": "gpt-4",
  "system_prompt": "You are a helpful assistant."
}
```

### Chat Streaming (SSE)

```http
POST /api/v1/chat/stream
Content-Type: application/json

{
  "message": "Write a Python sort function",
  "model": "deepseek",
  "stream": true
}
```

**SSE Events:**

| Event Type | Payload | When |
|-----------|---------|------|
| `delta` | `{"type":"delta","content":"token"}` | Each generated token |
| `done` | `{"type":"done","latency":1.23,"model":"gpt-4"}` | Stream complete |
| `error` | `{"type":"error","content":"message"}` | On failure |

**cURL Example:**
```bash
curl -N -X POST http://localhost:8000/api/v1/chat/stream \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!", "model": "gpt-4", "stream": true}'
```

---

## Project Structure

```
DualAIChat-WebApp/
├── apps/
│   ├── backend/                        # Python FastAPI service
│   │   ├── app/
│   │   │   ├── main.py                 # Application entry, CORS, middleware
│   │   │   ├── api/v1/endpoints/       # Route handlers
│   │   │   │   └── chat.py            # /chat/completions & /chat/stream
│   │   │   ├── core/
│   │   │   │   ├── config.py           # Pydantic-settings (.env loader)
│   │   │   │   └── logging.py          # Structured logging setup
│   │   │   ├── middleware/
│   │   │   │   └── request_logging.py  # Request timing middleware
│   │   │   ├── schemas/
│   │   │   │   └── chat.py             # ChatRequest/ChatResponse models
│   │   │   └── services/
│   │   │       └── llm_service.py      # AzureOpenAI + DeepSeek clients
│   │   ├── tests/                      # pytest test suite
│   │   ├── Dockerfile                  # Multi-stage production build
│   │   ├── requirements.txt
│   │   └── run.py                      # Dev server launcher
│   │
│   └── frontend/                       # React + Vite SPA
│       ├── src/
│       │   ├── api/chat.ts             # HTTP client + SSE stream reader
│       │   ├── components/
│       │   │   ├── chat/               # ChatWindow, MessageBubble
│       │   │   ├── layout/             # ThemeToggle, ErrorBoundary
│       │   │   └── ui/                 # Button, Dialog, DualAILogo
│       │   ├── hooks/useChat.ts        # Core chat state management
│       │   ├── styles/globals.css      # HSL theme variables
│       │   └── App.tsx                 # Root component
│       ├── Dockerfile                  # Multi-stage → Nginx
│       ├── nginx.conf                  # SPA routing + API proxy
│       └── vite.config.ts
│
├── packages/                           # Shared workspace packages
│   ├── shared-types/                   # TypeScript API contracts
│   └── typescript-config/              # Base + React tsconfig
│
├── scripts/                            # Automation scripts
│   ├── notion-docs.py                  # Notion documentation generator
│   ├── notion-subpages.py              # Sub-subpage builder
│   └── notion-icons.py                 # Page icon updater
│
├── docs/
│   ├── images/                         # README images
│   ├── architecture.md                 # Detailed architecture docs
│   └── setup.md                        # Step-by-step setup guide
│
├── archive/legacy/                     # Previous version (reference)
│
├── .github/workflows/ci.yml           # GitHub Actions CI pipeline
├── docker-compose.yml                  # Container orchestration
├── Makefile                            # Developer task runner
├── turbo.json                          # Turborepo config
├── package.json                        # npm workspaces root
└── .env.example                        # Environment template
```

---

## Available Commands

### Makefile

| Command | Description |
|---------|-------------|
| `make dev-backend` | Start FastAPI dev server with auto-reload |
| `make dev-frontend` | Start Vite dev server with HMR |
| `make install` | Install all dependencies (Python + Node) |
| `make test-backend` | Run pytest on backend |
| `make lint-frontend` | Run ESLint on frontend |
| `make docker-up` | Build & start Docker containers |
| `make docker-down` | Stop & remove containers |
| `make clean` | Remove all build artifacts and caches |
| `make help` | Show all available commands |

---

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `AZURE_ENDPOINT` | Yes | — | Azure AI Foundry endpoint URL |
| `AZURE_KEY` | Yes | — | Azure AI Foundry API key |
| `AZURE_API_VERSION` | No | `2024-12-01-preview` | Azure API version |
| `AZURE_DEPLOYMENT` | No | `gpt-4o-mini` | GPT deployment name |
| `DEEPSEEK_ENDPOINT` | Yes* | — | Azure AI Foundry endpoint |
| `DEEPSEEK_API_KEY` | No | Falls back to `AZURE_KEY` | DeepSeek API key |
| `DEEPSEEK_DEPLOYMENT` | No | `DeepSeek-R1` | DeepSeek model name |
| `PORT` | No | `8000` | Backend server port |
| `BACKEND_CORS_ORIGINS` | No | `[]` | Additional allowed origins (JSON) |
| `NOTION_TOKEN` | No | — | Notion API token (for doc scripts) |

*Required only for DeepSeek-R1 functionality.

---

## Documentation

Full documentation is maintained in **Notion** with 9 main sections and 16+ sub-pages:

| Section | Topics Covered |
|---------|---------------|
| **Tech Stack & Tools** | Python/FastAPI deep dive, React/TS patterns, Tailwind theming |
| **Architecture** | SSE streaming flow, error handling strategy, monorepo decisions |
| **Backend** | LLM services, config management, middleware pipeline |
| **Frontend** | useChat hook, component reference, state management |
| **AI Models** | GPT-4o-mini setup, DeepSeek-R1 setup, Azure configuration |
| **DevOps** | Docker multi-stage builds, CI/CD pipeline, Nginx config |
| **API Reference** | Endpoint specs, SSE protocol, error codes |
| **Phase 1** | Summary of everything built |
| **Phase 2** | Roadmap and planned features |

---

## Roadmap (Phase 2)

- [ ] **Authentication** — Azure AD / OAuth 2.0 login
- [ ] **Conversation persistence** — PostgreSQL + Prisma
- [ ] **Additional models** — Claude, Gemini, Llama via Azure
- [ ] **Prompt templates** — Saved system prompts library
- [ ] **Export conversations** — PDF, Markdown, JSON
- [ ] **Usage analytics** — Token counts, costs, response time charts
- [ ] **Rate limiting** — Per-user quotas with Redis
- [ ] **WebSocket upgrade** — Bidirectional real-time communication
- [ ] **Mobile responsive** — Full mobile-first redesign
- [ ] **Admin dashboard** — Model configuration, user management

---

## Contributing

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feat/amazing-feature`
3. **Commit** your changes: `git commit -m "feat: add amazing feature"`
4. **Push** to the branch: `git push origin feat/amazing-feature`
5. **Open** a Pull Request

Please follow the existing code style and include tests for new features.

---

## License

**Private** — All rights reserved. This project is not open-source.

---

<div align="center">

**Built with Azure AI Foundry, React, and FastAPI**

<sub>Phase 1 Complete &bull; Designed for enterprise-grade AI comparison</sub>

</div>
