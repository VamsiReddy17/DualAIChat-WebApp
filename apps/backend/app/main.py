import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api.v1.endpoints import chat
from app.core.config import settings
from app.core.logging import setup_logging
from app.middleware.request_logging import RequestLoggingMiddleware

# Configure structured logging
setup_logging()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# CORS - allow frontend origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://127.0.0.1:3000",
        *[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logging.getLogger(__name__).exception("Unhandled error on %s %s", request.method, request.url.path)
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred."},
    )


app.add_middleware(RequestLoggingMiddleware)

app.include_router(chat.router, prefix=f"{settings.API_V1_STR}/chat", tags=["chat"])


@app.get("/")
def root():
    return {"message": "Welcome to Dual AI Chat API", "version": "2.1"}


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "models": {
            "azure_openai": bool(settings.AZURE_KEY and settings.AZURE_ENDPOINT),
            "deepseek": bool(settings.DEEPSEEK_ENDPOINT and (settings.DEEPSEEK_API_KEY or settings.AZURE_KEY)),
        },
    }
