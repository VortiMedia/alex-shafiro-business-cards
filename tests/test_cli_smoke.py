#!/usr/bin/env python3
"""
CLI smoke tests for business card generator v2.0

Tests the command-line interface without making actual API calls.
Validates menu display, input handling, and basic workflow paths.
"""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
import sys
from io import StringIO

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from generate_business_cards_v2 import BusinessCardGeneratorV2
from fixtures.mock_openai import create_mock_openai_success
from fixtures.mock_gemini import create_mock_gemini_success


class TestCLIBanner:
    """Test CLI banner and initial display"""
    
    def test_banner_displays_version_info(self, capsys):
        """Banner should display correct version and model info"""
        generator = BusinessCardGeneratorV2()
        generator.print_banner()
        
        captured = capsys.readouterr()
        
        # Check for key banner elements
        assert "Business Card Generator v2.0" in captured.out
        assert "Dual Model Support" in captured.out
        assert "OpenAI GPT Image 1" in captured.out
        assert "Google Gemini" in captured.out
    
    def test_brand_info_display(self, capsys):
        """Brand information should display correctly"""
        generator = BusinessCardGeneratorV2()
        generator.show_brand_info()
        
        captured = capsys.readouterr()
        
        # Check for brand elements
        assert "Alex Shafiro" in captured.out
        assert "A Stronger Life" in captured.out
        assert "Revolutionary Rehabilitation" in captured.out
        assert "aslstrong.com" in captured.out
    
    def test_cost_information_display(self, capsys):
        """Cost information should display correctly"""
        generator = BusinessCardGeneratorV2()
        generator.show_cost_information()
        
        captured = capsys.readouterr()
        
        # Check for cost information
        assert "Cost Information" in captured.out
        assert "$0.005" in captured.out  # Gemini cost
        assert "$0.190" in captured.out  # GPT production cost
        assert "Draft" in captured.out
        assert "Production" in captured.out
    
    def test_generation_options_display(self, capsys):
        """Generation options menu should display correctly"""
        generator = BusinessCardGeneratorV2()
        generator.show_generation_options()
        
        captured = capsys.readouterr()
        
        # Check for menu options
        assert "Generation Options" in captured.out
        assert "1. Draft Quality" in captured.out
        assert "3. Production" in captured.out
        assert "Clinical Precision" in captured.out
        assert "Athletic Edge" in captured.out
        assert "Luxury Wellness" in captured.out


class TestCostEstimation:
    """Test cost estimation without API calls"""
    
    def test_estimate_concept_cost(self):
        """Cost estimation should return reasonable values"""
        generator = BusinessCardGeneratorV2()
        
        # Test different quality levels
        draft_cost = generator.estimate_concept_cost("draft")
        review_cost = generator.estimate_concept_cost("review") 
        production_cost = generator.estimate_concept_cost("production")
        
        # Should have reasonable values
        assert 0 < draft_cost < 0.1
        assert 0 < review_cost < 0.2
        assert 0 < production_cost < 0.5
        
        # Should be ordered correctly
        assert draft_cost < review_cost < production_cost
    
    def test_estimate_total_cost(self):
        """Total cost estimation should multiply correctly"""
        generator = BusinessCardGeneratorV2()
        concepts = ["Clinical-Precision", "Athletic-Edge", "Luxury-Wellness"]
        
        total_cost = generator.estimate_total_cost(concepts, "draft")
        single_cost = generator.estimate_concept_cost("draft")
        
        # Should be approximately 6x single cost (3 concepts x 2 cards each)
        expected_cost = single_cost * 6
        assert abs(total_cost - expected_cost) < 0.001


class TestWorkflowIntegration:
    """Test integration with ModernHybridWorkflow"""
    
    @patch('hybrid.modern_workflow.OpenAI')
    @patch('hybrid.modern_workflow.genai')
    def test_workflow_initialization(self, mock_gemini, mock_openai, monkeypatch):
        """Workflow should initialize properly with API keys"""
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test123456789012345678")
        monkeypatch.setenv("GOOGLE_API_KEY", "AIza1234567890123456789")
        
        # Setup successful mocks
        mock_openai.return_value = create_mock_openai_success()
        mock_gemini.Client.return_value = create_mock_gemini_success()
        
        generator = BusinessCardGeneratorV2()
        
        # Should have a workflow instance
        assert hasattr(generator, 'workflow')
        assert generator.workflow is not None
    
    @patch('hybrid.modern_workflow.OpenAI')
    @patch('hybrid.modern_workflow.genai')
    def test_session_cost_tracking(self, mock_gemini, mock_openai, monkeypatch):
        """Session costs should be tracked correctly"""
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test123456789012345678")
        monkeypatch.setenv("GOOGLE_API_KEY", "AIza1234567890123456789")
        
        # Setup successful mocks
        mock_openai.return_value = create_mock_openai_success()
        mock_gemini.Client.return_value = create_mock_gemini_success()
        
        generator = BusinessCardGeneratorV2()
        
        # Should start with empty session costs
        assert generator.session_costs == []
        
        # After handling generation (mocked), costs might be added
        # This would be tested in integration with actual generation


