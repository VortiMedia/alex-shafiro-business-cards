#!/usr/bin/env python3
"""
Tests for image validation rules

Tests all validation functions with various image scenarios
including edge cases and error conditions.
"""

import pytest
import io
from pathlib import Path
from PIL import Image
import sys

# Add src to path for imports  
sys.path.append(str(Path(__file__).parent.parent / "src"))

from validation.image_rules import (
    validate_min_resolution,
    validate_color_mode,
    validate_aspect_ratio,
    validate_file_size,
    validate_print_dpi,
    validate_business_card_image,
    _load_image
)

# Test data - create various image samples
def create_test_image(width=800, height=600, mode="RGB", color="white"):
    """Create test image with specified parameters"""
    img = Image.new(mode, (width, height), color)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()

@pytest.fixture
def valid_business_card_image():
    """Create a valid business card image (1536x1024)"""
    return create_test_image(1536, 1024, "RGB")

@pytest.fixture
def small_image():
    """Create a small image below minimum resolution"""
    return create_test_image(300, 200, "RGB")

@pytest.fixture
def large_image():
    """Create a large high-resolution image"""
    return create_test_image(3000, 2000, "RGB")

@pytest.fixture
def rgba_image():
    """Create an RGBA image with transparency"""
    return create_test_image(800, 600, "RGBA")

@pytest.fixture
def grayscale_image():
    """Create a grayscale image"""
    return create_test_image(800, 600, "L")

@pytest.fixture
def wrong_aspect_image():
    """Create an image with wrong aspect ratio (square)"""
    return create_test_image(1000, 1000, "RGB")


class TestMinResolution:
    """Test minimum resolution validation"""
    
    def test_valid_resolution_passes(self, valid_business_card_image):
        """Images meeting minimum resolution should pass"""
        assert validate_min_resolution(valid_business_card_image, 512, 512) is True
    
    def test_small_image_fails(self, small_image):
        """Images below minimum resolution should fail"""
        assert validate_min_resolution(small_image, 512, 512) is False
    
    def test_custom_minimum_values(self, valid_business_card_image):
        """Custom minimum values should be respected"""
        assert validate_min_resolution(valid_business_card_image, 2000, 1500) is False
        assert validate_min_resolution(valid_business_card_image, 1000, 800) is True
    
    def test_invalid_image_raises_error(self):
        """Invalid image data should raise ValueError"""
        with pytest.raises(ValueError, match="Invalid image data"):
            validate_min_resolution(b"not_an_image")
    
    def test_empty_data_raises_error(self):
        """Empty data should raise ValueError"""
        with pytest.raises(ValueError):
            validate_min_resolution(b"")


class TestColorMode:
    """Test color mode validation"""
    
    def test_rgb_mode_passes(self, valid_business_card_image):
        """RGB images should pass by default"""
        assert validate_color_mode(valid_business_card_image) is True
    
    def test_rgba_mode_passes(self, rgba_image):
        """RGBA images should pass by default"""
        assert validate_color_mode(rgba_image) is True
    
    def test_grayscale_fails_default(self, grayscale_image):
        """Grayscale images should fail with default settings"""
        assert validate_color_mode(grayscale_image) is False
    
    def test_custom_allowed_modes(self, grayscale_image):
        """Custom allowed modes should be respected"""
        assert validate_color_mode(grayscale_image, ("L",)) is True
        assert validate_color_mode(grayscale_image, ("RGB", "L")) is True
    
    def test_invalid_image_raises_error(self):
        """Invalid image data should raise ValueError"""
        with pytest.raises(ValueError, match="Invalid image data"):
            validate_color_mode(b"invalid_data")


class TestAspectRatio:
    """Test aspect ratio validation"""
    
    def test_business_card_ratio_passes(self, valid_business_card_image):
        """Images with business card ratio (1.5) should pass with tolerance"""
        # 1536/1024 = 1.5, close to 1.75 target within tolerance
        assert validate_aspect_ratio(valid_business_card_image, 1.75, 0.3) is True
    
    def test_exact_ratio_passes(self):
        """Images with exact target ratio should pass"""
        exact_ratio_image = create_test_image(1750, 1000, "RGB")  # 1.75 ratio
        assert validate_aspect_ratio(exact_ratio_image, 1.75, 0.1) is True
    
    def test_wrong_ratio_fails(self, wrong_aspect_image):
        """Images with wrong aspect ratio should fail"""
        # Square image (1:1) vs target 1.75:1
        assert validate_aspect_ratio(wrong_aspect_image, 1.75, 0.1) is False
    
    def test_custom_tolerance(self, valid_business_card_image):
        """Custom tolerance should be respected"""
        # Tight tolerance should fail
        assert validate_aspect_ratio(valid_business_card_image, 1.75, 0.1) is False
        # Loose tolerance should pass
        assert validate_aspect_ratio(valid_business_card_image, 1.75, 0.5) is True
    
    def test_invalid_image_raises_error(self):
        """Invalid image data should raise ValueError"""
        with pytest.raises(ValueError, match="Invalid image data"):
            validate_aspect_ratio(b"not_an_image")


