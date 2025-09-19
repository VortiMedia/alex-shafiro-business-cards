#!/usr/bin/env python3
"""
Integration tests for ModernHybridWorkflow

Tests the complete generation workflow with mocked API responses.
Validates end-to-end functionality without real API costs.
"""

import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch
import sys

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent / "src"))

from hybrid.modern_workflow import ModernHybridWorkflow, ModelType, GenerationResult
from fixtures.mock_openai import (
    create_mock_openai_success,
    create_mock_openai_auth_error,
    create_mock_openai_rate_limit,
    create_mock_openai_empty_response,
    TINY_PNG
)
from fixtures.mock_gemini import (
    create_mock_gemini_success,
    create_mock_gemini_auth_error,
    create_mock_gemini_rate_limit,
    create_mock_gemini_empty_response
)


class TestSuccessfulGeneration:
    """Test successful image generation scenarios"""
    
    def test_generate_card_production_uses_gpt(self, monkeypatch, tmp_path):
        """Production quality should use GPT Image 1 when available"""
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test123456789012345678")
        monkeypatch.setenv("GOOGLE_API_KEY", "AIza1234567890123456789")
        
        with patch('hybrid.modern_workflow.OpenAI') as mock_openai_class, \
             patch('hybrid.modern_workflow.genai') as mock_gemini_module:
            
            # Setup successful mocks
            mock_openai_class.return_value = create_mock_openai_success()
            mock_gemini_module.Client.return_value = create_mock_gemini_success()
            
            wf = ModernHybridWorkflow()
            wf.production_dir = tmp_path
            wf.drafts_dir = tmp_path
            
            result = wf.generate_card(
                "Clinical-Precision", 
                "front", 
                model=ModelType.AUTO, 
                quality="production"
            )
            
            assert result.success is True
            assert result.model_used == "gpt-image-1"
            assert result.cost_estimate > 0
            assert result.filepath is not None
            assert Path(result.filepath).exists()
    
    def test_generate_card_draft_uses_gemini(self, monkeypatch, tmp_path):
        """Draft quality should use Gemini when available"""
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test123456789012345678")
        monkeypatch.setenv("GOOGLE_API_KEY", "AIza1234567890123456789")
        
        with patch('hybrid.modern_workflow.OpenAI') as mock_openai_class, \
             patch('hybrid.modern_workflow.genai') as mock_gemini_module:
            
            # Setup successful mocks
            mock_openai_class.return_value = create_mock_openai_success()
            mock_gemini_module.Client.return_value = create_mock_gemini_success()
            
            wf = ModernHybridWorkflow()
            wf.production_dir = tmp_path
            wf.drafts_dir = tmp_path
            
            result = wf.generate_card(
                "Athletic-Edge",
                "back", 
                model=ModelType.AUTO, 
                quality="draft"
            )
            
            assert result.success is True
            assert result.model_used == "gemini-2.5-flash-image-preview"
            assert result.cost_estimate == 0.005  # Gemini cost
            assert result.filepath is not None
            assert Path(result.filepath).exists()
    
    def test_specific_model_request_honored(self, monkeypatch, tmp_path):
        """Specific model requests should be honored"""
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test123456789012345678")
        monkeypatch.setenv("GOOGLE_API_KEY", "AIza1234567890123456789")
        
        with patch('hybrid.modern_workflow.OpenAI') as mock_openai_class, \
             patch('hybrid.modern_workflow.genai') as mock_gemini_module:
            
            # Setup successful mocks
            mock_openai_class.return_value = create_mock_openai_success()
            mock_gemini_module.Client.return_value = create_mock_gemini_success()
            
            wf = ModernHybridWorkflow()
            wf.production_dir = tmp_path
            wf.drafts_dir = tmp_path
            
            # Force Gemini for production (normally would use GPT)
            result = wf.generate_card(
                "Luxury-Wellness",
                "front",
                model=ModelType.GEMINI_FLASH,
                quality="production"
            )
            
            assert result.success is True
            assert result.model_used == "gemini-2.5-flash-image-preview"
            assert result.cost_estimate == 0.005
    
    def test_file_naming_convention(self, monkeypatch, tmp_path):
        """Generated files should follow naming convention"""
        monkeypatch.setenv("GOOGLE_API_KEY", "AIza1234567890123456789")
        
        with patch('hybrid.modern_workflow.genai') as mock_gemini_module:
            mock_gemini_module.Client.return_value = create_mock_gemini_success()
            
            wf = ModernHybridWorkflow()
            wf.drafts_dir = tmp_path
            
            result = wf.generate_card(
                "Clinical-Precision",
                "front",
                quality="draft"
            )
            
            assert result.success is True
            filename = Path(result.filepath).name
            
            # Check naming components
            assert "Clinical-Precision" in filename
            assert "front" in filename
            assert filename.endswith(".png")
            # Should include timestamp
            assert len(filename.split("_")) >= 4


