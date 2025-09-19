#!/usr/bin/env python3
"""
Unit tests for ModernHybridWorkflow

Tests core functionality without making network calls.
All API interactions are mocked for fast, reliable testing.
"""

import os
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch
import sys

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent / "src"))

from hybrid.modern_workflow import ModernHybridWorkflow, ModelType, GenerationResult
from fixtures.mock_openai import create_mock_openai_success, TINY_PNG, BUSINESS_CARD_PNG
from fixtures.mock_gemini import create_mock_gemini_success

class TestModelSelection:
    """Test model selection logic"""
    
    def test_auto_prefers_gpt_for_production(self, monkeypatch):
        """Production quality should prefer GPT Image 1 when available"""
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test123456789012345678")
        monkeypatch.setenv("GOOGLE_API_KEY", "AIza1234567890123456789")
        
        with patch('hybrid.modern_workflow.OpenAI'), patch('hybrid.modern_workflow.genai'):
            wf = ModernHybridWorkflow()
            chosen = wf._select_model(ModelType.AUTO, "production")
            assert chosen == ModelType.GPT_IMAGE_1
    
    def test_auto_prefers_gemini_for_draft(self, monkeypatch):
        """Draft quality should prefer Gemini when available"""
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test123456789012345678")
        monkeypatch.setenv("GOOGLE_API_KEY", "AIza1234567890123456789")
        
        with patch('hybrid.modern_workflow.OpenAI'), patch('hybrid.modern_workflow.genai'):
            wf = ModernHybridWorkflow()
            chosen = wf._select_model(ModelType.AUTO, "draft")
            assert chosen == ModelType.GEMINI_FLASH
    
    def test_fallback_to_available_model(self, monkeypatch):
        """Should fallback to available model when preferred is unavailable"""
        # Only OpenAI available
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test123456789012345678")
        monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        
        with patch('hybrid.modern_workflow.OpenAI') as mock_openai, \
             patch('hybrid.modern_workflow.genai') as mock_genai:
            # Setup mocks - OpenAI works, Gemini fails
            mock_openai.return_value = create_mock_openai_success()
            mock_genai.Client.side_effect = Exception("No API key")
            
            wf = ModernHybridWorkflow()
            chosen = wf._select_model(ModelType.AUTO, "draft")
            assert chosen == ModelType.GPT_IMAGE_1  # Falls back to GPT
    
    def test_specific_model_request_honored(self, monkeypatch):
        """Specific model requests should be honored when available"""
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test123456789012345678")
        monkeypatch.setenv("GOOGLE_API_KEY", "AIza1234567890123456789")
        
        with patch('hybrid.modern_workflow.OpenAI'), patch('hybrid.modern_workflow.genai'):
            wf = ModernHybridWorkflow()
            chosen = wf._select_model(ModelType.GEMINI_FLASH, "production")
            assert chosen == ModelType.GEMINI_FLASH
    
    def test_unavailable_specific_model_falls_back(self, monkeypatch):
        """Unavailable specific model should fallback to AUTO logic"""
        # Only OpenAI available
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test123456789012345678")
        monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        
        with patch('hybrid.modern_workflow.OpenAI') as mock_openai, \
             patch('hybrid.modern_workflow.genai') as mock_genai:
            # Setup mocks - OpenAI works, Gemini fails
            mock_openai.return_value = create_mock_openai_success()
            mock_genai.Client.side_effect = Exception("No API key")
            
            wf = ModernHybridWorkflow()
            chosen = wf._select_model(ModelType.GEMINI_FLASH, "production")
            assert chosen == ModelType.GPT_IMAGE_1  # Falls back


