"""Create detailed sub-subpages inside each Notion section."""
import json, os, time, urllib.request

TOKEN = os.environ.get("NOTION_TOKEN", "")
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}

# Parent page IDs
PAGES = {
    "tech":     "3086efb9-58c3-813a-a5ba-c1a41363f754",
    "arch":     "3086efb9-58c3-818b-8757-c75e24376fc3",
    "backend":  "3086efb9-58c3-810d-8555-f7f22aa23fe4",
    "frontend": "3086efb9-58c3-813b-8c6a-dc69c4f52239",
    "ai":       "3086efb9-58c3-819e-b71a-dd63d4604c59",
    "devops":   "3086efb9-58c3-8115-b7a0-c63191ae236d",
    "api":      "3086efb9-58c3-811f-9b9a-de8e469d0459",
    "phase2":   "3086efb9-58c3-810c-a252-e70efbe1ee8d",
}

def api(method, url, body=None):
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, headers=HEADERS, method=method)
    time.sleep(0.35)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())

def page(parent_id, title, icon, children):
    r = api("POST", "https://api.notion.com/v1/pages", {
        "parent": {"page_id": parent_id},
        "icon": {"type": "emoji", "emoji": icon},
        "properties": {"title": [{"text": {"content": title}}]},
        "children": children[:100],
    })
    pid = r["id"]
    print(f"    + {title}")
    remaining = children[100:]
    while remaining:
        batch, remaining = remaining[:100], remaining[100:]
        api("PATCH", f"https://api.notion.com/v1/blocks/{pid}/children", {"children": batch})
    return pid

def rt(t, bold=False, italic=False, code=False, color=None):
    r = {"type": "text", "text": {"content": t}}
    ann = {}
    if bold: ann["bold"] = True
    if italic: ann["italic"] = True
    if code: ann["code"] = True
    if color: ann["color"] = color
    if ann: r["annotations"] = ann
    return r

def h1(t): return {"object":"block","type":"heading_1","heading_1":{"rich_text":[rt(t)]}}
def h2(t): return {"object":"block","type":"heading_2","heading_2":{"rich_text":[rt(t)]}}
def h3(t): return {"object":"block","type":"heading_3","heading_3":{"rich_text":[rt(t)]}}
def p(*parts):
    rts = [rt(x) if isinstance(x, str) else x for x in parts]
    return {"object":"block","type":"paragraph","paragraph":{"rich_text":rts}}
def bullet(*parts):
    rts = [rt(x) if isinstance(x, str) else x for x in parts]
    return {"object":"block","type":"bulleted_list_item","bulleted_list_item":{"rich_text":rts}}
def num(*parts):
    rts = [rt(x) if isinstance(x, str) else x for x in parts]
    return {"object":"block","type":"numbered_list_item","numbered_list_item":{"rich_text":rts}}
def divider(): return {"object":"block","type":"divider","divider":{}}
def callout(t, icon, color="gray_background"):
    return {"object":"block","type":"callout","callout":{"rich_text":[rt(t)],"icon":{"type":"emoji","emoji":icon},"color":color}}
def co(parts, icon, color="blue_background"):
    rts = [rt(x) if isinstance(x, str) else x for x in parts]
    return {"object":"block","type":"callout","callout":{"rich_text":rts,"icon":{"type":"emoji","emoji":icon},"color":color}}
def code(t, lang="plain text"): return {"object":"block","type":"code","code":{"rich_text":[rt(t)],"language":lang}}
def tbl(rows):
    w = len(rows[0])
    return {"object":"block","type":"table","table":{"table_width":w,"has_column_header":True,"has_row_header":False,
        "children":[{"type":"table_row","table_row":{"cells":[[rt(c)] for c in row]}} for row in rows]}}

# ============================================================
# TECH STACK sub-subpages
# ============================================================
print("\n[Tech Stack] Creating sub-subpages...")

page(PAGES["tech"], "Python & FastAPI Deep Dive", "\U0001F40D", [
    co([rt("Learn why Python + FastAPI is the backbone of our backend and how each component works together.")], "\U0001F393", "green_background"),
    divider(),
    h2("Why Python 3.12?"),
    p("Python 3.12 introduced significant performance improvements (up to 25% faster) and better error messages. For AI applications, Python is unmatched:"),
    bullet(rt("AI/ML ecosystem: ", bold=True), "OpenAI SDK, LangChain, HuggingFace all Python-first"),
    bullet(rt("async/await: ", bold=True), "Native coroutines for non-blocking I/O (critical for API calls to Azure)"),
    bullet(rt("Type hints: ", bold=True), "Full typing support with mypy/pyright for IDE autocomplete"),
    bullet(rt("Community: ", bold=True), "Largest AI developer community, most tutorials and examples"),
    divider(),
    h2("Why FastAPI Over Django?"),
    tbl([
        ["Feature", "FastAPI", "Django", "Flask"],
        ["Async support", "Native", "Limited (3.1+)", "None"],
        ["Request validation", "Automatic (Pydantic)", "Manual forms", "Manual"],
        ["OpenAPI docs", "Auto-generated", "DRF only", "Flask-RESTx"],
        ["Performance", "~15,000 req/s", "~3,000 req/s", "~5,000 req/s"],
        ["Learning curve", "Low", "High", "Low"],
        ["Best for", "APIs", "Full-stack apps", "Simple APIs"],
    ]),
    divider(),
    h2("How FastAPI Works in Our Project"),
    h3("Application Lifecycle"),
    num("Uvicorn starts and imports ", rt("app.main:app", code=True)),
    num("FastAPI creates the ASGI application object"),
    num("Middleware stack is applied: CORS \u2192 RequestLogging \u2192 ExceptionHandler"),
    num("API router mounts endpoints at ", rt("/api/v1/chat/", code=True)),
    num("Uvicorn listens on port 8000 for incoming requests"),
    divider(),
    h3("Request Processing Pipeline"),
    code("Incoming Request\n  \u2502\n  \u251c\u2500\u2500 CORSMiddleware (checks Origin header)\n  \u251c\u2500\u2500 RequestLoggingMiddleware (logs method, path)\n  \u251c\u2500\u2500 Pydantic Validation (validates request body)\n  \u251c\u2500\u2500 Route Handler (chat.py endpoint)\n  \u251c\u2500\u2500 Service Layer (llm_service.py)\n  \u251c\u2500\u2500 Azure AI SDK Call (async)\n  \u2502\n  \u2514\u2500\u2500 Response (JSON or SSE stream)", "plain text"),
    divider(),
    h3("Pydantic Validation Example"),
    p("When a request hits ", rt("POST /api/v1/chat/stream", code=True), ", FastAPI automatically:"),
    num("Parses the JSON body"),
    num("Validates against ChatRequest schema"),
    num("Converts types (string \u2192 ModelName enum)"),
    num("Returns 422 with detailed errors if validation fails"),
    code('# What happens when you send {"model": "invalid"}:\n{\n  "detail": [\n    {\n      "type": "enum",\n      "loc": ["body", "model"],\n      "msg": "Input should be \'gpt-4\' or \'deepseek\'",\n      "input": "invalid"\n    }\n  ]\n}', "json"),
])

