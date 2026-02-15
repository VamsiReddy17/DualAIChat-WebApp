"""
Tests for LLM service layer.
"""

from app.services.llm_service import AzureOpenAIService, DeepSeekService


def test_azure_service_instantiation():
    """AzureOpenAIService should instantiate without error."""
    service = AzureOpenAIService()
    assert service is not None


def test_deepseek_service_instantiation():
    """DeepSeekService should instantiate without error."""
    service = DeepSeekService()
    assert service is not None
