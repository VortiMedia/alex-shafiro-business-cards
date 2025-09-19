#!/usr/bin/env python3
"""
Mock Google Gemini API responses for testing
Provides success, error, and edge case scenarios without real API calls

Updated for Sprint 3: Mock images are now validation-compliant (1024x1024)
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

def create_test_png(width=1024, height=1024, color=(10, 10, 10, 255)):
    """Generate validation-compliant PNG for Gemini tests"""
    if not Image:
        # Fallback to tiny PNG if PIL not available
        return base64.b64decode(
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGP4BwQACfsD/IbLr9YAAAAASUVORK5CYII="
        )
    
    img = Image.new('RGBA', (width, height), color)
    buffer = io.BytesIO()
    img.save(buffer, format='PNG', quality=95)
    return buffer.getvalue()

# Square format (1024×1024) - matches Gemini 2.5 Flash Image output
# Deep matte black background to match brand specs (#0A0A0A)
SQUARE_PNG = create_test_png(1024, 1024, (10, 10, 10, 255))

# Fallback tiny PNG for error scenarios
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
    """Create successful Gemini API mock with validation-compliant image"""
    mock_client = MagicMock()
    
    # Create response with validation-compliant image data (1024x1024)
    mock_response = MockGeminiResponse(
        candidates=[
            MockCandidate(
                content=MockContent(
                    parts=[
                        MockContentPart(
                            inline_data=MockInlineData(data=SQUARE_PNG)
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