page(PAGES["tech"], "React & TypeScript Deep Dive", "\u269B", [
    co([rt("How React 18 and TypeScript work together to create a responsive, type-safe chat interface.")], "\U0001F393", "green_background"),
    divider(),
    h2("Why React 18?"),
    p("React 18 introduced ", rt("concurrent features", bold=True), " which are critical for our streaming UI:"),
    bullet(rt("startTransition: ", bold=True), "Keeps the UI responsive while streaming tokens update the DOM"),
    bullet(rt("Automatic batching: ", bold=True), "Multiple setState calls in stream handlers are batched into one re-render"),
    bullet(rt("Suspense improvements: ", bold=True), "Better loading states for async operations"),
    divider(),
    h2("Why Not Next.js?"),
    tbl([
        ["Consideration", "React SPA", "Next.js"],
        ["SSR needed?", "No (chat has no SEO)", "Yes (blogs, landing)"],
        ["Streaming control", "Full control", "RSC complexity"],
        ["Bundle size", "Smaller", "Larger (framework)"],
        ["Deployment", "Static files + API", "Node.js server"],
        ["Learning curve", "Lower", "Higher"],
    ]),
    p("For a ", rt("real-time chat app", bold=True), ", SSR adds complexity with no benefit. Static SPA + API is simpler and faster."),
    divider(),
    h2("TypeScript Strict Mode"),
    p("We use TypeScript in ", rt("strict mode", code=True), " which enables all strict checks:"),
    code("// tsconfig.app.json\n{\n  \"compilerOptions\": {\n    \"strict\": true,              // Enables all strict checks\n    \"noUnusedLocals\": true,      // Error on unused variables\n    \"noUnusedParameters\": true,  // Error on unused params\n    \"noFallthroughCasesInSwitch\": true,\n    \"verbatimModuleSyntax\": true  // Explicit import types\n  }\n}", "json"),
    divider(),
    h2("Hooks Pattern"),
    p("We follow the ", rt("custom hooks pattern", bold=True), " to separate UI from logic:"),
    code("// useChat.ts - ALL chat logic lives here\nconst {\n  messages,       // Message[]\n  isLoading,      // boolean\n  loadingModels,  // Set<string>\n  sendMessage,    // (text: string) => Promise<void>\n  cancelRequest,  // () => void\n  retryMessage,   // (id: string) => Promise<void>\n  systemPrompt,   // string\n  setSystemPrompt // (prompt: string) => void\n} = useChat(selectedModel);\n\n// ChatWindow.tsx - ONLY renders UI\n// No API calls, no state logic, just JSX", "typescript"),
    divider(),
    h2("State Management Decisions"),
    tbl([
        ["Option", "Verdict", "Reason"],
        ["React hooks (useState/useCallback)", "CHOSEN", "Simple, no extra dependency, sufficient for our needs"],
        ["Redux", "Rejected", "Overkill for single-page chat app"],
        ["Zustand", "Considered", "Good option if state grows in Phase 2"],
        ["React Query", "Phase 2", "Will add for caching/sync when we add persistence"],
    ]),
])

