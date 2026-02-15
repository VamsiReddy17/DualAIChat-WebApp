import json
import time
import logging
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.schemas.chat import ChatRequest, ChatResponse, ModelName
from app.services.llm_service import AzureOpenAIService, DeepSeekService

logger = logging.getLogger(__name__)

router = APIRouter()

azure_service = AzureOpenAIService()
deepseek_service = DeepSeekService()


def _get_service(model: ModelName):
    if model == ModelName.GPT4:
        return azure_service
    return deepseek_service


@router.post("/completions", response_model=ChatResponse)
async def chat_completion(request: ChatRequest):
    service = _get_service(request.model)
    return await service.get_completion(request)


@router.post("/stream")
async def chat_stream(request: ChatRequest):
    service = _get_service(request.model)

    async def event_generator():
        start_time = time.time()
        try:
            async for chunk in service.get_streaming_completion(request):
                # SSE format: data: {json}\n\n
                payload = json.dumps({"type": "delta", "content": chunk})
                yield f"data: {payload}\n\n"

            latency = time.time() - start_time
            done_payload = json.dumps({
                "type": "done",
                "latency": round(latency, 3),
                "model": request.model.value,
            })
            yield f"data: {done_payload}\n\n"
        except Exception:
            logger.exception("Stream error for model %s", request.model.value)
            error_payload = json.dumps({"type": "error", "content": "An error occurred during streaming."})
            yield f"data: {error_payload}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )
