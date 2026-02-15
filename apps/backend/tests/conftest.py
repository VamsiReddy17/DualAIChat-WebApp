"""
Shared test fixtures for backend tests.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture()
def client() -> TestClient:
    """Provides a synchronous test client for FastAPI."""
    return TestClient(app)