page(PAGES["tech"], "Tailwind CSS & Design System", "\U0001F3A8", [
    co([rt("How Tailwind CSS powers the entire UI with a custom dark/light theme system.")], "\U0001F393", "green_background"),
    divider(),
    h2("Why Tailwind Over CSS Modules?"),
    tbl([
        ["Feature", "Tailwind CSS", "CSS Modules", "Styled Components"],
        ["Bundle size", "Small (purged)", "Medium", "Large (runtime)"],
        ["Speed to build", "Very fast", "Moderate", "Moderate"],
        ["Theming", "CSS vars + class", "CSS vars", "ThemeProvider"],
        ["Learning curve", "Utility names", "CSS knowledge", "JS + CSS"],
        ["Maintainability", "Collocated", "Separate files", "Collocated"],
    ]),
    divider(),
    h2("Theme System"),
    p("Our theme uses ", rt("HSL CSS custom properties", bold=True), " that switch based on a ", rt(".dark", code=True), " class:"),
    code(":root {\n  --background: 0 0% 100%;       /* White */\n  --foreground: 240 10% 3.9%;    /* Near-black */\n  --muted-foreground: 240 5.2% 33.9%;  /* Dark gray (readable!) */\n  --border: 240 5.9% 85%;        /* Visible border */\n}\n\n.dark {\n  --background: 240 10% 3.9%;    /* Near-black */\n  --foreground: 0 0% 98%;        /* Near-white */\n  --muted-foreground: 240 5% 64.9%;  /* Medium gray */\n  --border: 240 3.7% 15.9%;      /* Subtle border */\n}", "css"),
    divider(),
    h2("Light Mode Contrast Fix"),
    p("We discovered that many text elements used extremely low opacity values that were invisible on white backgrounds:"),
    tbl([
        ["Element", "Before (broken)", "After (fixed)"],
        ["Timestamps", "text-muted-foreground/50", "text-muted-foreground"],
        ["Dot separators", "opacity-30", "opacity-50"],
        ["Latency display", "opacity-60", "opacity-80"],
        ["Empty state text", "/40 and /60", "full and /80"],
        ["Placeholder", "/40", "/60"],
        ["Footer text", "/40", "/70"],
    ]),
    p(rt("Rule: ", bold=True), "No text element should have opacity below 60% in light mode."),
    divider(),
    h2("Component Styling Pattern"),
    code("// We use cn() utility to merge Tailwind classes conditionally:\nimport { cn } from '@/lib/utils';\n\n<button className={cn(\n  // Base styles (always applied)\n  \"flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-medium\",\n  // Conditional styles\n  selectedModel === k\n    ? \"bg-background text-foreground shadow-sm\"  // Active\n    : \"text-muted-foreground hover:text-foreground\"  // Inactive\n)}>\n  {icon} {label}\n</button>", "typescript"),
])

# ============================================================
# ARCHITECTURE sub-subpages
# ============================================================
print("\n[Architecture] Creating sub-subpages...")

page(PAGES["arch"], "SSE Streaming Deep Dive", "\u26A1", [
    co([rt("How Server-Sent Events work, why we chose SSE over WebSockets, and how the full streaming pipeline functions.")], "\U0001F393", "green_background"),
    divider(),
    h2("SSE vs WebSocket"),
    tbl([
        ["Feature", "SSE (our choice)", "WebSocket"],
        ["Direction", "Server \u2192 Client only", "Bidirectional"],
        ["Protocol", "HTTP/1.1", "Upgraded connection"],
        ["Reconnection", "Automatic", "Manual"],
        ["Complexity", "Simple", "Complex"],
        ["Proxy support", "Works everywhere", "Needs special config"],
        ["Best for", "AI streaming, live feeds", "Real-time chat, games"],
    ]),
    p(rt("Verdict: ", bold=True), "SSE is perfect for AI streaming because data only flows server\u2192client. No bidirectional channel needed."),
    divider(),
    h2("Backend SSE Implementation"),
    code("# chat.py - How the backend generates SSE events\nasync def event_generator():\n    start_time = time.time()\n    try:\n        async for chunk in service.get_streaming_completion(request):\n            # Each chunk = one token from the AI model\n            payload = json.dumps({\"type\": \"delta\", \"content\": chunk})\n            yield f\"data: {payload}\\n\\n\"  # SSE format\n\n        # Stream complete - send metadata\n        latency = time.time() - start_time\n        done = json.dumps({\n            \"type\": \"done\",\n            \"latency\": round(latency, 3),\n            \"model\": request.model.value,\n        })\n        yield f\"data: {done}\\n\\n\"\n\n    except Exception:\n        error = json.dumps({\"type\": \"error\", \"content\": \"Stream failed.\"})\n        yield f\"data: {error}\\n\\n\"\n\nreturn StreamingResponse(\n    event_generator(),\n    media_type=\"text/event-stream\",\n    headers={\"Cache-Control\": \"no-cache\", \"X-Accel-Buffering\": \"no\"},\n)", "python"),
    divider(),
    h2("Frontend SSE Consumption"),
    code("// chat.ts - How the frontend reads the SSE stream\nconst reader = response.body?.getReader();\nconst decoder = new TextDecoder();\nlet buffer = '';\n\nwhile (true) {\n    const { done, value } = await reader.read();\n    if (done) break;\n\n    buffer += decoder.decode(value, { stream: true });\n    const lines = buffer.split('\\n');\n    buffer = lines.pop() || '';  // Keep incomplete line\n\n    for (const line of lines) {\n        if (!line.trim().startsWith('data: ')) continue;\n        const json = line.trim().slice(6);\n        const event = JSON.parse(json);\n\n        if (event.type === 'delta')  // Append token to message\n        if (event.type === 'done')   // Show latency badge\n        if (event.type === 'error')  // Show error state\n    }\n}", "typescript"),
    divider(),
    h2("SSE Event Protocol"),
    tbl([
        ["Event Type", "Payload", "When Sent"],
        ["delta", '{"type":"delta","content":"token"}', "For each generated token"],
        ["done", '{"type":"done","latency":1.23,"model":"gpt-4"}', "After last token"],
        ["error", '{"type":"error","content":"message"}', "On generation failure"],
    ]),
])

