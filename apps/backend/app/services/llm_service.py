import httpx
import time
import json
import asyncio
from typing import AsyncGenerator, Dict, Any, List
from fastapi import HTTPException
from app.core.config import settings
from app.schemas.chat import ChatRequest

class BaseLLMService:
    async def get_completion(self, request: ChatRequest) -> Dict[str, Any]:
        raise NotImplementedError

    async def get_streaming_completion(self, request: ChatRequest) -> AsyncGenerator[str, None]:
        raise NotImplementedError

class AzureOpenAIService(BaseLLMService):
    def __init__(self):
        self.api_key = settings.AZURE_KEY
        self.endpoint = settings.AZURE_ENDPOINT.rstrip("/")
        self.deployment = "gpt-4o" 
        self.api_version = "2024-02-15-preview"
        self.url = f"{self.endpoint}/openai/deployments/{self.deployment}/chat/completions?api-version={self.api_version}"

    async def get_completion(self, request: ChatRequest) -> Dict[str, Any]:
        start_time = time.time()
        async with httpx.AsyncClient(timeout=60.0) as client:
            payload = {
                "messages": [
                    {"role": "system", "content": request.system_prompt},
                    {"role": "user", "content": request.message}
                ],
                "temperature": 0.7,
                "max_tokens": 2000
            }
            headers = {"api-key": self.api_key, "Content-Type": "application/json"}
            
            try:
                response = await client.post(self.url, headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()
                latency = time.time() - start_time
                
                return {
                    "reply": data["choices"][0]["message"]["content"],
                    "model": "gpt-4o",
                    "usage": data.get("usage"),
                    "latency": latency
                }
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Azure OpenAI Error: {str(e)}")

    async def get_streaming_completion(self, request: ChatRequest) -> AsyncGenerator[str, None]:
        async with httpx.AsyncClient(timeout=None) as client:
            payload = {
                "messages": [
                    {"role": "system", "content": request.system_prompt},
                    {"role": "user", "content": request.message}
                ],
                "stream": True
            }
            headers = {"api-key": self.api_key, "Content-Type": "application/json"}
            
            async with client.stream("POST", self.url, headers=headers, json=payload) as response:
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        line = line[6:]
                        if line == "[DONE]":
                            break
                        try:
                            data = json.loads(line)
                            delta = data["choices"][0].get("delta", {})
                            if "content" in delta:
                                yield delta["content"]
                        except:
                            continue

class DeepSeekService(BaseLLMService):
    def __init__(self):
        self.api_key = settings.DEEPSEEK_API_KEY
        self.endpoint = settings.DEEPSEEK_ENDPOINT.rstrip("/")
        self.url = f"{self.endpoint}/v1/chat/completions"

    async def get_completion(self, request: ChatRequest) -> Dict[str, Any]:
        start_time = time.time()
        async with httpx.AsyncClient(timeout=60.0) as client:
            payload = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": request.system_prompt},
                    {"role": "user", "content": request.message}
                ],
                "stream": False
            }
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            try:
                response = await client.post(self.url, headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()
                latency = time.time() - start_time
                
                return {
                    "reply": data["choices"][0]["message"]["content"],
                    "model": "deepseek-v3",
                    "usage": data.get("usage"),
                    "latency": latency
                }
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"DeepSeek Error: {str(e)}")

    async def get_streaming_completion(self, request: ChatRequest) -> AsyncGenerator[str, None]:
        async with httpx.AsyncClient(timeout=None) as client:
            payload = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": request.system_prompt},
                    {"role": "user", "content": request.message}
                ],
                "stream": True
            }
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            async with client.stream("POST", self.url, headers=headers, json=payload) as response:
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        line = line[6:]
                        if line == "[DONE]":
                            break
                        try:
                            data = json.loads(line)
                            delta = data["choices"][0].get("delta", {})
                            if "content" in delta:
                                yield delta["content"]
                        except:
                            continue