class TestImageValidation:
    """Test image validation logic"""
    
    def test_validate_image_accepts_valid_png(self):
        """Valid PNG data should pass validation"""
        with patch('hybrid.modern_workflow.OpenAI'), patch('hybrid.modern_workflow.genai'):
            wf = ModernHybridWorkflow()
            
            # Should not raise exception for validation-compliant PNG (1536x1024)
            try:
                wf._validate_image(BUSINESS_CARD_PNG)
                assert True
            except ValueError:
                pytest.fail("Valid PNG should pass validation")
    
    def test_validate_image_rejects_invalid_data(self):
        """Invalid image data should fail validation"""
        with patch('hybrid.modern_workflow.OpenAI'), patch('hybrid.modern_workflow.genai'):
            wf = ModernHybridWorkflow()
            
            with pytest.raises(ValueError):
                wf._validate_image(b"not_an_image")
    
    def test_validate_image_rejects_empty_data(self):
        """Empty data should fail validation"""
        with patch('hybrid.modern_workflow.OpenAI'), patch('hybrid.modern_workflow.genai'):
            wf = ModernHybridWorkflow()
            
            with pytest.raises(ValueError):
                wf._validate_image(b"")


class TestPromptBuilding:
    """Test prompt building logic"""
    
    def test_prompt_includes_brand_info(self):
        """Prompt should include all brand information"""
        with patch('hybrid.modern_workflow.OpenAI'), patch('hybrid.modern_workflow.genai'):
            wf = ModernHybridWorkflow()
            prompt = wf._build_universal_prompt("Clinical-Precision", "front")
            
            # Check for key brand elements
            assert "Alex Shafiro" in prompt
            assert "A Stronger Life" in prompt
            assert "Revolutionary Rehabilitation" in prompt
            assert "#0A0A0A" in prompt  # Deep black
            assert "#00C9A7" in prompt  # Emerald
    
    def test_prompt_differentiates_front_back(self):
        """Front and back prompts should be different"""
        with patch('hybrid.modern_workflow.OpenAI'), patch('hybrid.modern_workflow.genai'):
            wf = ModernHybridWorkflow()
            front_prompt = wf._build_universal_prompt("Clinical-Precision", "front")
            back_prompt = wf._build_universal_prompt("Clinical-Precision", "back")
            
            assert front_prompt != back_prompt
            assert "contact" in front_prompt.lower() or "info" in front_prompt.lower()
            assert "tagline" in back_prompt.lower() or "revolutionary" in back_prompt.lower()
    
    def test_prompt_maps_concepts(self):
        """Different concepts should generate different prompts"""
        with patch('hybrid.modern_workflow.OpenAI'), patch('hybrid.modern_workflow.genai'):
            wf = ModernHybridWorkflow()
            clinical = wf._build_universal_prompt("Clinical-Precision", "front")
            athletic = wf._build_universal_prompt("Athletic-Edge", "front")
            luxury = wf._build_universal_prompt("Luxury-Wellness", "front")
            
            # Should all be different
            assert clinical != athletic != luxury


class TestFileSaving:
    """Test file saving functionality"""
    
    def test_save_image_creates_file(self, tmp_path, monkeypatch):
        """_save_image should create file with correct naming"""
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test123456789012345678")
        
        with patch('hybrid.modern_workflow.OpenAI'), patch('hybrid.modern_workflow.genai'):
            wf = ModernHybridWorkflow()
            wf.production_dir = tmp_path
            
            path = wf._save_image(
                TINY_PNG, 
                "Clinical-Precision", 
                "front", 
                "gpt-image-1", 
                tmp_path
            )
            
            # Check file exists
            assert Path(path).exists()
            assert Path(path).stat().st_size > 0
            
            # Check naming convention
            filename = Path(path).name
            assert "Clinical-Precision" in filename
            assert "front" in filename
            assert filename.endswith(".png")
    
    def test_save_image_handles_directory_creation(self, tmp_path, monkeypatch):
        """_save_image should handle missing directories"""
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test123456789012345678")
        
        with patch('hybrid.modern_workflow.OpenAI'), patch('hybrid.modern_workflow.genai'):
            wf = ModernHybridWorkflow()
            
            # Use non-existent subdirectory
            save_dir = tmp_path / "new_subdir"
            wf.production_dir = save_dir
            
            path = wf._save_image(
                TINY_PNG,
                "Athletic-Edge", 
                "back",
                "gemini",
                save_dir
            )
            
            # Should create directory and file
            assert Path(path).exists()
            assert save_dir.exists()