page(PAGES["arch"], "Error Handling Strategy", "\U0001F6E1", [
    co([rt("How errors are caught, logged, and displayed at every layer of the stack.")], "\U0001F393", "green_background"),
    divider(),
    h2("Error Handling Layers"),
    code("Layer 1: Azure AI SDK\n  \u2514\u2500 APITimeoutError \u2192 504 Gateway Timeout\n  \u2514\u2500 APIError \u2192 502 Bad Gateway\n  \u2514\u2500 Unexpected \u2192 500 Internal Error\n\nLayer 2: FastAPI Endpoint\n  \u2514\u2500 Validation Error \u2192 422 (auto by Pydantic)\n  \u2514\u2500 Stream Error \u2192 SSE error event\n\nLayer 3: Global Exception Handler\n  \u2514\u2500 Any uncaught exception \u2192 generic 500\n  \u2514\u2500 NEVER leaks credentials or stack traces\n\nLayer 4: Frontend\n  \u2514\u2500 Network error \u2192 \"Failed to fetch\" message\n  \u2514\u2500 Abort error \u2192 silently ignored (user cancelled)\n  \u2514\u2500 Stream error \u2192 retry button on message\n  \u2514\u2500 JS crash \u2192 ErrorBoundary fallback UI", "plain text"),
    divider(),
    h2("Security Principle"),
    callout("NEVER expose internal details to the client. Error responses are always generic. Real errors are logged server-side only.", "\U0001F512", "red_background"),
    code("# BAD - leaks credentials and internals\nraise HTTPException(500, detail=f\"Azure error: {str(e)}\")\n\n# GOOD - generic message, real error in server logs\nlogger.exception(\"Azure OpenAI error\")\nraise HTTPException(502, detail=\"Azure OpenAI service error. Please try again.\")", "python"),
    divider(),
    h2("Frontend Error Recovery"),
    tbl([
        ["Error Type", "User Sees", "Recovery Action"],
        ["Network failure", "Red error banner", "Auto-retry on reconnect"],
        ["AI generation fail", "Error badge on message", "Click retry button"],
        ["Timeout", "Error badge", "Retry with same prompt"],
        ["User cancels", "Partial response kept", "Send new message"],
        ["JS crash", "ErrorBoundary fallback", "Click Reload App"],
    ]),
])

# ============================================================
# BACKEND sub-subpages
# ============================================================
print("\n[Backend] Creating sub-subpages...")

page(PAGES["backend"], "LLM Services Explained", "\U0001F916", [
    co([rt("Detailed walkthrough of how AzureOpenAIService and DeepSeekService connect to Azure AI.")], "\U0001F393", "green_background"),
    divider(),
    h2("AzureOpenAIService"),
    code("from openai import AsyncAzureOpenAI, APITimeoutError, APIError\n\nclass AzureOpenAIService:\n    def __init__(self):\n        self.client = AsyncAzureOpenAI(\n            azure_endpoint=settings.AZURE_ENDPOINT,\n            api_key=settings.AZURE_KEY,\n            api_version=settings.AZURE_API_VERSION,\n            timeout=REQUEST_TIMEOUT,  # 60s\n        )\n\n    async def get_completion(self, request):\n        response = await self.client.chat.completions.create(\n            model=settings.AZURE_DEPLOYMENT,  # \"gpt-4o-mini\"\n            messages=[\n                {\"role\": \"system\", \"content\": request.system_prompt},\n                {\"role\": \"user\", \"content\": request.message},\n            ],\n            max_tokens=4096,\n            temperature=0.7,\n        )\n        return response.choices[0].message.content\n\n    async def get_streaming_completion(self, request):\n        stream = await self.client.chat.completions.create(\n            ...,  # same params\n            stream=True,\n        )\n        async for chunk in stream:\n            delta = chunk.choices[0].delta.content\n            if delta:\n                yield delta  # One token at a time", "python"),
    divider(),
    h2("DeepSeekService"),
    p("Key difference: Uses ", rt("standard OpenAI client", bold=True), " (not Azure-specific) because Azure AI Foundry uses the OpenAI-compatible API format:"),
    code("from openai import AsyncOpenAI\n\nclass DeepSeekService:\n    def __init__(self):\n        endpoint = settings.DEEPSEEK_ENDPOINT\n        if not endpoint.endswith('/openai/v1'):\n            endpoint += '/openai/v1'  # Required path\n\n        self.client = AsyncOpenAI(\n            base_url=endpoint,\n            api_key=settings.DEEPSEEK_API_KEY or settings.AZURE_KEY,\n            timeout=REQUEST_TIMEOUT,\n        )", "python"),
    divider(),
    h2("Key Differences Between Services"),
    tbl([
        ["Aspect", "AzureOpenAIService", "DeepSeekService"],
        ["SDK Client", "AsyncAzureOpenAI", "AsyncOpenAI"],
        ["Auth", "azure_endpoint + api_key", "base_url + api_key"],
        ["API Version", "Required (2024-12-01)", "Not needed"],
        ["Path", "Auto-handled by SDK", "Must append /openai/v1"],
        ["Deployment", "gpt-4o-mini", "DeepSeek-R1"],
    ]),
])