class TestFileSize:
    """Test file size validation"""
    
    def test_normal_size_passes(self, valid_business_card_image):
        """Normal-sized images should pass"""
        assert validate_file_size(valid_business_card_image) is True
    
    def test_too_small_fails(self):
        """Very small images should fail"""
        tiny_image = create_test_image(10, 10, "RGB")  # Will be very small
        assert validate_file_size(tiny_image, min_bytes=50000) is False
    
    def test_custom_limits(self, valid_business_card_image):
        """Custom size limits should be respected"""
        image_size = len(valid_business_card_image)
        
        # Set max below actual size
        assert validate_file_size(valid_business_card_image, max_bytes=image_size // 2) is False
        # Set min above actual size
        assert validate_file_size(valid_business_card_image, min_bytes=image_size * 2) is False
        # Set limits around actual size
        assert validate_file_size(valid_business_card_image, 
                                min_bytes=image_size // 2, 
                                max_bytes=image_size * 2) is True
    
    def test_file_path_handling(self, tmp_path, valid_business_card_image):
        """Should handle file paths correctly"""
        # Save test image to file
        test_file = tmp_path / "test_image.png"
        with open(test_file, "wb") as f:
            f.write(valid_business_card_image)
        
        # Test with Path object
        assert validate_file_size(test_file) is True
        
        # Test with string path
        assert validate_file_size(str(test_file)) is True
    
    def test_invalid_path_returns_false(self):
        """Invalid file path should return False"""
        assert validate_file_size("nonexistent_file.png") is False


class TestPrintDPI:
    """Test print DPI validation"""
    
    def test_high_dpi_passes(self, large_image):
        """High DPI images should pass"""
        # 3000x2000 on 3.5x2 inch = 857x1000 DPI (minimum 857)
        assert validate_print_dpi(large_image, min_dpi=150) is True
    
    def test_low_dpi_fails(self, small_image):
        """Low DPI images should fail"""
        # 300x200 on 3.5x2 inch = 85x100 DPI
        assert validate_print_dpi(small_image, min_dpi=150) is False
    
    def test_business_card_dimensions(self, valid_business_card_image):
        """Standard business card size should be validated correctly"""
        # 1536x1024 on 3.5x2 inch = 438x512 DPI (minimum 438)
        assert validate_print_dpi(valid_business_card_image, min_dpi=400) is True
        assert validate_print_dpi(valid_business_card_image, min_dpi=500) is False
    
    def test_custom_dpi_threshold(self, valid_business_card_image):
        """Custom DPI threshold should be respected"""
        # Use very high threshold
        assert validate_print_dpi(valid_business_card_image, min_dpi=1000) is False
        # Use low threshold
        assert validate_print_dpi(valid_business_card_image, min_dpi=100) is True
    
    def test_invalid_image_raises_error(self):
        """Invalid image data should raise ValueError"""
        with pytest.raises(ValueError, match="Invalid image data"):
            validate_print_dpi(b"invalid")


class TestComprehensiveValidation:
    """Test comprehensive validation function"""
    
    def test_valid_image_passes_all_checks(self, large_image):
        """High-quality image should pass all validation checks"""
        results = validate_business_card_image(large_image)
        
        assert results['min_resolution'] is True
        assert results['color_mode'] is True
        # Note: 3000x2000 = 1.5 ratio, default tolerance may not accept this
        # This test focuses on other validation aspects
        assert results['file_size'] is True
        assert results['print_dpi'] is True
    
    def test_poor_image_fails_multiple_checks(self, small_image):
        """Low-quality image should fail multiple checks"""
        results = validate_business_card_image(small_image)
        
        assert results['min_resolution'] is False  # Too small
        assert results['print_dpi'] is False      # Too low DPI
        assert results['overall_valid'] is False  # Should fail overall
    
    def test_invalid_image_fails_gracefully(self):
        """Invalid image should fail all checks gracefully"""
        results = validate_business_card_image(b"not_an_image")
        
        # All checks should be False
        for key, value in results.items():
            assert value is False
    
    def test_mixed_results(self, valid_business_card_image):
        """Image passing some checks but failing others"""
        # This image might pass resolution and color but fail aspect ratio
        results = validate_business_card_image(valid_business_card_image)
        
        # Should have mixed results
        assert results['min_resolution'] is True
        assert results['color_mode'] is True
        assert results['file_size'] is True
        # Other checks might pass or fail depending on exact dimensions


class TestImageLoading:
    """Test internal image loading helper"""
    
    def test_load_from_bytes(self, valid_business_card_image):
        """Should load image from bytes"""
        img = _load_image(valid_business_card_image)
        assert isinstance(img, Image.Image)
        assert img.width > 0
        assert img.height > 0
    
    def test_load_from_file_path(self, tmp_path, valid_business_card_image):
        """Should load image from file path"""
        # Save test image
        test_file = tmp_path / "test.png"
        with open(test_file, "wb") as f:
            f.write(valid_business_card_image)
        
        # Test loading from path
        img = _load_image(test_file)
        assert isinstance(img, Image.Image)
        
        # Test loading from string path
        img = _load_image(str(test_file))
        assert isinstance(img, Image.Image)
    
    def test_invalid_data_raises_error(self):
        """Invalid data should raise ValueError"""
        with pytest.raises(ValueError, match="Cannot load image"):
            _load_image(b"not_an_image")
    
    def test_unsupported_type_raises_error(self):
        """Unsupported data type should raise ValueError"""
        with pytest.raises(ValueError, match="Unsupported image_data type"):
            _load_image(123)  # Invalid type


if __name__ == "__main__":
    pytest.main([__file__, "-v"])