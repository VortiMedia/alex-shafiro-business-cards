#!/usr/bin/env python3
"""
Mock OpenAI API responses for testing
Provides success, error, and edge case scenarios without real API calls

Updated for Sprint 3: Mock images are now validation-compliant (1536x1024)
"""

import base64
import io
from unittest.mock import MagicMock
from dataclasses import dataclass
from typing import Optional

try:
    from PIL import Image
except ImportError:
    Image = None

def create_test_png(width=1536, height=1024, color=(10, 10, 10, 255)):
    """Generate validation-compliant PNG for business card tests"""
    if not Image:
        # Fallback to tiny PNG if PIL not available
        return base64.b64decode(
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGP4BwQACfsD/IbLr9YAAAAASUVORK5CYII="
        )
    
    img = Image.new('RGBA', (width, height), color)
    buffer = io.BytesIO()
    img.save(buffer, format='PNG', quality=95)
    return buffer.getvalue()

# Business card proportions (1536×1024) - matches OpenAI GPT Image 1 output
# Deep matte black background to match brand specs (#0A0A0A)
BUSINESS_CARD_PNG = create_test_png(1536, 1024, (10, 10, 10, 255))

# Convert to base64 for OpenAI response format
BUSINESS_CARD_B64 = base64.b64encode(BUSINESS_CARD_PNG).decode('utf-8')

# Fallback tiny PNG for error scenarios
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
    """Create successful OpenAI API mock with validation-compliant image"""
    mock_client = MagicMock()
    
    # Create response with base64 encoded business card PNG (1536x1024)
    mock_response = MockOpenAIResponse(
        data=[MockOpenAIImageData(b64_json=BUSINESS_CARD_B64)]
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