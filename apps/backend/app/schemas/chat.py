from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from enum import Enum


class ModelName(str, Enum):
    GPT4 = "gpt-4"
    DEEPSEEK = "deepseek"


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=32000, description="User message")
    model: ModelName = ModelName.GPT4
    stream: bool = False
    system_prompt: Optional[str] = Field(
        default="You are a helpful assistant.",
        max_length=4000,
        description="System prompt for the model",
    )


class ChatResponse(BaseModel):
    reply: str
    model: str
    usage: Optional[Dict[str, Any]] = None
    latency: Optional[float] = None
