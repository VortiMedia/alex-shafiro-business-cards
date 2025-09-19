#!/usr/bin/env python3
"""
API Status Monitoring for Business Card Generator

Provides health checks and status utilities for OpenAI and Google Gemini APIs
without making expensive generation calls during testing.
"""

import os
from typing import Dict, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class APIStatus(Enum):
    """API availability status"""
    AVAILABLE = "available"
    MISSING_KEY = "missing_key"
    INVALID_KEY = "invalid_key"
    UNAVAILABLE = "unavailable"
    UNKNOWN = "unknown"

@dataclass
class APIHealthCheck:
    """Container for API health check results"""
    name: str
    status: APIStatus
    has_key: bool
    key_format_valid: bool
    message: str

def check_openai_status() -> APIHealthCheck:
    """
    Check OpenAI API availability and key status
    
    Returns:
        APIHealthCheck: Status information for OpenAI API
    """
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        return APIHealthCheck(
            name="OpenAI GPT Image 1",
            status=APIStatus.MISSING_KEY,
            has_key=False,
            key_format_valid=False,
            message="OPENAI_API_KEY not found in environment"
        )
    
    # Basic format validation (OpenAI keys typically start with 'sk-')
    if not api_key.startswith('sk-') or len(api_key) < 20:
        return APIHealthCheck(
            name="OpenAI GPT Image 1",
            status=APIStatus.INVALID_KEY,
            has_key=True,
            key_format_valid=False,
            message="API key format appears invalid (should start with 'sk-')"
        )
    
    return APIHealthCheck(
        name="OpenAI GPT Image 1",
        status=APIStatus.AVAILABLE,
        has_key=True,
        key_format_valid=True,
        message="API key found and format looks valid"
    )

def check_gemini_status() -> APIHealthCheck:
    """
    Check Google Gemini API availability and key status
    
    Returns:
        APIHealthCheck: Status information for Gemini API
    """
    # Check both possible environment variable names
    api_key = os.getenv('GOOGLE_API_KEY') or os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        return APIHealthCheck(
            name="Google Gemini 2.5 Flash",
            status=APIStatus.MISSING_KEY,
            has_key=False,
            key_format_valid=False,
            message="GOOGLE_API_KEY or GEMINI_API_KEY not found in environment"
        )
    
    # Basic format validation (Google API keys typically start with 'AIza')
    if not api_key.startswith('AIza') or len(api_key) < 20:
        return APIHealthCheck(
            name="Google Gemini 2.5 Flash",
            status=APIStatus.INVALID_KEY,
            has_key=True,
            key_format_valid=False,
            message="API key format appears invalid (should start with 'AIza')"
        )
    
    return APIHealthCheck(
        name="Google Gemini 2.5 Flash",
        status=APIStatus.AVAILABLE,
        has_key=True,
        key_format_valid=True,
        message="API key found and format looks valid"
    )

def get_api_status_summary() -> Dict[str, APIHealthCheck]:
    """
    Get comprehensive status summary for all APIs
    
    Returns:
        Dict[str, APIHealthCheck]: Status for each API service
    """
    return {
        "openai": check_openai_status(),
        "gemini": check_gemini_status()
    }

def format_status_report(detailed: bool = True) -> str:
    """
    Format API status as human-readable report
    
    Args:
        detailed: Include detailed messages (default: True)
        
    Returns:
        str: Formatted status report
    """
    status_summary = get_api_status_summary()
    
    report_lines = ["🔍 API Status Check"]
    report_lines.append("=" * 50)
    
    for api_name, health_check in status_summary.items():
        # Status indicator
        if health_check.status == APIStatus.AVAILABLE:
            indicator = "✅"
        elif health_check.status == APIStatus.MISSING_KEY:
            indicator = "❌"
        elif health_check.status == APIStatus.INVALID_KEY:
            indicator = "⚠️ "
        else:
            indicator = "❓"
        
        # Basic status line
        report_lines.append(f"{indicator} {health_check.name}: {health_check.status.value}")
        
        # Add detailed message if requested
        if detailed:
            report_lines.append(f"   {health_check.message}")
        
        report_lines.append("")  # Blank line between services
    
    # Summary
    available_count = sum(1 for hc in status_summary.values() if hc.status == APIStatus.AVAILABLE)
    total_count = len(status_summary)
    
    if available_count == 0:
        summary_msg = "❌ No APIs available - please configure API keys"
    elif available_count == total_count:
        summary_msg = "✅ All APIs ready for use"
    else:
        summary_msg = f"⚠️  {available_count}/{total_count} APIs available"
    
    report_lines.append(summary_msg)
    
    return "\n".join(report_lines)

def get_available_models() -> Tuple[bool, bool]:
    """
    Get boolean flags for which models are available
    
    Returns:
        Tuple[bool, bool]: (openai_available, gemini_available)
    """
    status_summary = get_api_status_summary()
    
    openai_available = status_summary["openai"].status == APIStatus.AVAILABLE
    gemini_available = status_summary["gemini"].status == APIStatus.AVAILABLE
    
    return openai_available, gemini_available

def recommend_workflow() -> str:
    """
    Recommend workflow based on available APIs
    
    Returns:
        str: Human-readable workflow recommendation
    """
    openai_available, gemini_available = get_available_models()
    
    if openai_available and gemini_available:
        return "💡 Recommended: Use dual model workflow for optimal cost/quality balance"
    elif openai_available:
        return "💡 Recommended: Use OpenAI GPT Image 1 for high-quality results"
    elif gemini_available:
        return "💡 Recommended: Use Gemini for cost-effective generation"
    else:
        return "❌ No workflow available - please configure API keys"

def validate_environment() -> bool:
    """
    Validate that the environment is properly configured
    
    Returns:
        bool: True if at least one API is available
    """
    openai_available, gemini_available = get_available_models()
    return openai_available or gemini_available