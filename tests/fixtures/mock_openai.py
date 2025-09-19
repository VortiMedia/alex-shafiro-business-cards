#!/usr/bin/env python3
"""
Mock OpenAI API responses for testing
Provides success, error, and edge case scenarios without real API calls
"""

import base64
from unittest.mock import MagicMock
from dataclasses import dataclass
from typing import Optional

# Minimal valid PNG (1x1 transparent pixel)
TINY_PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGP4BwQACfsD/IbLr9YAAAAASUVORK5CYII="
)

@dataclass
class MockOpenAIImageData:
    """Mock structure for OpenAI image response data"""
    b64_json: Optional[str] = None

@dataclass 
class MockOpenAIResponse:
    """Mock structure for OpenAI images.generate response"""
    data: list

def create_mock_openai_success():
    """Create successful OpenAI API mock"""
    mock_client = MagicMock()
    
    # Create response with base64 encoded tiny PNG
    mock_response = MockOpenAIResponse(
        data=[MockOpenAIImageData(b64_json=base64.b64encode(TINY_PNG).decode())]
    )
    
    mock_client.images.generate.return_value = mock_response
    return mock_client

def create_mock_openai_auth_error():
    """Create OpenAI API mock that raises authentication error"""
    mock_client = MagicMock()
    mock_client.images.generate.side_effect = Exception("Authentication failed")
    return mock_client

def create_mock_openai_rate_limit():
    """Create OpenAI API mock that raises rate limit error"""
    mock_client = MagicMock()
    mock_client.images.generate.side_effect = Exception("Rate limit exceeded")
    return mock_client

def create_mock_openai_empty_response():
    """Create OpenAI API mock that returns empty data"""
    mock_client = MagicMock()
    mock_response = MockOpenAIResponse(data=[])
    mock_client.images.generate.return_value = mock_response
    return mock_client

def create_mock_openai_invalid_b64():
    """Create OpenAI API mock that returns invalid base64 data"""
    mock_client = MagicMock()
    mock_response = MockOpenAIResponse(
        data=[MockOpenAIImageData(b64_json="invalid_base64_data")]
    )
    mock_client.images.generate.return_value = mock_response
    return mock_client