page(PAGES["backend"], "Configuration & Environment", "\U0001F511", [
    co([rt("How environment variables flow from .env to the running application.")], "\U0001F393", "green_background"),
    divider(),
    h2("Configuration Flow"),
    code(".env file (project root)\n    \u2502\n    \u251c\u2500\u2500 python-dotenv reads the file\n    \u251c\u2500\u2500 Pydantic-Settings validates types\n    \u251c\u2500\u2500 Settings object created (singleton)\n    \u2502\n    \u2514\u2500\u2500 Import anywhere: from app.core.config import settings", "plain text"),
    divider(),
    h2("Path Resolution"),
    p("The .env file lives at the project root, but config.py is deep inside the backend:"),
    code("# apps/backend/app/core/config.py\n#\n# File tree:    config.py \u2192 core \u2192 app \u2192 backend \u2192 apps \u2192 ROOT\n# Levels up:       1        2      3       4        5\n\nROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent\nENV_FILE = ROOT_DIR / '.env'", "python"),
    divider(),
    h2("All Environment Variables"),
    tbl([
        ["Variable", "Required", "Default", "Purpose"],
        ["AZURE_ENDPOINT", "Yes", "None", "Azure OpenAI endpoint URL"],
        ["AZURE_KEY", "Yes", "None", "Azure API key"],
        ["AZURE_API_VERSION", "No", "2024-12-01-preview", "Azure API version"],
        ["AZURE_DEPLOYMENT", "No", "gpt-4o-mini", "Model deployment name"],
        ["DEEPSEEK_ENDPOINT", "Yes*", "None", "Azure AI Foundry endpoint"],
        ["DEEPSEEK_API_KEY", "No", "Falls back to AZURE_KEY", "DeepSeek-specific key"],
        ["DEEPSEEK_DEPLOYMENT", "No", "DeepSeek-R1", "DeepSeek model name"],
        ["PORT", "No", "8000", "Server port"],
        ["BACKEND_CORS_ORIGINS", "No", "[]", "Allowed frontend origins (JSON array)"],
    ]),
    p(rt("*Required only if you want DeepSeek-R1 to work", italic=True)),
])

page(PAGES["backend"], "Middleware & Logging", "\U0001F4DD", [
    co([rt("How request logging, CORS, and error handling middleware protects and monitors the API.")], "\U0001F393", "green_background"),
    divider(),
    h2("Middleware Stack (execution order)"),
    code("Request arrives\n  \u2502\n  1\uFE0F\u20E3 CORSMiddleware\n  \u2502   Checks Origin header\n  \u2502   Adds Access-Control-Allow-* headers\n  \u2502   Handles preflight OPTIONS automatically\n  \u2502\n  2\uFE0F\u20E3 RequestLoggingMiddleware\n  \u2502   Logs: \"GET /health -> 200 (3.1ms)\"\n  \u2502   Measures request duration\n  \u2502\n  3\uFE0F\u20E3 Route Handler\n  \u2502   Pydantic validates body\n  \u2502   Business logic executes\n  \u2502\n  4\uFE0F\u20E3 Global Exception Handler (catches any unhandled error)\n      Returns generic 500\n      Logs full stack trace server-side", "plain text"),
    divider(),
    h2("CORS Configuration"),
    p("CORS allows the frontend (different port) to call the backend:"),
    code("# Always allow these origins\nallow_origins=[\n    \"http://localhost:5173\",    # Vite dev server\n    \"http://localhost:3000\",    # Alternative port\n    \"http://127.0.0.1:5173\",\n    \"http://127.0.0.1:3000\",\n    *settings.BACKEND_CORS_ORIGINS,  # From .env\n]\nallow_methods=[\"*\"]     # GET, POST, OPTIONS, etc.\nallow_headers=[\"*\"]     # Content-Type, Authorization, etc.\nallow_credentials=True  # Cookies (for Phase 2 auth)", "python"),
    divider(),
    h2("Structured Logging"),
    code("# Output format:\n# 2026-02-15 13:11:50 [INFO] app.middleware.request_logging: GET /health -> 200 (3.0ms)\n# 2026-02-15 13:12:01 [INFO] app.middleware.request_logging: POST /api/v1/chat/stream -> 200 (2341.5ms)\n# 2026-02-15 13:12:05 [ERROR] app.services.llm_service: Azure OpenAI request timed out\n\n# Noisy loggers are suppressed:\nlogging.getLogger('httpx').setLevel(logging.WARNING)\nlogging.getLogger('openai').setLevel(logging.WARNING)", "python"),
])

# ============================================================
# FRONTEND sub-subpages
# ============================================================
print("\n[Frontend] Creating sub-subpages...")

page(PAGES["frontend"], "useChat Hook Deep Dive", "\U0001FA9D", [
    co([rt("The core state management hook: how messages flow, how streaming works, and how cancellation is handled.")], "\U0001F393", "green_background"),
    divider(),
    h2("Message Lifecycle"),
    code("1. User clicks Send\n   \u2502\n2. sendMessage(text) called\n   \u251c\u2500 Creates UserMessage { id, role:'user', content }\n   \u251c\u2500 Creates AIMessage(s) { id, role:'assistant', content:'' }\n   \u251c\u2500 Adds all to messages[] state\n   \u251c\u2500 Sets loadingModels = new Set(['gpt-4', 'deepseek'])\n   \u2502\n3. Parallel streaming begins (Promise.all)\n   \u251c\u2500 chatApi.streamMessage(GPT-4o) \u2192 onEvent callbacks\n   \u251c\u2500 chatApi.streamMessage(DeepSeek) \u2192 onEvent callbacks\n   \u2502\n4. For each delta event:\n   \u2514\u2500 updateMsg(id, m => ({...m, content: m.content + token}))\n   \u2514\u2500 React re-renders the MessageBubble\n   \u2502\n5. For done event:\n   \u2514\u2500 updateMsg(id, m => ({...m, latency: 1.234}))\n   \u2514\u2500 Remove model from loadingModels\n   \u2502\n6. All streams complete\n   \u2514\u2500 loadingModels = empty Set\n   \u2514\u2500 isLoading = false", "plain text"),
    divider(),
    h2("Cancellation with AbortController"),
    code("// When user clicks Stop:\nconst cancelRequest = useCallback(() => {\n    abortRef.current?.abort();  // Cancels all in-flight fetch()\n    abortRef.current = null;\n    setLoadingModels(new Set());  // Clears loading state\n}, []);\n\n// The abort signal is passed to every fetch():\nawait fetch(url, { signal: controller.signal });\n\n// AbortError is caught and silently ignored:\ncatch (err) {\n    if (err instanceof DOMException && err.name === 'AbortError') return;\n    // Only real errors are shown to user\n}", "typescript"),
    divider(),
    h2("Retry Logic"),
    p("When an AI message fails, the retry button re-sends the previous user message:"),
    code("const retryMessage = async (messageId) => {\n    // 1. Find the failed message\n    const failed = messages.find(m => m.id === messageId);\n    // 2. Find the user message before it\n    let userText = '';\n    for (let i = idx - 1; i >= 0; i--) {\n        if (messages[i].role === 'user') { userText = messages[i].content; break; }\n    }\n    // 3. Clear the failed message and re-stream\n    updateMsg(messageId, m => ({ ...m, content: '', error: false }));\n    await chatApi.streamMessage({ message: userText, model: failed.model });\n};", "typescript"),
])