class TestInputHandling:
    """Test user input handling"""
    
    def test_cost_estimation_methods(self):
        """Cost estimation methods should be available"""
        generator = BusinessCardGeneratorV2()
        
        # Should have cost estimation methods
        assert hasattr(generator, 'estimate_concept_cost')
        assert hasattr(generator, 'estimate_total_cost')
        assert callable(generator.estimate_concept_cost)
        assert callable(generator.estimate_total_cost)
    
    def test_generation_handler_methods(self):
        """Generation handler methods should be available"""
        generator = BusinessCardGeneratorV2()
        
        # Should have generation handlers
        assert hasattr(generator, 'handle_quality_generation')
        assert hasattr(generator, 'handle_single_concept')
        assert hasattr(generator, 'handle_custom_generation')
        
        assert callable(generator.handle_quality_generation)
        assert callable(generator.handle_single_concept)  
        assert callable(generator.handle_custom_generation)


class TestResultsDisplay:
    """Test results display functionality"""
    
    def test_print_generation_results_method_exists(self):
        """Results display method should exist"""
        generator = BusinessCardGeneratorV2()
        
        assert hasattr(generator, 'print_generation_results')
        assert callable(generator.print_generation_results)
    
    def test_empty_results_handling(self, capsys):
        """Should handle empty results gracefully"""
        generator = BusinessCardGeneratorV2()
        
        # Test with empty results
        generator.print_generation_results({})
        
        captured = capsys.readouterr()
        
        # Should indicate no results
        assert "No cards" in captured.out or "failed" in captured.out.lower()


class TestErrorScenarios:
    """Test error handling in CLI"""
    
    @patch('hybrid.modern_workflow.OpenAI')
    @patch('hybrid.modern_workflow.genai')
    def test_api_unavailable_handling(self, mock_gemini, mock_openai, monkeypatch):
        """Should handle API unavailable scenarios"""
        # No API keys set
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        
        # Should handle missing APIs gracefully during initialization
        try:
            generator = BusinessCardGeneratorV2()
            # If it gets here, it should handle the error gracefully
            assert hasattr(generator, 'workflow')
        except ValueError:
            # Expected if no APIs are available
            pass
    
    def test_invalid_quality_handling(self):
        """Should handle invalid quality parameters"""
        generator = BusinessCardGeneratorV2()
        
        # Should handle invalid quality levels gracefully
        cost = generator.estimate_concept_cost("invalid_quality")
        
        # Should return a default value rather than crashing
        assert isinstance(cost, (int, float))
        assert cost >= 0


class TestMenuSystem:
    """Test CLI menu system"""
    
    def test_menu_display_formatting(self, capsys):
        """Menu should be properly formatted"""
        generator = BusinessCardGeneratorV2()
        generator.show_generation_options()
        
        captured = capsys.readouterr()
        lines = captured.out.split('\n')
        
        # Should have structured menu
        option_lines = [line for line in lines if line.strip().startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '0.'))]
        
        # Should have multiple menu options
        assert len(option_lines) >= 8  # Expected menu items
    
    def test_banner_formatting(self, capsys):
        """Banner should be properly formatted"""
        generator = BusinessCardGeneratorV2()
        generator.print_banner()
        
        captured = capsys.readouterr()
        lines = captured.out.split('\n')
        
        # Should have title and separator
        title_line = next((line for line in lines if "Business Card Generator v2.0" in line), None)
        separator_line = next((line for line in lines if "=" in line), None)
        
        assert title_line is not None
        assert separator_line is not None


class TestModuleStructure:
    """Test that the CLI module has expected structure"""
    
    def test_required_imports(self):
        """Should import required modules without errors"""
        # These imports should work if dependencies are properly set up
        import sys
        from pathlib import Path
        
        # Should be able to import the main class
        from generate_business_cards_v2 import BusinessCardGeneratorV2
        
        assert BusinessCardGeneratorV2 is not None
    
    def test_class_structure(self):
        """BusinessCardGeneratorV2 should have expected methods"""
        from generate_business_cards_v2 import BusinessCardGeneratorV2
        
        generator = BusinessCardGeneratorV2()
        
        # Core methods
        expected_methods = [
            'print_banner',
            'show_brand_info', 
            'show_cost_information',
            'show_generation_options',
            'handle_quality_generation',
            'handle_single_concept',
            'handle_custom_generation',
            'print_generation_results'
        ]
        
        for method in expected_methods:
            assert hasattr(generator, method), f"Missing method: {method}"
            assert callable(getattr(generator, method)), f"Method not callable: {method}"


# Integration test with mocked workflow
@pytest.fixture 
def mock_cli_environment(monkeypatch):
    """Set up mocked environment for CLI testing"""
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test123456789012345678")
    monkeypatch.setenv("GOOGLE_API_KEY", "AIza1234567890123456789")
    
    with patch('hybrid.modern_workflow.OpenAI') as mock_openai, \
         patch('hybrid.modern_workflow.genai') as mock_gemini:
        
        mock_openai.return_value = create_mock_openai_success()
        mock_gemini.Client.return_value = create_mock_gemini_success()
        
        yield


if __name__ == "__main__":
    pytest.main([__file__, "-v"])