class TestCostEstimation:
    """Test cost calculation accuracy"""
    
    def test_cost_map_values_are_defined(self):
        """All expected cost values should be defined"""
        with patch('hybrid.modern_workflow.OpenAI'), patch('hybrid.modern_workflow.genai'):
            wf = ModernHybridWorkflow()
            
            # Check all expected cost keys exist
            assert "gemini_flash" in wf.COSTS
            assert "gpt_image_1_low" in wf.COSTS
            assert "gpt_image_1_medium" in wf.COSTS
            assert "gpt_image_1_high" in wf.COSTS
            
            # Check values are reasonable
            assert wf.COSTS["gemini_flash"] == 0.005
            assert wf.COSTS["gpt_image_1_high"] == 0.19
            
            # Check ordering (gemini should be cheapest)
            assert wf.COSTS["gemini_flash"] < wf.COSTS["gpt_image_1_low"]
    
    def test_quality_to_cost_mapping(self):
        """Quality levels should map to correct costs"""
        with patch('hybrid.modern_workflow.OpenAI'), patch('hybrid.modern_workflow.genai'):
            wf = ModernHybridWorkflow()
            
            # Test quality settings mapping
            quality_settings = {
                "draft": {"cost": wf.COSTS["gpt_image_1_low"]},
                "review": {"cost": wf.COSTS["gpt_image_1_medium"]},
                "production": {"cost": wf.COSTS["gpt_image_1_high"]}
            }
            
            # Verify cost progression
            assert quality_settings["draft"]["cost"] < quality_settings["review"]["cost"]
            assert quality_settings["review"]["cost"] < quality_settings["production"]["cost"]


class TestErrorHandling:
    """Test error handling and edge cases"""
    
    def test_no_api_keys_raises_error(self, monkeypatch):
        """Missing all API keys should raise ValueError"""
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        
        with patch('hybrid.modern_workflow.OpenAI'), patch('hybrid.modern_workflow.genai'):
            with pytest.raises(ValueError, match="No API keys available"):
                ModernHybridWorkflow()
    
    def test_model_selection_with_no_available_models(self, monkeypatch):
        """Model selection should return None when no models available"""
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test123456789012345678")
        
        with patch('hybrid.modern_workflow.OpenAI'), patch('hybrid.modern_workflow.genai'):
            wf = ModernHybridWorkflow()
            # Manually set both as unavailable
            wf.openai_available = False
            wf.gemini_available = False
            
            chosen = wf._select_model(ModelType.AUTO, "production")
            assert chosen is None
    
    def test_graceful_handling_of_invalid_concept(self):
        """Invalid concept should not crash prompt building"""
        with patch('hybrid.modern_workflow.OpenAI'), patch('hybrid.modern_workflow.genai'):
            wf = ModernHybridWorkflow()
            
            # Should not raise exception, just use default behavior
            prompt = wf._build_universal_prompt("NonExistent-Concept", "front")
            assert isinstance(prompt, str)
            assert len(prompt) > 0


# Fixtures for common test setup
@pytest.fixture
def mock_workflow(monkeypatch):
    """Create a mocked workflow instance for testing"""
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test123456789012345678")
    monkeypatch.setenv("GOOGLE_API_KEY", "AIza1234567890123456789")
    
    with patch('hybrid.modern_workflow.OpenAI') as mock_openai, \
         patch('hybrid.modern_workflow.genai') as mock_gemini:
        
        # Setup mock clients
        mock_openai.return_value = create_mock_openai_success()
        mock_gemini.Client.return_value = create_mock_gemini_success()
        
        return ModernHybridWorkflow()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])