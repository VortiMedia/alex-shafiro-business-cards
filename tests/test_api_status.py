#!/usr/bin/env python3
"""
Tests for API status monitoring

Tests API health checks, key validation, and status reporting
without making actual API calls.
"""

import pytest
import os
from pathlib import Path
import sys

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent / "src"))

from monitoring.api_status import (
    check_openai_status,
    check_gemini_status,
    get_api_status_summary,
    format_status_report,
    get_available_models,
    recommend_workflow,
    validate_environment,
    APIStatus,
    APIHealthCheck
)


class TestOpenAIStatusCheck:
    """Test OpenAI API status checking"""
    
    def test_missing_key(self, monkeypatch):
        """Missing OpenAI API key should be detected"""
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        
        result = check_openai_status()
        
        assert result.name == "OpenAI GPT Image 1"
        assert result.status == APIStatus.MISSING_KEY
        assert result.has_key is False
        assert result.key_format_valid is False
        assert "not found" in result.message
    
    def test_valid_key_format(self, monkeypatch):
        """Valid OpenAI API key format should be accepted"""
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test123456789012345678")
        
        result = check_openai_status()
        
        assert result.status == APIStatus.AVAILABLE
        assert result.has_key is True
        assert result.key_format_valid is True
        assert "format looks valid" in result.message
    
    def test_invalid_key_format(self, monkeypatch):
        """Invalid OpenAI API key format should be rejected"""
        monkeypatch.setenv("OPENAI_API_KEY", "invalid_key_format")
        
        result = check_openai_status()
        
        assert result.status == APIStatus.INVALID_KEY
        assert result.has_key is True
        assert result.key_format_valid is False
        assert "format appears invalid" in result.message
    
    def test_short_key(self, monkeypatch):
        """Short API key should be rejected"""
        monkeypatch.setenv("OPENAI_API_KEY", "sk-123")  # Too short
        
        result = check_openai_status()
        
        assert result.status == APIStatus.INVALID_KEY
        assert result.key_format_valid is False


class TestGeminiStatusCheck:
    """Test Gemini API status checking"""
    
    def test_missing_key(self, monkeypatch):
        """Missing Gemini API key should be detected"""
        monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        
        result = check_gemini_status()
        
        assert result.name == "Google Gemini 2.5 Flash"
        assert result.status == APIStatus.MISSING_KEY
        assert result.has_key is False
        assert "not found" in result.message
    
    def test_valid_google_key(self, monkeypatch):
        """Valid Google API key should be accepted"""
        monkeypatch.setenv("GOOGLE_API_KEY", "AIza1234567890123456789012345678")
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        
        result = check_gemini_status()
        
        assert result.status == APIStatus.AVAILABLE
        assert result.has_key is True
        assert result.key_format_valid is True
    
    def test_valid_gemini_key(self, monkeypatch):
        """Valid Gemini API key should be accepted"""
        monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
        monkeypatch.setenv("GEMINI_API_KEY", "AIza1234567890123456789012345678")
        
        result = check_gemini_status()
        
        assert result.status == APIStatus.AVAILABLE
        assert result.has_key is True
        assert result.key_format_valid is True
    
    def test_google_key_priority(self, monkeypatch):
        """GOOGLE_API_KEY should take priority over GEMINI_API_KEY"""
        monkeypatch.setenv("GOOGLE_API_KEY", "AIza_google_key_12345678")
        monkeypatch.setenv("GEMINI_API_KEY", "AIza_gemini_key_12345678")
        
        # Both are valid format, should use GOOGLE_API_KEY
        result = check_gemini_status()
        assert result.status == APIStatus.AVAILABLE
    
    def test_invalid_key_format(self, monkeypatch):
        """Invalid Gemini API key format should be rejected"""
        monkeypatch.setenv("GOOGLE_API_KEY", "invalid_format_key")
        
        result = check_gemini_status()
        
        assert result.status == APIStatus.INVALID_KEY
        assert result.has_key is True
        assert result.key_format_valid is False


class TestStatusSummary:
    """Test comprehensive status summary"""
    
    def test_both_apis_available(self, monkeypatch):
        """Both APIs available should be reported correctly"""
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test123456789012345678")
        monkeypatch.setenv("GOOGLE_API_KEY", "AIza1234567890123456789")
        
        summary = get_api_status_summary()
        
        assert "openai" in summary
        assert "gemini" in summary
        assert summary["openai"].status == APIStatus.AVAILABLE
        assert summary["gemini"].status == APIStatus.AVAILABLE
    
    def test_only_openai_available(self, monkeypatch):
        """Only OpenAI available scenario"""
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test123456789012345678")
        monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        
        summary = get_api_status_summary()
        
        assert summary["openai"].status == APIStatus.AVAILABLE
        assert summary["gemini"].status == APIStatus.MISSING_KEY
    
    def test_no_apis_available(self, monkeypatch):
        """No APIs available scenario"""
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        
        summary = get_api_status_summary()
        
        assert summary["openai"].status == APIStatus.MISSING_KEY
        assert summary["gemini"].status == APIStatus.MISSING_KEY