class TestErrorHandling:
    """Test error scenarios and recovery"""
    
    def test_openai_auth_error_handling(self, monkeypatch, tmp_path):
        """OpenAI auth errors should be handled gracefully"""
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test123456789012345678")
        
        with patch('hybrid.modern_workflow.OpenAI') as mock_openai_class:
            # Setup auth error mock
            mock_openai_class.return_value = create_mock_openai_auth_error()
            
            wf = ModernHybridWorkflow()
            wf.production_dir = tmp_path
            
            result = wf.generate_card(
                "Clinical-Precision",
                "front",
                model=ModelType.GPT_IMAGE_1,
                quality="production"
            )
            
            assert result.success is False
            assert "Authentication failed" in result.error_message
            assert result.model_used == "gpt-image-1"
    
    def test_gemini_rate_limit_handling(self, monkeypatch, tmp_path):
        """Gemini rate limit errors should be handled gracefully"""
        monkeypatch.setenv("GOOGLE_API_KEY", "AIza1234567890123456789")
        
        with patch('hybrid.modern_workflow.genai') as mock_gemini_module:
            # Setup rate limit error mock
            mock_gemini_module.Client.return_value = create_mock_gemini_rate_limit()
            
            wf = ModernHybridWorkflow()
            wf.drafts_dir = tmp_path
            
            result = wf.generate_card(
                "Athletic-Edge",
                "back",
                model=ModelType.GEMINI_FLASH,
                quality="draft"
            )
            
            assert result.success is False
            assert "Rate limit exceeded" in result.error_message
            assert result.model_used == "gemini-2.5-flash-image-preview"
    
    def test_empty_response_handling(self, monkeypatch, tmp_path):
        """Empty API responses should be handled gracefully"""
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test123456789012345678")
        
        with patch('hybrid.modern_workflow.OpenAI') as mock_openai_class:
            # Setup empty response mock
            mock_openai_class.return_value = create_mock_openai_empty_response()
            
            wf = ModernHybridWorkflow()
            wf.production_dir = tmp_path
            
            result = wf.generate_card(
                "Luxury-Wellness",
                "front",
                model=ModelType.GPT_IMAGE_1,
                quality="production"
            )
            
            assert result.success is False
            assert result.model_used == "gpt-image-1"
    
    def test_fallback_when_primary_model_fails(self, monkeypatch, tmp_path):
        """Should handle graceful failure when model selection fails"""
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test123456789012345678")
        monkeypatch.setenv("GOOGLE_API_KEY", "AIza1234567890123456789")
        
        with patch('hybrid.modern_workflow.OpenAI') as mock_openai_class, \
             patch('hybrid.modern_workflow.genai') as mock_gemini_module:
            
            # Setup mixed success/failure
            mock_openai_class.return_value = create_mock_openai_auth_error()
            mock_gemini_module.Client.return_value = create_mock_gemini_success()
            
            wf = ModernHybridWorkflow()
            wf.production_dir = tmp_path
            
            # Request production (would normally use GPT, but it fails)
            result = wf.generate_card(
                "Clinical-Precision",
                "front",
                model=ModelType.GPT_IMAGE_1,  # Explicitly request failing model
                quality="production"
            )
            
            # Should fail gracefully with clear error
            assert result.success is False
            assert result.model_used == "gpt-image-1"