page(PAGES["frontend"], "Component Reference", "\U0001F9E9", [
    co([rt("Every component in the frontend with its props, purpose, and key implementation details.")], "\U0001F393", "green_background"),
    divider(),
    h2("ChatWindow.tsx"),
    p(rt("Location: ", bold=True), rt("components/chat/ChatWindow.tsx", code=True)),
    p(rt("Purpose: ", bold=True), "Main application shell. Renders sidebar, header, chat panels, and input area."),
    h3("Key State"),
    tbl([
        ["State", "Type", "Purpose"],
        ["selectedModel", "'both' | 'gpt-4' | 'deepseek'", "Which panels to show"],
        ["input", "string", "Current textarea value"],
        ["history", "ChatSession[]", "Past conversations (localStorage)"],
        ["chatId", "string | null", "Currently loaded session"],
        ["sidebar", "boolean", "Sidebar open/closed"],
        ["online", "boolean", "Backend health status"],
    ]),
    divider(),
    h2("MessageBubble.tsx"),
    p(rt("Location: ", bold=True), rt("components/chat/MessageBubble.tsx", code=True)),
    p(rt("Purpose: ", bold=True), "Renders a single message with markdown, code highlighting, and action buttons."),
    h3("Props"),
    tbl([
        ["Prop", "Type", "Purpose"],
        ["msg", "Message", "The message object to render"],
        ["isUser", "boolean", "true = right-aligned user bubble"],
        ["onRetry", "(() => void) | undefined", "Retry callback for failed messages"],
    ]),
    h3("Sub-components"),
    bullet(rt("Btn", bold=True), " \u2014 Reusable action button (copy, thumbs, retry)"),
    bullet(rt("CopyBtn", bold=True), " \u2014 Code block copy button with Copied! feedback"),
    divider(),
    h2("ErrorBoundary.tsx"),
    p(rt("Location: ", bold=True), rt("components/layout/ErrorBoundary.tsx", code=True)),
    p("React class component that catches any JavaScript error in its subtree. Shows a full-screen fallback with error message and Reload App button."),
    divider(),
    h2("ThemeToggle.tsx & theme-provider.tsx"),
    p("Together these manage dark/light theme:"),
    bullet(rt("theme-provider.tsx", bold=True), " \u2014 React context with theme state, persists to localStorage, applies .dark class to <html>"),
    bullet(rt("ThemeToggle.tsx", bold=True), " \u2014 Button that toggles between light/dark with animated sun/moon icons"),
])

# ============================================================
# AI MODELS sub-subpages
# ============================================================
print("\n[AI Models] Creating sub-subpages...")

page(PAGES["ai"], "GPT-4o-mini Setup & Usage", "\u2728", [
    co([rt("Step-by-step: how GPT-4o-mini is configured, called, and what to know about Azure OpenAI.")], "\U0001F393", "green_background"),
    divider(),
    h2("What is Azure OpenAI Service?"),
    p("Azure OpenAI is Microsoft's hosted version of OpenAI models. You get the same GPT models but with:"),
    bullet(rt("Enterprise security: ", bold=True), "Data stays in your Azure region, no training on your data"),
    bullet(rt("SLA: ", bold=True), "99.9% uptime guarantee"),
    bullet(rt("Compliance: ", bold=True), "SOC 2, HIPAA, GDPR certified"),
    bullet(rt("Network: ", bold=True), "Private endpoints, VNet integration"),
    divider(),
    h2("SDK Configuration"),
    code("from openai import AsyncAzureOpenAI\n\nclient = AsyncAzureOpenAI(\n    azure_endpoint=\"https://your-resource.cognitiveservices.azure.com/\",\n    api_key=\"your-key\",\n    api_version=\"2024-12-01-preview\",\n    timeout=60.0,\n)", "python"),
    divider(),
    h2("Calling the Model"),
    code("response = await client.chat.completions.create(\n    model=\"gpt-4o-mini\",  # deployment name\n    messages=[\n        {\"role\": \"system\", \"content\": \"You are a helpful assistant.\"},\n        {\"role\": \"user\", \"content\": \"Explain quantum computing\"},\n    ],\n    max_tokens=4096,\n    temperature=0.7,\n    stream=True,  # For SSE streaming\n)", "python"),
])

