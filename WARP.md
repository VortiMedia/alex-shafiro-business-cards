# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

**Alex Shafiro PT Business Card Generator v1.0** - A Python command-line application that generates premium business cards using Google's Gemini 2.5 Flash Image API. Produces print-ready PNG files with actual AI image generation.

## Key Architecture

### Core Components
- **`generate_business_cards.py`** - Main generator (429 lines, fully functional)
- **Google GenAI SDK** - Uses `google-genai>=1.0.0` with `gemini-2.5-flash-image-preview` model
- **Business card concepts** - Three variations: Clinical Precision, Athletic Edge, Luxury Wellness
- **Brand system** - Deep matte black (#0A0A0A) with emerald accent (#00C9A7)
- **Interactive CLI** - Menu-driven interface for generating single or multiple concepts

### Design Philosophy
"Equinox meets Mayo Clinic" - Premium luxury aesthetic with medical credibility. Sophisticated minimalism over embellishment.

## Essential Commands

### Setup & Installation
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set API key (required)
export GEMINI_API_KEY="your_key_here"
# OR create .env file
echo "GEMINI_API_KEY=your_key_here" > .env

# 3. Generate cards
python generate_business_cards.py
```

### Interactive Menu Options
1. **Generate all three concepts** (Recommended) - Creates all variations
2. **Clinical Precision only** - Medical authority focus
3. **Athletic Edge only** - Performance-focused design  
4. **Luxury Wellness only** - Premium spa aesthetic

### Validation
```bash
# Check output
ls -la ./output/

# Test API connection
python -c "from google import genai; print('✅ Ready')" 
```

## Technical Details

### API Implementation
- **Uses Google GenAI SDK** - `google-genai>=1.0.0` with Gemini 2.5 Flash Image
- **Generates actual PNG images** - Not text descriptions
- **Cost**: ~$0.005 per image (~$0.03 for complete 6-card set)
- **Quality**: 1024x1024 pixels, suitable for professional printing

### Print Specifications
- **Size**: 3.5" × 2.0" business card standard
- **Quality**: 300+ DPI for professional printing
- **Format**: PNG (convert to CMYK for offset printing)
- **Output**: Flat artboard design (NO 3D mockups)

### Brand Requirements
- **Background**: Deep matte black (#0A0A0A)
- **Accent**: Single emerald color (#00C9A7)
- **Typography**: Clean sans-serif fonts
- **Design**: Flat artboard presentation only

## File Organization

### Input Files
- `generate_business_cards.py` - Main generator
- `requirements.txt` - Python dependencies
- `.env` - API credentials (create from `.env.example`)

### Output Structure  
```
./output/
├── ASL_Alex_Shafiro_Clinical-Precision_front_YYYYMMDD_HHMMSS.png
├── ASL_Alex_Shafiro_Clinical-Precision_back_YYYYMMDD_HHMMSS.png
├── ASL_Alex_Shafiro_Athletic-Edge_front_YYYYMMDD_HHMMSS.png
└── ...
```

## Common Issues & Solutions

### API Problems
- **Missing API key**: Check `GEMINI_API_KEY` environment variable
- **Import errors**: Run `pip install google-genai python-dotenv Pillow`
- **Generation failures**: Verify internet connection and API quota

### Quality Issues
- **Wrong aspect ratio**: Adjust prompt to emphasize "business card proportions" 
- **Text illegibility**: Add "high contrast, legible at small sizes" to prompts
- **Wrong colors**: Emphasize "deep matte black background, single emerald accent"

## Dependencies

### Core Requirements
- `google-genai>=1.0.0` - For Gemini 2.5 Flash Image API access
- `python-dotenv>=1.0.0` - Environment variable management  
- `Pillow>=10.0.0` - Image processing and validation
- `requests>=2.31.0` - HTTP client for API calls

### Python Version
- **Minimum**: Python 3.10+ (required for nano-banana)
- **Recommended**: Python 3.12+ (current project uses 3.12.2)

## Business Logic

### Brand Information (in code)
```python
BRAND_INFO = {
    "name": "Alex Shafiro PT / DPT / OCS / CSCS",
    "company": "A Stronger Life", 
    "tagline": "Revolutionary Rehabilitation",
    "email": "admin@aslstrong.com",
    "website": "www.aslstrong.com",
    "location": "Stamford, CT"
}
```

### Design Concepts
- **Clinical Precision**: Medical authority, symmetric layout
- **Athletic Edge**: Dynamic, performance-focused
- **Luxury Wellness**: Equinox-level sophistication

### Print Specifications
- **Standard**: 3.5" × 2.0" business cards
- **Bleed**: 0.125" all sides for professional printing
- **Safe zone**: 0.25" margins for critical elements
- **Printer compatibility**: Direct upload to VistaPrint or local print shops

## Security Notes

### API Key Management
- Never commit `.env` files to git
- Use environment variables in production
- `.env.example` shows required format
- API keys should have appropriate permissions/quotas

### Cost Control
- Monitor API usage - each image generation costs ~$0.02
- Consider implementing daily limits for production use
- Cache successful generations to avoid re-generation costs
