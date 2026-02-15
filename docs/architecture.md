# Architecture

## High-Level Overview

```
┌────────────┐      HTTP/SSE      ┌────────────┐      SDK Calls      ┌──────────────┐
│  Frontend   │ ────────────────→ │  Backend    │ ──────────────────→ │ Azure AI     │
│  (React)    │ ←──────────────── │  (FastAPI)  │ ←────────────────── │ Services     │
└────────────┘                    └────────────┘                      └──────────────┘
```

## Frontend

- **Framework**: React 18 + TypeScript
- **Build tool**: Vite
- **Styling**: Tailwind CSS + Radix UI primitives
- **State management**: React hooks (useChat)
- **Streaming**: SSE via fetch ReadableStream

## Backend

- **Framework**: FastAPI (Python 3.12)
- **AI SDKs**: openai (AsyncAzureOpenAI, AsyncOpenAI)
- **Configuration**: pydantic-settings (.env)
- **Streaming**: Server-Sent Events (text/event-stream)

## Models

| Model | Provider | Endpoint |
|-------|----------|----------|
| GPT-4o-mini | Azure AI Foundry | `*.services.ai.azure.com` |
| DeepSeek-R1 | Azure AI Foundry | `*.services.ai.azure.com` |

## API Contract

### POST /api/v1/chat/completions
Non-streaming chat completion.

### POST /api/v1/chat/stream
Server-Sent Events stream. Each event is a JSON payload:

```json
{ "type": "delta", "content": "chunk of text" }
{ "type": "done", "latency": 1.234, "model": "gpt-4" }
{ "type": "error", "content": "error message" }
```
