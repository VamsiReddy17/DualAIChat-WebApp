# Setup Guide

## Prerequisites

- Python 3.12+
- Node.js 20+
- Azure AI credentials (see `.env.example`)

## Quick Start (Local Development)

### 1. Clone & configure

```bash
git clone <repo-url>
cd DualAIChat-WebApp
cp .env.example .env
# Edit .env with your Azure credentials
```

### 2. Install dependencies

```bash
# Frontend + shared packages (from project root)
npm install

# Backend (Python)
cd apps/backend
python -m venv venv
source venv/bin/activate       # Linux/macOS
# venv\Scripts\Activate.ps1    # Windows PowerShell
pip install -r requirements.txt
```

### 3. Start backend

```bash
cd apps/backend
python run.py
```

Backend runs at `http://localhost:8000`.

### 4. Start frontend

```bash
cd apps/frontend
npm run dev
```

Frontend runs at `http://localhost:5173`.

## Docker (Production)

```bash
cp .env.example .env
# Fill in your credentials
docker compose up --build -d
```

- Frontend: `http://localhost`
- Backend API: `http://localhost:8000`

## Running Tests

```bash
# Backend
cd apps/backend && python -m pytest tests/ -v

# Frontend
cd apps/frontend && npm run lint && npm run build
```

## Monorepo Structure

This project uses **npm workspaces** to manage shared packages:

- `packages/shared-types` — TypeScript interfaces shared across apps
- `packages/typescript-config` — Base tsconfig files

Install everything from the root with `npm install`.