page(PAGES["ai"], "DeepSeek-R1 Setup & Usage", "\U0001F9E0", [
    co([rt("How DeepSeek-R1 works on Azure AI Foundry and why it uses a different SDK client.")], "\U0001F393", "green_background"),
    divider(),
    h2("What is Azure AI Foundry?"),
    p("Azure AI Foundry (formerly Azure AI Studio) hosts third-party models as Model-as-a-Service (MaaS). Unlike Azure OpenAI:"),
    bullet(rt("No deployment step: ", bold=True), "Models are pre-deployed, you just call them"),
    bullet(rt("OpenAI-compatible API: ", bold=True), "Uses standard /v1/chat/completions format"),
    bullet(rt("Pay-per-token: ", bold=True), "No reserved capacity needed"),
    divider(),
    h2("Why Standard OpenAI Client?"),
    p("Azure AI Foundry exposes an ", rt("OpenAI-compatible API", bold=True), ", not the Azure-specific API. So we use the standard client:"),
    code("from openai import AsyncOpenAI  # NOT AsyncAzureOpenAI\n\nclient = AsyncOpenAI(\n    base_url=\"https://your-resource.services.ai.azure.com/openai/v1\",\n    api_key=\"your-key\",\n    timeout=60.0,\n)\n\n# The /openai/v1 path is REQUIRED\n# Without it, you get 404 errors", "python"),
    divider(),
    h2("DeepSeek-R1 Characteristics"),
    tbl([
        ["Feature", "Detail"],
        ["Reasoning style", "Chain-of-thought (shows thinking process)"],
        ["Best at", "Math, logic, complex analysis"],
        ["Response time", "Slower (2.5-4s) due to deeper reasoning"],
        ["Token limit", "Varies by deployment"],
        ["Temperature", "Lower values (0.3-0.5) work best for reasoning"],
    ]),
])

# ============================================================
# DEVOPS sub-subpages
# ============================================================
print("\n[DevOps] Creating sub-subpages...")

page(PAGES["devops"], "Docker Configuration Explained", "\U0001F4E6", [
    co([rt("Line-by-line explanation of both Dockerfiles and docker-compose.yml.")], "\U0001F393", "green_background"),
    divider(),
    h2("Backend Dockerfile (Multi-stage)"),
    code("# Stage 1: Install dependencies in a builder\nFROM python:3.12-slim AS builder\nWORKDIR /build\nCOPY requirements.txt .\nRUN pip install --no-cache-dir --prefix=/install -r requirements.txt\n# Why --prefix? Installs to /install instead of system Python.\n# This lets us copy ONLY the packages to the runtime stage.\n\n# Stage 2: Minimal runtime image\nFROM python:3.12-slim\nWORKDIR /app\nCOPY --from=builder /install /usr/local  # Only packages, no pip/build tools\nCOPY . .  # Copy application code\n\n# Security: Run as non-root user\nRUN addgroup --system app && adduser --system --group app\nUSER app\n\nEXPOSE 8000\nCMD [\"uvicorn\", \"app.main:app\", \"--host\", \"0.0.0.0\", \"--port\", \"8000\"]", "docker"),
    p(rt("Result: ", bold=True), "~180MB image (vs ~900MB if we kept build tools)"),
    divider(),
    h2("Frontend Dockerfile (Multi-stage)"),
    code("# Stage 1: Build the React app\nFROM node:20-alpine AS builder\nWORKDIR /app\nCOPY package.json package-lock.json ./\nRUN npm ci             # Clean install (reproducible)\nCOPY . .\nRUN npm run build      # Produces /app/dist with static files\n\n# Stage 2: Serve with Nginx\nFROM nginx:alpine\nCOPY --from=builder /app/dist /usr/share/nginx/html\nCOPY nginx.conf /etc/nginx/conf.d/default.conf\nEXPOSE 80\nCMD [\"nginx\", \"-g\", \"daemon off;\"]", "docker"),
    p(rt("Result: ", bold=True), "~25MB image (just nginx + static HTML/JS/CSS)"),
    divider(),
    h2("docker-compose.yml Explained"),
    code("services:\n  backend:\n    build: ./apps/backend       # Build from Dockerfile\n    env_file: .env              # Inject all env vars\n    ports: [\"8000:8000\"]\n    healthcheck:                # Docker checks if service is alive\n      test: curl -f http://localhost:8000/health\n      interval: 30s\n\n  frontend:\n    build: ./apps/frontend\n    ports: [\"80:80\"]\n    depends_on:\n      backend:\n        condition: service_healthy  # Won't start until backend is healthy", "yaml"),
])

page(PAGES["devops"], "CI/CD Pipeline Explained", "\U0001F916", [
    co([rt("How GitHub Actions tests every change and what each step does.")], "\U0001F393", "green_background"),
    divider(),
    h2("Pipeline Overview"),
    code("Push/PR to main\n       \u2502\n       \u251c\u2500\u2500 Backend Job (parallel)\n       \u2502    \u251c\u2500 Setup Python 3.12\n       \u2502    \u251c\u2500 Cache pip packages\n       \u2502    \u251c\u2500 pip install requirements.txt pytest httpx\n       \u2502    \u2514\u2500 python -m pytest tests/ -v\n       \u2502\n       \u2514\u2500\u2500 Frontend Job (parallel)\n            \u251c\u2500 Setup Node 20\n            \u251c\u2500 Cache npm packages\n            \u251c\u2500 npm ci (clean install)\n            \u251c\u2500 npm run lint (ESLint)\n            \u2514\u2500 npm run build (Vite production build)\n\nBoth must pass \u2192 PR can be merged", "plain text"),
    divider(),
    h2("What Each Step Catches"),
    tbl([
        ["Step", "Catches", "Example"],
        ["pytest", "Logic errors, API regressions", "Endpoint returns wrong status code"],
        ["npm run lint", "Code quality issues", "Unused imports, missing types"],
        ["npm run build", "TypeScript errors, import issues", "Broken import path after refactor"],
    ]),
    divider(),
    h2("Caching Strategy"),
    p("Both jobs use caching to speed up CI:"),
    bullet(rt("Python: ", bold=True), "pip cache based on requirements.txt hash"),
    bullet(rt("Node: ", bold=True), "npm cache based on package-lock.json hash"),
    p("If dependencies haven't changed, install step is nearly instant."),
])

