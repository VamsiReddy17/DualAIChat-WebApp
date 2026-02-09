# 🚀 Dual AI Chat - Professional Edition

A modern, full-stack web application that integrates **GPT-4o** (Azure OpenAI) and **DeepSeek-V3** into a unified interface. Compare responses from both AI models side-by-side in real-time with advanced features like streaming, performance metrics, and customizable system prompts.

![Dual AI Chat Interface](https://github.com/user-attachments/assets/899c00be-1b63-4f5e-9f49-9ff068b2049c)

## ✨ Features

### 🎨 Modern UI/UX
- **Dual View Mode**: Side-by-side comparison of GPT-4o and DeepSeek-V3 responses
- **Single Model Mode**: Focus on one model at a time (GPT-4o or DeepSeek)
- **Glassmorphism Design**: Beautiful, modern UI with backdrop blur effects
- **Dark/Light Theme**: Seamless theme switching with persistent preferences
- **Responsive Design**: Mobile-first layout that adapts to all screen sizes
- **Smooth Animations**: Framer Motion powered transitions and micro-interactions

### 💬 Advanced Chat Features
- **Real-Time Streaming**: Responses appear as they're generated (no waiting for full completion)
- **Syntax Highlighting**: Beautiful code block rendering with Prism.js (VS Code Dark Plus theme)
- **Markdown Support**: Full markdown rendering with tables, lists, and formatted text
- **Chat History**: Persistent conversation history with localStorage
- **System Prompt Configuration**: Set custom personas for both models via a configuration dialog
- **Performance Metrics**: Real-time latency tracking and token usage display
- **Message Actions**: Copy, regenerate, and feedback (thumbs up/down) for each response

### 🏗️ Architecture

#### Backend (FastAPI)
- **Service-Oriented Architecture**: Modular, maintainable codebase
- **LLM Service Layer**: Separate services for Azure OpenAI and DeepSeek
- **Streaming Support**: Efficient Server-Sent Events (SSE) for real-time responses
- **Pydantic Schemas**: Type-safe request/response validation
- **Error Handling**: Robust error handling with detailed error messages
- **Latency Tracking**: Automatic performance measurement for each request

#### Frontend (React + TypeScript + Vite)
- **Custom Hooks**: Centralized chat logic via `useChat` hook
- **Type Safety**: Full TypeScript coverage with strict mode
- **Component Library**: shadcn/ui components for consistent design
- **State Management**: React hooks with localStorage persistence
- **Code Splitting**: Optimized bundle sizes with Vite

## 📁 Project Structure

```
DualAIChat-WebApp/
├── apps/
│   ├── backend/                 # FastAPI Backend
│   │   ├── app/
│   │   │   ├── api/
│   │   │   │   └── v1/
│   │   │   │       └── endpoints/
│   │   │   │           └── chat.py      # API endpoints
│   │   │   ├── core/
│   │   │   │   └── config.py            # Configuration & settings
│   │   │   ├── schemas/
│   │   │   │   └── chat.py              # Pydantic models
│   │   │   ├── services/
│   │   │   │   └── llm_service.py       # LLM service layer
│   │   │   └── main.py                  # FastAPI app
│   │   ├── run.py                        # Server entry point
│   │   └── venv/                         # Python virtual environment
│   │
│   └── frontend/                # React Frontend
│       ├── src/
│       │   ├── api/
│       │   │   └── chat.ts              # API client
│       │   ├── components/
│       │   │   ├── ChatWindow.tsx       # Main chat interface
│       │   │   ├── MessageBubble.tsx    # Message component
│       │   │   ├── ThemeToggle.tsx      # Theme switcher
│       │   │   └── ui/                  # shadcn/ui components
│       │   ├── hooks/
│       │   │   └── useChat.ts           # Chat state management
│       │   ├── lib/
│       │   │   └── utils.ts             # Utility functions
│       │   └── App.tsx                  # Root component
│       ├── package.json
│       └── vite.config.ts
│
└── legacy/                      # Legacy code (deprecated)
    └── ...                      # Old Azure Functions implementation
```

## 🚀 Getting Started

### Prerequisites

- **Python 3.11+**
- **Node.js 18+** and npm
- **Azure OpenAI** API key and endpoint
- **DeepSeek** API key and endpoint

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd apps/backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment:**
   - **Windows:**
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - **Linux/Mac:**
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install fastapi uvicorn httpx pydantic pydantic-settings python-dotenv
   ```

5. **Create `.env` file:**
   ```env
   AZURE_ENDPOINT=https://your-resource.openai.azure.com/
   AZURE_KEY=your-azure-api-key
   DEEPSEEK_ENDPOINT=https://api.deepseek.com
   DEEPSEEK_API_KEY=your-deepseek-api-key
   ```

6. **Run the server:**
   ```bash
   python run.py
   ```
   
   The backend will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd apps/frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start development server:**
   ```bash
   npm run dev
   ```
   
   The frontend will be available at `http://localhost:5173`

## 🔧 Configuration

### Backend Configuration

Edit `apps/backend/app/core/config.py` or set environment variables:

- `AZURE_ENDPOINT`: Your Azure OpenAI endpoint
- `AZURE_KEY`: Your Azure OpenAI API key
- `DEEPSEEK_ENDPOINT`: Your DeepSeek API endpoint
- `DEEPSEEK_API_KEY`: Your DeepSeek API key

### Frontend Configuration

The frontend API base URL is configured in `apps/frontend/src/api/chat.ts`:

```typescript
const API_BASE_URL = 'http://localhost:8000/api/v1';
```

Update this if your backend is running on a different host/port.

## 📡 API Endpoints

### POST `/api/v1/chat/completions`
Send a message to a specific model (non-streaming).

**Request:**
```json
{
  "message": "Explain quantum computing",
  "model": "gpt-4",
  "system_prompt": "You are a helpful assistant."
}
```

**Response:**
```json
{
  "reply": "Quantum computing is...",
  "model": "gpt-4o",
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 150,
    "total_tokens": 160
  },
  "latency": 2.34
}
```

### POST `/api/v1/chat/stream`
Stream a response from a model in real-time.

**Request:** Same as above, with `stream: true`

**Response:** Server-Sent Events (SSE) stream with text chunks

## 🎯 Usage

1. **Select Model Mode:**
   - **Dual View**: Compare both models side-by-side
   - **GPT-4o Only**: Focus on OpenAI's model
   - **DeepSeek Only**: Focus on DeepSeek's model

2. **Configure System Prompt:**
   - Click the gear icon (⚙️) next to the input field
   - Set a custom system prompt to define model behavior
   - Example: "You are a senior Python developer who writes concise, production-ready code"

3. **Send Messages:**
   - Type your message in the input field
   - Press Enter or click the send button
   - Watch responses stream in real-time

4. **View Performance:**
   - Latency is displayed in the message header
   - Token usage appears in the message actions (hover over messages)

5. **Manage History:**
   - Click the history icon to view past conversations
   - Load previous chats or start a new one

## 🛠️ Tech Stack

### Backend
- **FastAPI**: Modern, fast web framework
- **Pydantic**: Data validation using Python type annotations
- **httpx**: Async HTTP client
- **Uvicorn**: ASGI server

### Frontend
- **React 19**: UI library
- **TypeScript**: Type-safe JavaScript
- **Vite**: Next-generation frontend tooling
- **Tailwind CSS**: Utility-first CSS framework
- **shadcn/ui**: High-quality component library
- **Framer Motion**: Animation library
- **React Markdown**: Markdown rendering
- **React Syntax Highlighter**: Code syntax highlighting

## 📝 Development

### Running in Development Mode

**Backend:**
```bash
cd apps/backend
python run.py
```

**Frontend:**
```bash
cd apps/frontend
npm run dev
```

### Building for Production

**Backend:**
The backend runs as-is with Uvicorn. For production, consider using:
- Gunicorn with Uvicorn workers
- Docker containerization
- Cloud deployment (Azure App Service, AWS, etc.)

**Frontend:**
```bash
cd apps/frontend
npm run build
```

The production build will be in `apps/frontend/dist/`

## 🔒 Environment Variables

Create a `.env` file in `apps/backend/`:

```env
# Azure OpenAI Configuration
AZURE_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_KEY=your-azure-api-key-here

# DeepSeek Configuration
DEEPSEEK_ENDPOINT=https://api.deepseek.com
DEEPSEEK_API_KEY=your-deepseek-api-key-here
```

## 🐛 Troubleshooting

### Backend Issues
- **401 Unauthorized**: Check your API keys in `.env`
- **500 Internal Server Error**: Verify endpoint URLs are correct
- **Connection Timeout**: Ensure your endpoints are accessible

### Frontend Issues
- **Blank White Screen**: Check browser console for errors, verify backend is running
- **CORS Errors**: Ensure backend CORS is configured correctly
- **Build Errors**: Run `npm install` again to ensure all dependencies are installed

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues and questions, please open an issue on GitHub.

---

**Built with ❤️ using FastAPI, React, and TypeScript**