class TestFullConceptGeneration:
    """Test complete concept set generation"""
    
    def test_generate_full_concept_set_success(self, monkeypatch, tmp_path):
        """Full concept set should generate both front and back"""
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test123456789012345678")
        monkeypatch.setenv("GOOGLE_API_KEY", "AIza1234567890123456789")
        
        with patch('hybrid.modern_workflow.OpenAI') as mock_openai_class, \
             patch('hybrid.modern_workflow.genai') as mock_gemini_module:
            
            # Setup successful mocks
            mock_openai_class.return_value = create_mock_openai_success()
            mock_gemini_module.Client.return_value = create_mock_gemini_success()
            
            wf = ModernHybridWorkflow()
            wf.production_dir = tmp_path
            wf.drafts_dir = tmp_path
            
            results = wf.generate_full_concept_set(
                "Clinical-Precision",
                "production"
            )
            
            # Should have both front and back
            assert 'front' in results
            assert 'back' in results
            
            # Both should be successful
            assert results['front'].success is True
            assert results['back'].success is True
            
            # Both should use GPT for production
            assert results['front'].model_used == "gpt-image-1"
            assert results['back'].model_used == "gpt-image-1"
            
            # Files should exist
            assert Path(results['front'].filepath).exists()
            assert Path(results['back'].filepath).exists()
    
    def test_partial_failure_handling(self, monkeypatch, tmp_path):
        """Should handle cases where one card fails but other succeeds"""
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test123456789012345678")
        
        with patch('hybrid.modern_workflow.OpenAI') as mock_openai_class:
            # Create a mock that fails on first call, succeeds on second
            mock_client = MagicMock()
            call_count = 0
            
            def side_effect(*args, **kwargs):
                nonlocal call_count
                call_count += 1
                if call_count == 1:
                    raise Exception("First call fails")
                else:
                    return create_mock_openai_success().images.generate(*args, **kwargs)
            
            mock_client.images.generate.side_effect = side_effect
            mock_openai_class.return_value = mock_client
            
            wf = ModernHybridWorkflow()
            wf.production_dir = tmp_path
            
            results = wf.generate_full_concept_set(
                "Athletic-Edge",
                "production"
            )
            
            # Should have results for both attempts
            assert 'front' in results
            assert 'back' in results
            
            # First should fail, second should succeed
            assert results['front'].success is False
            assert results['back'].success is True


class TestCostTracking:
    """Test cost estimation and tracking"""
    
    def test_cost_estimation_accuracy(self, monkeypatch, tmp_path):
        """Cost estimates should match expected values"""
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test123456789012345678")
        monkeypatch.setenv("GOOGLE_API_KEY", "AIza1234567890123456789")
        
        with patch('hybrid.modern_workflow.OpenAI') as mock_openai_class, \
             patch('hybrid.modern_workflow.genai') as mock_gemini_module:
            
            # Setup successful mocks
            mock_openai_class.return_value = create_mock_openai_success()
            mock_gemini_module.Client.return_value = create_mock_gemini_success()
            
            wf = ModernHybridWorkflow()
            wf.production_dir = tmp_path
            wf.drafts_dir = tmp_path
            
            # Test different quality levels
            draft_result = wf.generate_card("Clinical-Precision", "front", quality="draft")
            review_result = wf.generate_card("Clinical-Precision", "front", quality="review")
            production_result = wf.generate_card("Clinical-Precision", "front", quality="production")
            
            # Check cost progression
            assert draft_result.cost_estimate == 0.005  # Gemini
            assert review_result.cost_estimate == 0.07   # GPT medium
            assert production_result.cost_estimate == 0.19  # GPT high
            
            # Verify cost ordering
            assert draft_result.cost_estimate < review_result.cost_estimate
            assert review_result.cost_estimate < production_result.cost_estimate


# Test fixtures for common setups
@pytest.fixture
def mock_successful_workflow(monkeypatch, tmp_path):
    """Create a fully mocked workflow with successful API responses"""
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test123456789012345678")
    monkeypatch.setenv("GOOGLE_API_KEY", "AIza1234567890123456789")
    
    with patch('hybrid.modern_workflow.OpenAI') as mock_openai_class, \
         patch('hybrid.modern_workflow.genai') as mock_gemini_module:
        
        # Setup successful mocks
        mock_openai_class.return_value = create_mock_openai_success()
        mock_gemini_module.Client.return_value = create_mock_gemini_success()
        
        wf = ModernHybridWorkflow()
        wf.production_dir = tmp_path
        wf.drafts_dir = tmp_path
        
        return wf


if __name__ == "__main__":
    pytest.main([__file__, "-v"])