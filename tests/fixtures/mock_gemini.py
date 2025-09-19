#!/usr/bin/env python3
"""
Mock Google Gemini API responses for testing
Provides success, error, and edge case scenarios without real API calls
"""

import base64
from unittest.mock import MagicMock
from dataclasses import dataclass
from typing import Optional

# Minimal valid PNG (1x1 transparent pixel) - same as OpenAI mock
TINY_PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGP4BwQACfsD/IbLr9YAAAAASUVORK5CYII="
)

@dataclass
class MockInlineData:
    """Mock structure for Gemini inline image data"""
    data: bytes

@dataclass
class MockContentPart:
    """Mock structure for Gemini content part with image data"""
    inline_data: Optional[MockInlineData] = None

@dataclass
class MockContent:
    """Mock structure for Gemini content container"""
    parts: list

@dataclass
class MockCandidate:
    """Mock structure for Gemini response candidate"""
    content: MockContent

@dataclass
class MockGeminiResponse:
    """Mock structure for Gemini models.generate_content response"""
    candidates: list

def create_mock_gemini_success():
    """Create successful Gemini API mock"""
    mock_client = MagicMock()
    
    # Create response with image data in parts
    mock_response = MockGeminiResponse(
        candidates=[
            MockCandidate(
                content=MockContent(
                    parts=[
                        MockContentPart(
                            inline_data=MockInlineData(data=TINY_PNG)
                        )
                    ]
                )
            )
        ]
    )
    
    mock_client.models.generate_content.return_value = mock_response
    return mock_client

def create_mock_gemini_auth_error():
    """Create Gemini API mock that raises authentication error"""
    mock_client = MagicMock()
    mock_client.models.generate_content.side_effect = Exception("Authentication failed")
    return mock_client

def create_mock_gemini_rate_limit():
    """Create Gemini API mock that raises rate limit error"""
    mock_client = MagicMock()
    mock_client.models.generate_content.side_effect = Exception("Rate limit exceeded")
    return mock_client

def create_mock_gemini_empty_response():
    """Create Gemini API mock that returns no candidates"""
    mock_client = MagicMock()
    mock_response = MockGeminiResponse(candidates=[])
    mock_client.models.generate_content.return_value = mock_response
    return mock_client

def create_mock_gemini_no_image_data():
    """Create Gemini API mock that returns candidates but no image data"""
    mock_client = MagicMock()
    mock_response = MockGeminiResponse(
        candidates=[
            MockCandidate(
                content=MockContent(
                    parts=[
                        MockContentPart(inline_data=None)  # No image data
                    ]
                )
            )
        ]
    )
    mock_client.models.generate_content.return_value = mock_response
    return mock_client

def create_mock_gemini_empty_parts():
    """Create Gemini API mock that returns candidates with empty parts"""
    mock_client = MagicMock()
    mock_response = MockGeminiResponse(
        candidates=[
            MockCandidate(
                content=MockContent(parts=[])  # Empty parts list
            )
        ]
    )
    mock_client.models.generate_content.return_value = mock_response
    return mock_client