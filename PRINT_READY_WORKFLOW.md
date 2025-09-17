# Print-Ready Business Card Workflow

## Overview
The updated business card generator now produces flat artboard designs at 1122×672 pixels with proper bleed areas. This document outlines the post-processing steps to create print-ready files.

## Generator Output
- **Format**: PNG files at 300 DPI
- **Dimensions**: 1122×672 px (3.75×2.25 inches with 0.125" bleed)
- **Color**: RGB (needs conversion to CMYK for print)
- **Content**: Flat artboard design with real QR codes

## Print-Ready Conversion Process

### Option 1: Professional Design Software (Recommended)

#### Using Adobe Illustrator/InDesign:
1. **Import the generated PNG**
   - Place the PNG file in a new document
   - Set document to 3.75×2.25" with 0.125" bleed

2. **Color Conversion**
   - File → Document Color Mode → CMYK
   - Check colors against CMYK gamut
   - Adjust black to 100% K (instead of rich black) for solid areas

3. **Export for Print**
   - File → Export → Adobe PDF (Print)
   - PDF/X-1a:2001 preset
   - Include bleed marks and printer marks
   - Output as PDF/X-1a CMYK

#### Using Figma (Alternative):
1. **Create new frame**: 1122×672px at 300 DPI
2. **Import PNG** as background
3. **Export settings**:
   - Format: PDF
   - Scale: 1x (maintains 300 DPI)
   - Note: Additional CMYK conversion needed in print shop

### Option 2: Python Post-Processing Script

```python
from PIL import Image, ImageCms
import os

def convert_to_print_ready(input_path, output_path):
    """Convert RGB PNG to print-ready CMYK with proper settings"""
    
    # Load image
    image = Image.open(input_path)
    
    # Convert RGB to CMYK
    rgb_profile = ImageCms.createProfile('sRGB')
    cmyk_profile = ImageCms.createProfile('CMYK')
    transform = ImageCms.buildTransform(rgb_profile, cmyk_profile, 'RGB', 'CMYK')
    cmyk_image = ImageCms.applyTransform(image, transform)
    
    # Save as TIFF with 300 DPI
    cmyk_image.save(output_path, 'TIFF', dpi=(300, 300), compression='lzw')
    print(f"✅ Print-ready file saved: {output_path}")

# Usage
convert_to_print_ready("ASL_Alex_Shafiro_PT_front_20250101_120000.png", "print_ready_front.tiff")
```

### Option 3: Online Print Services

Most online print services (Vistaprint, Moo, etc.) can handle:
- High-resolution PNG files (300+ DPI)
- Automatic RGB to CMYK conversion
- Standard business card dimensions

Upload the generated PNG files directly, ensuring:
- File size meets service requirements
- Dimensions are correct (3.5×2.0" finished size)
- Resolution is 300 DPI minimum

## Print Specifications Achieved

✅ **Dimensions**: Exact 1122×672px with 0.125" bleed  
✅ **Resolution**: 300 DPI enforced  
✅ **Layout**: Flat artboard (no mockup effects)  
✅ **QR Codes**: Real, scannable codes generated  
✅ **Logo**: Properly integrated from project assets  
✅ **Typography**: Clean, professional hierarchy  
✅ **Color**: High contrast for excellent print quality  

## Recommended Print Settings

- **Paper Stock**: 16pt matte black cardstock
- **Finish**: Matte or silk finish (not glossy)
- **Quantity**: Minimum 250 for cost efficiency
- **Cutting**: Precision cut to 3.5×2.0" with rounded corners optional
- **Quality Check**: Request a proof print before full run

## File Naming Convention

Generated files follow this pattern:
```
ASL_Alex_Shafiro_PT_front_YYYYMMDD_HHMMSS.png
ASL_Alex_Shafiro_PT_back_YYYYMMDD_HHMMSS.png
```

## Issues Fixed

1. ✅ **Flat artboard output** instead of photorealistic mockup
2. ✅ **Real QR codes** generated with proper contrast and quiet zones
3. ✅ **Robust logo handling** with fallback paths
4. ✅ **Strict quality validation** - rejects substandard images
5. ✅ **Proper API formatting** with role and inlineData schema
6. ✅ **Print dimensions** with bleed specifications
7. ✅ **Resolution enforcement** at 300 DPI minimum

## Next Steps

1. Run the generator to create your cards
2. Choose your preferred post-processing method
3. Convert to CMYK if using professional printing
4. Submit to printer with specifications above

For questions about the workflow, check the generator code or consult your print service provider.