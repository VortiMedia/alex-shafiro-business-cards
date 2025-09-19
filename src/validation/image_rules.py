#!/usr/bin/env python3
"""
Image Validation Rules for Business Card Generator

Provides reusable validation functions to ensure generated images
meet quality standards for print-ready business cards.
"""

import io
from pathlib import Path
from typing import Tuple, Union
from PIL import Image

def validate_min_resolution(
    image_data: Union[bytes, str, Path], 
    min_width: int = 512, 
    min_height: int = 512
) -> bool:
    """
    Validate that image meets minimum resolution requirements
    
    Args:
        image_data: Image data as bytes, file path, or Path object
        min_width: Minimum width in pixels (default: 512)
        min_height: Minimum height in pixels (default: 512)
        
    Returns:
        bool: True if image meets minimum resolution
        
    Raises:
        ValueError: If image data is invalid or corrupted
    """
    try:
        img = _load_image(image_data)
        return img.width >= min_width and img.height >= min_height
    except Exception as e:
        raise ValueError(f"Invalid image data: {e}")

def validate_color_mode(
    image_data: Union[bytes, str, Path], 
    allowed_modes: Tuple[str, ...] = ("RGB", "RGBA")
) -> bool:
    """
    Validate that image uses acceptable color mode
    
    Args:
        image_data: Image data as bytes, file path, or Path object
        allowed_modes: Tuple of allowed PIL color modes (default: RGB, RGBA)
        
    Returns:
        bool: True if image uses allowed color mode
        
    Raises:
        ValueError: If image data is invalid or corrupted
    """
    try:
        img = _load_image(image_data)
        return img.mode in allowed_modes
    except Exception as e:
        raise ValueError(f"Invalid image data: {e}")

def validate_aspect_ratio(
    image_data: Union[bytes, str, Path], 
    target_ratio: float = 1.75,  # 3.5" / 2.0" business card ratio
    tolerance: float = 0.1
) -> bool:
    """
    Validate that image has acceptable aspect ratio for business cards
    
    Args:
        image_data: Image data as bytes, file path, or Path object
        target_ratio: Target aspect ratio (default: 1.75 for business cards)
        tolerance: Acceptable deviation from target ratio (default: 0.1)
        
    Returns:
        bool: True if aspect ratio is within tolerance
        
    Raises:
        ValueError: If image data is invalid or corrupted
    """
    try:
        img = _load_image(image_data)
        actual_ratio = img.width / img.height
        return abs(actual_ratio - target_ratio) <= tolerance
    except Exception as e:
        raise ValueError(f"Invalid image data: {e}")

def validate_file_size(
    image_data: Union[bytes, str, Path],
    min_bytes: int = 1024,  # 1KB minimum
    max_bytes: int = 10 * 1024 * 1024  # 10MB maximum
) -> bool:
    """
    Validate that image file size is within reasonable bounds
    
    Args:
        image_data: Image data as bytes, file path, or Path object
        min_bytes: Minimum file size in bytes (default: 1024)
        max_bytes: Maximum file size in bytes (default: 10MB)
        
    Returns:
        bool: True if file size is within bounds
    """
    try:
        if isinstance(image_data, bytes):
            size = len(image_data)
        elif isinstance(image_data, (str, Path)):
            size = Path(image_data).stat().st_size
        else:
            raise ValueError("Invalid image_data type")
            
        return min_bytes <= size <= max_bytes
    except Exception:
        return False

def validate_print_dpi(
    image_data: Union[bytes, str, Path],
    min_dpi: float = 150.0  # Minimum for reasonable print quality
) -> bool:
    """
    Validate that image has sufficient DPI for print quality
    
    Note: This is a heuristic check based on image dimensions
    assuming standard business card size (3.5" x 2.0")
    
    Args:
        image_data: Image data as bytes, file path, or Path object
        min_dpi: Minimum DPI for print quality (default: 150)
        
    Returns:
        bool: True if estimated DPI meets minimum requirement
        
    Raises:
        ValueError: If image data is invalid or corrupted
    """
    try:
        img = _load_image(image_data)
        
        # Business card dimensions in inches
        card_width_inches = 3.5
        card_height_inches = 2.0
        
        # Calculate estimated DPI
        width_dpi = img.width / card_width_inches
        height_dpi = img.height / card_height_inches
        
        # Use the lower DPI value (more conservative)
        estimated_dpi = min(width_dpi, height_dpi)
        
        return estimated_dpi >= min_dpi
    except Exception as e:
        raise ValueError(f"Invalid image data: {e}")

def validate_business_card_image(image_data: Union[bytes, str, Path]) -> dict:
    """
    Comprehensive validation for business card images
    
    Runs all validation rules and returns detailed results
    
    Args:
        image_data: Image data as bytes, file path, or Path object
        
    Returns:
        dict: Validation results with bool values for each check
        {
            'min_resolution': bool,
            'color_mode': bool,
            'aspect_ratio': bool,
            'file_size': bool,
            'print_dpi': bool,
            'overall_valid': bool
        }
    """
    results = {}
    
    try:
        results['min_resolution'] = validate_min_resolution(image_data)
    except Exception:
        results['min_resolution'] = False
    
    try:
        results['color_mode'] = validate_color_mode(image_data)
    except Exception:
        results['color_mode'] = False
    
    try:
        results['aspect_ratio'] = validate_aspect_ratio(image_data)
    except Exception:
        results['aspect_ratio'] = False
    
    try:
        results['file_size'] = validate_file_size(image_data)
    except Exception:
        results['file_size'] = False
    
    try:
        results['print_dpi'] = validate_print_dpi(image_data)
    except Exception:
        results['print_dpi'] = False
    
    # Overall validity - all checks must pass
    results['overall_valid'] = all([
        results['min_resolution'],
        results['color_mode'],
        results['aspect_ratio'],
        results['file_size'],
        results['print_dpi']
    ])
    
    return results

def _load_image(image_data: Union[bytes, str, Path]) -> Image.Image:
    """
    Internal helper to load image from various data sources
    
    Args:
        image_data: Image data as bytes, file path, or Path object
        
    Returns:
        PIL.Image.Image: Loaded image object
        
    Raises:
        ValueError: If image cannot be loaded
    """
    try:
        if isinstance(image_data, bytes):
            return Image.open(io.BytesIO(image_data))
        elif isinstance(image_data, (str, Path)):
            return Image.open(image_data)
        else:
            raise ValueError(f"Unsupported image_data type: {type(image_data)}")
    except Exception as e:
        raise ValueError(f"Cannot load image: {e}")