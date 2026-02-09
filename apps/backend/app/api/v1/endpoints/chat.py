from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.llm_service import AzureOpenAIService, DeepSeekService
import json
import time

router = APIRouter()

azure_service = AzureOpenAIService()
deepseek_service = DeepSeekService()

@router.post("/completions", response_model=ChatResponse)
async def chat_completion(request: ChatRequest):
    if request.model == "gpt-4":
        return await azure_service.get_completion(request)
    elif request.model == "deepseek":
        return await deepseek_service.get_completion(request)
    else:
        raise HTTPException(status_code=400, detail="Invalid model specified")

@router.post("/stream")
async def chat_stream(request: ChatRequest):
    if request.model == "gpt-4":
        service = azure_service
    elif request.model == "deepseek":
        service = deepseek_service
    else:
        raise HTTPException(status_code=400, detail="Invalid model")

    async def event_generator():
        start_time = time.time()
        async for chunk in service.get_streaming_completion(request):
            yield chunk
        
        # Final metadata chunk (optional, can be used for latency/usage)
        latency = time.time() - start_time
        # We send a special JSON chunk at the end for metadata
        yield f"\n\n--METADATA--\n{json.dumps({'latency': latency, 'model': request.model})}"

    return StreamingResponse(event_generator(), media_type="text/plain")
