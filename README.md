# Dual AI Chat

> Enterprise-grade side-by-side AI comparison platform powered by Azure OpenAI (GPT-4o) and Azure AI Foundry (DeepSeek-R1).

---

## Monorepo Structure

```
DualAIChat-WebApp/
├── apps/
│   ├── backend/                        # Python FastAPI service
│   │   ├── app/
│   │   │   ├── __init__.py
│   │   │   ├── main.py                 # Application entry point
│   │   │   ├── api/
│   │   │   │   └── v1/
│   │   │   │       └── endpoints/
│   │   │   │           └── chat.py     # Chat endpoints
│   │   │   ├── core/
│   │   │   │   ├── config.py           # Pydantic-settings config
│   │   │   │   └── logging.py          # Centralized logging
│   │   │   ├── middleware/
│   │   │   │   └── request_logging.py  # Request/response logger
│   │   │   ├── schemas/
│   │   │   │   └── chat.py             # Request/response models
│   │   │   └── services/
│   │   │       └── llm_service.py      # Azure AI SDK clients
│   │   ├── tests/
│   │   │   ├── conftest.py
│   │   │   ├── api/
│   │   │   └── services/
│   │   ├── Dockerfile
│   │   ├── pytest.ini
│   │   ├── requirements.txt
│   │   └── run.py
│   │
│   └── frontend/                       # React + Vite SPA
│       ├── src/
│       │   ├── api/                    # API client layer
│       │   ├── components/
│       │   │   ├── chat/               # Chat feature components
│       │   │   ├── layout/             # App shell components
│       │   │   └── ui/                 # Shared UI primitives
│       │   ├── constants/
│       │   ├── hooks/
│       │   ├── lib/
│       │   ├── styles/
│       │   ├── types/
│       │   ├── App.tsx
│       │   └── main.tsx
│       ├── Dockerfile
│       ├── nginx.conf
│       ├── package.json
│       └── vite.config.ts
│
├── packages/                           # Shared workspace packages
│   ├── shared-types/                   # TypeScript types & API contracts
│   │   ├── src/index.ts
│   │   ├── package.json
│   │   └── tsconfig.json
│   └── typescript-config/              # Shared TS compiler options
│       ├── base.json
│       ├── react.json
│       └── package.json
│
├── docs/
│   ├── architecture.md
│   └── setup.md
├── .github/
│   └── workflows/
│       └── ci.yml                      # GitHub Actions pipeline
├── .env.example                        # Env template (no secrets)
├── .gitignore
├── .dockerignore
├── docker-compose.yml
├── Makefile
├── package.json                        # Root — npm workspaces
├── turbo.json                          # Turborepo pipeline config
└── README.md
```

## Quick Start

```bash
# 1. Configure
cp .env.example .env
# Edit .env with your Azure credentials

# 2. Install
npm install                                           # Frontend + packages
cd apps/backend && pip install -r requirements.txt    # Backend

# 3. Run backend
cd apps/backend && python run.py                      # http://localhost:8000

# 4. Run frontend (new terminal)
cd apps/frontend && npm run dev                       # http://localhost:5173
```

## Docker Deploy

```bash
docker compose up --build -d
# Frontend → http://localhost   |   Backend → http://localhost:8000
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, TypeScript, Vite, Tailwind CSS, Radix UI |
| Backend | Python 3.12, FastAPI, Pydantic, OpenAI SDK |
| AI Models | GPT-4o-mini (Azure OpenAI), DeepSeek-R1 (Azure AI Foundry) |
| Streaming | Server-Sent Events (SSE) |
| Monorepo | npm workspaces, Turborepo |
| CI/CD | GitHub Actions |
| Containerization | Docker, Docker Compose, Nginx |

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | API info |
| `GET` | `/health` | Health check with model status |
| `POST` | `/api/v1/chat/completions` | Non-streaming completion |
| `POST` | `/api/v1/chat/stream` | SSE streaming completion |

## License

Private — All rights reserved.
