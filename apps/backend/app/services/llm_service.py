import time
import logging
import asyncio
from typing import AsyncGenerator, Dict, Any
from fastapi import HTTPException
from openai import AsyncAzureOpenAI, AsyncOpenAI, APIError, APITimeoutError
from app.core.config import settings
from app.schemas.chat import ChatRequest

logger = logging.getLogger(__name__)

REQUEST_TIMEOUT = 60  # seconds


class BaseLLMService:
    async def get_completion(self, request: ChatRequest) -> Dict[str, Any]:
        raise NotImplementedError

    async def get_streaming_completion(self, request: ChatRequest) -> AsyncGenerator[str, None]:
        raise NotImplementedError


class AzureOpenAIService(BaseLLMService):
    """Azure AI Foundry - gpt-4o-mini."""

    def __init__(self):
        self.client = AsyncAzureOpenAI(
            api_version=settings.AZURE_API_VERSION,
            azure_endpoint=settings.AZURE_ENDPOINT.rstrip("/") if settings.AZURE_ENDPOINT else "",
            api_key=settings.AZURE_KEY,
            timeout=REQUEST_TIMEOUT,
        )
        self.deployment = settings.AZURE_DEPLOYMENT

    async def get_completion(self, request: ChatRequest) -> Dict[str, Any]:
        start_time = time.time()
        try:
            response = await self.client.chat.completions.create(
                model=self.deployment,
                messages=[
                    {"role": "system", "content": request.system_prompt or ""},
                    {"role": "user", "content": request.message},
                ],
                max_tokens=4096,
                temperature=0.7,
                top_p=1.0,
            )
            latency = time.time() - start_time
            return {
                "reply": response.choices[0].message.content or "",
                "model": self.deployment,
                "usage": response.usage.model_dump() if response.usage else None,
                "latency": round(latency, 3),
            }
        except APITimeoutError:
            logger.error("Azure AI Foundry request timed out")
            raise HTTPException(status_code=504, detail="Azure AI Foundry request timed out. Please try again.")
        except APIError as e:
            logger.error("Azure AI Foundry API error: status=%s", e.status_code)
            raise HTTPException(status_code=502, detail="Azure AI Foundry service error. Please try again.")
        except Exception as e:
            logger.exception("Unexpected Azure AI Foundry error")
            raise HTTPException(status_code=500, detail="An unexpected error occurred with Azure AI Foundry.")

    async def get_streaming_completion(self, request: ChatRequest) -> AsyncGenerator[str, None]:
        try:
            stream = await self.client.chat.completions.create(
                model=self.deployment,
                messages=[
                    {"role": "system", "content": request.system_prompt or ""},
                    {"role": "user", "content": request.message},
                ],
                stream=True,
            )
            async for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except APITimeoutError:
            logger.error("Azure AI Foundry stream timed out")
            yield "\n\n[Error: Request timed out. Please try again.]"
        except APIError as e:
            logger.error("Azure AI Foundry stream API error: status=%s", e.status_code)
            yield "\n\n[Error: Azure AI Foundry service error.]"
        except Exception:
            logger.exception("Unexpected Azure OpenAI stream error")
            yield "\n\n[Error: An unexpected error occurred.]"


class DeepSeekService(BaseLLMService):
    """Azure AI Foundry - DeepSeek-R1 (OpenAI-compatible API)."""

    def __init__(self):
        endpoint = (settings.DEEPSEEK_ENDPOINT or "").rstrip("/")
        if endpoint and "/openai/v1" not in endpoint:
            endpoint = f"{endpoint}/openai/v1"
        api_key = settings.DEEPSEEK_API_KEY or settings.AZURE_KEY
        self.client = AsyncOpenAI(
            base_url=f"{endpoint}/" if endpoint else "",
            api_key=api_key,
            timeout=REQUEST_TIMEOUT,
        )
        self.deployment = settings.DEEPSEEK_DEPLOYMENT

    async def get_completion(self, request: ChatRequest) -> Dict[str, Any]:
        start_time = time.time()
        try:
            completion = await self.client.chat.completions.create(
                model=self.deployment,
                messages=[
                    {"role": "system", "content": request.system_prompt or ""},
                    {"role": "user", "content": request.message},
                ],
            )
            latency = time.time() - start_time
            msg = completion.choices[0].message
            return {
                "reply": msg.content or "",
                "model": self.deployment,
                "usage": completion.usage.model_dump() if completion.usage else None,
                "latency": round(latency, 3),
            }
        except APITimeoutError:
            logger.error("DeepSeek request timed out")
            raise HTTPException(status_code=504, detail="DeepSeek request timed out. Please try again.")
        except APIError as e:
            logger.error("DeepSeek API error: status=%s", e.status_code)
            raise HTTPException(status_code=502, detail="DeepSeek service error. Please try again.")
        except Exception:
            logger.exception("Unexpected DeepSeek error")
            raise HTTPException(status_code=500, detail="An unexpected error occurred with DeepSeek.")

    async def get_streaming_completion(self, request: ChatRequest) -> AsyncGenerator[str, None]:
        try:
            stream = await self.client.chat.completions.create(
                model=self.deployment,
                messages=[
                    {"role": "system", "content": request.system_prompt or ""},
                    {"role": "user", "content": request.message},
                ],
                stream=True,
            )
            async for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except APITimeoutError:
            logger.error("DeepSeek stream timed out")
            yield "\n\n[Error: Request timed out. Please try again.]"
        except APIError as e:
            logger.error("DeepSeek stream API error: status=%s", e.status_code)
            yield "\n\n[Error: DeepSeek service error.]"
        except Exception:
            logger.exception("Unexpected DeepSeek stream error")
            yield "\n\n[Error: An unexpected error occurred.]"