# ============================================================
# API REFERENCE sub-subpages
# ============================================================
print("\n[API Reference] Creating sub-subpages...")

page(PAGES["api"], "Chat Completions Endpoint", "\U0001F4AC", [
    co([rt("Everything about POST /api/v1/chat/completions \u2014 the non-streaming chat endpoint.")], "\U0001F393", "green_background"),
    divider(),
    h2("Endpoint"),
    p(rt("POST /api/v1/chat/completions", code=True)),
    p("Sends a message to the selected AI model and waits for the complete response before returning."),
    divider(),
    h2("When to Use"),
    bullet("When you need the full response at once (not token-by-token)"),
    bullet("For programmatic/API usage where streaming isn't needed"),
    bullet("For simpler client implementations"),
    divider(),
    h2("Request"),
    code('POST /api/v1/chat/completions\nContent-Type: application/json\n\n{\n  "message": "Explain quantum computing in simple terms",\n  "model": "gpt-4",\n  "system_prompt": "You are a helpful assistant. Keep answers concise."\n}', "json"),
    divider(),
    h2("Response (200 OK)"),
    code('{\n  "reply": "Quantum computing uses quantum bits (qubits) that can be 0, 1, or both simultaneously...",\n  "model": "gpt-4",\n  "usage": {\n    "prompt_tokens": 24,\n    "completion_tokens": 156,\n    "total_tokens": 180\n  },\n  "latency": 2.341\n}', "json"),
    divider(),
    h2("Error Responses"),
    tbl([
        ["Status", "Body", "Cause"],
        ["422", '{"detail":[{"loc":["body","model"],...}]}', "Invalid model or empty message"],
        ["502", '{"detail":"Azure OpenAI service error."}', "Azure API returned error"],
        ["504", '{"detail":"Request timed out."}', "Azure API took > 60 seconds"],
        ["500", '{"detail":"An internal error occurred."}', "Unexpected server error"],
    ]),
    divider(),
    h2("cURL Example"),
    code('curl -X POST http://localhost:8000/api/v1/chat/completions \\\n  -H "Content-Type: application/json" \\\n  -d \'{\n    "message": "Write a haiku about coding",\n    "model": "deepseek",\n    "system_prompt": "You are a creative writer."\n  }\'', "bash"),
])

page(PAGES["api"], "Streaming Endpoint (SSE)", "\u26A1", [
    co([rt("Everything about POST /api/v1/chat/stream \u2014 the real-time streaming endpoint.")], "\U0001F393", "green_background"),
    divider(),
    h2("Endpoint"),
    p(rt("POST /api/v1/chat/stream", code=True)),
    p("Streams AI-generated tokens in real-time using Server-Sent Events. The response starts immediately and tokens arrive as they're generated."),
    divider(),
    h2("When to Use"),
    bullet("The frontend uses this for all chat interactions"),
    bullet("Provides instant feedback (user sees tokens appear)"),
    bullet("Better UX than waiting 2-4 seconds for complete response"),
    divider(),
    h2("Request"),
    code('POST /api/v1/chat/stream\nContent-Type: application/json\n\n{\n  "message": "Write a Python function to sort a list",\n  "model": "gpt-4",\n  "stream": true,\n  "system_prompt": "You are a senior Python developer."\n}', "json"),
    divider(),
    h2("Response Headers"),
    code("Content-Type: text/event-stream\nCache-Control: no-cache\nX-Accel-Buffering: no", "plain text"),
    divider(),
    h2("SSE Event Types"),
    tbl([
        ["Type", "When", "Example Payload"],
        ["delta", "Each generated token", '{"type":"delta","content":"def "}'],
        ["done", "After last token", '{"type":"done","latency":2.1,"model":"gpt-4"}'],
        ["error", "On failure", '{"type":"error","content":"Stream failed."}'],
    ]),
    divider(),
    h2("Full SSE Stream Example"),
    code('data: {"type":"delta","content":"def "}\n\ndata: {"type":"delta","content":"sort_list"}\n\ndata: {"type":"delta","content":"(items"}\n\ndata: {"type":"delta","content":"): "}\n\ndata: {"type":"delta","content":"\\n    return "}\n\ndata: {"type":"delta","content":"sorted(items)"}\n\ndata: {"type":"done","latency":1.876,"model":"gpt-4"}', "plain text"),
    divider(),
    h2("cURL Example"),
    code('# -N flag disables output buffering (required for SSE)\ncurl -N -X POST http://localhost:8000/api/v1/chat/stream \\\n  -H "Content-Type: application/json" \\\n  -d \'{"message": "Hello", "model": "gpt-4", "stream": true}\'', "bash"),
])

print("\n" + "=" * 50)
print("ALL SUB-SUBPAGES CREATED!")
print("=" * 50)