class TestStatusReporting:
    """Test status report formatting"""
    
    def test_detailed_report_format(self, monkeypatch):
        """Detailed report should include all information"""
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test123456789012345678")
        monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
        
        report = format_status_report(detailed=True)
        
        # Should include header
        assert "API Status Check" in report
        assert "=" in report  # Header separator
        
        # Should include service names
        assert "OpenAI GPT Image 1" in report
        assert "Google Gemini 2.5 Flash" in report
        
        # Should include indicators
        assert "✅" in report or "❌" in report
        
        # Should include detailed messages
        assert "format looks valid" in report or "not found" in report
    
    def test_brief_report_format(self, monkeypatch):
        """Brief report should exclude detailed messages"""
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test123456789012345678")
        monkeypatch.setenv("GOOGLE_API_KEY", "AIza1234567890123456789")
        
        brief_report = format_status_report(detailed=False)
        detailed_report = format_status_report(detailed=True)
        
        # Brief should be shorter
        assert len(brief_report) < len(detailed_report)
        
        # Should still have key elements
        assert "API Status Check" in brief_report
        assert "OpenAI" in brief_report
    
    def test_summary_messages(self, monkeypatch):
        """Summary messages should reflect API availability"""
        # All available
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test123456789012345678")
        monkeypatch.setenv("GOOGLE_API_KEY", "AIza1234567890123456789")
        
        report = format_status_report()
        assert "All APIs ready" in report
        
        # None available
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
        
        report = format_status_report()
        assert "No APIs available" in report


class TestAvailabilityChecks:
    """Test availability checking functions"""
    
    def test_get_available_models_both(self, monkeypatch):
        """Both models available"""
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test123456789012345678")
        monkeypatch.setenv("GOOGLE_API_KEY", "AIza1234567890123456789")
        
        openai_available, gemini_available = get_available_models()
        
        assert openai_available is True
        assert gemini_available is True
    
    def test_get_available_models_openai_only(self, monkeypatch):
        """Only OpenAI available"""
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test123456789012345678")
        monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
        
        openai_available, gemini_available = get_available_models()
        
        assert openai_available is True
        assert gemini_available is False
    
    def test_get_available_models_none(self, monkeypatch):
        """No models available"""
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
        
        openai_available, gemini_available = get_available_models()
        
        assert openai_available is False
        assert gemini_available is False


class TestWorkflowRecommendations:
    """Test workflow recommendation logic"""
    
    def test_dual_model_recommendation(self, monkeypatch):
        """Both APIs available should recommend dual workflow"""
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test123456789012345678")
        monkeypatch.setenv("GOOGLE_API_KEY", "AIza1234567890123456789")
        
        recommendation = recommend_workflow()
        
        assert "dual model workflow" in recommendation.lower()
        assert "optimal cost/quality balance" in recommendation.lower()
    
    def test_openai_only_recommendation(self, monkeypatch):
        """Only OpenAI available should recommend GPT Image 1"""
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test123456789012345678")
        monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
        
        recommendation = recommend_workflow()
        
        assert "OpenAI GPT Image 1" in recommendation
        assert "high-quality" in recommendation.lower()
    
    def test_gemini_only_recommendation(self, monkeypatch):
        """Only Gemini available should recommend cost-effective generation"""
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        monkeypatch.setenv("GOOGLE_API_KEY", "AIza1234567890123456789")
        
        recommendation = recommend_workflow()
        
        assert "Gemini" in recommendation
        assert "cost-effective" in recommendation.lower()
    
    def test_no_apis_recommendation(self, monkeypatch):
        """No APIs should recommend configuration"""
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
        
        recommendation = recommend_workflow()
        
        assert "No workflow available" in recommendation
        assert "configure API keys" in recommendation.lower()


class TestEnvironmentValidation:
    """Test environment validation"""
    
    def test_validate_environment_valid(self, monkeypatch):
        """Valid environment should return True"""
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test123456789012345678")
        
        assert validate_environment() is True
    
    def test_validate_environment_invalid(self, monkeypatch):
        """Invalid environment should return False"""
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
        
        assert validate_environment() is False


class TestDataStructures:
    """Test data structure definitions"""
    
    def test_api_status_enum_values(self):
        """APIStatus enum should have expected values"""
        expected_values = ["available", "missing_key", "invalid_key", "unavailable", "unknown"]
        
        for value in expected_values:
            # Should be able to create enum with each value
            status = APIStatus(value)
            assert status.value == value
    
    def test_api_health_check_structure(self):
        """APIHealthCheck should have expected structure"""
        health_check = APIHealthCheck(
            name="Test API",
            status=APIStatus.AVAILABLE,
            has_key=True,
            key_format_valid=True,
            message="Test message"
        )
        
        assert health_check.name == "Test API"
        assert health_check.status == APIStatus.AVAILABLE
        assert health_check.has_key is True
        assert health_check.key_format_valid is True
        assert health_check.message == "Test message"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])