# Alex Shafiro PT - Business Card Generator v1.0

Generate premium business cards using Google's Gemini 2.5 Flash Image API that actually creates images.

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set API key
export GEMINI_API_KEY="your_key_here"
# Or create .env file: echo "GEMINI_API_KEY=your_key_here" > .env

# 3. Generate cards
python generate_business_cards.py
```

## 🎨 What You Get

**3 Premium Concept Variations:**
- **Clinical Precision**: Medical authority, symmetric layout
- **Athletic Edge**: Dynamic, performance-focused
- **Luxury Wellness**: Equinox-level sophistication

**Each Concept Includes:**
- ✅ Front card with logo, contact info, QR code
- ✅ Back card with "Revolutionary Rehabilitation" tagline
- ✅ Print-ready PNG files (300+ DPI)
- ✅ Deep matte black background (#0A0A0A)
- ✅ Emerald accent color (#00C9A7)
- ✅ Professional typography and layout

## 📋 Brand Info

- **Name**: Alex Shafiro PT / DPT / OCS / CSCS
- **Company**: A Stronger Life  
- **Tagline**: Revolutionary Rehabilitation
- **Website**: www.aslstrong.com
- **Email**: admin@aslstrong.com
- **Location**: Stamford, CT

## 🔑 Setup

### Get API Key
1. Go to [Google AI Studio](https://aistudio.google.com)
2. Generate an API key
3. Set environment variable:
   ```bash
   export GEMINI_API_KEY="your_key_here"
   ```

### Install Dependencies
```bash
pip install google-genai python-dotenv Pillow
```

## 🎯 Usage Options

1. **All Concepts** (Recommended) - Generates all 3 variations
2. **Clinical Precision** - Medical authority focus
3. **Athletic Edge** - Performance-focused design  
4. **Luxury Wellness** - Premium spa aesthetic

## 📁 Output

Files saved to `./output/`:
```
ASL_Alex_Shafiro_Clinical-Precision_front_20250918_132000.png
ASL_Alex_Shafiro_Clinical-Precision_back_20250918_132001.png
ASL_Alex_Shafiro_Athletic-Edge_front_20250918_132002.png
...
```

## 🖨️ Print Ready

- **Size**: 3.5" × 2.0" business card standard
- **Quality**: 300+ DPI for professional printing
- **Format**: PNG (convert to CMYK for offset printing)
- **Printer**: Upload directly to VistaPrint or local print shop

## 💰 Cost

~$0.02 per card generated (~$0.12 for all 6 cards)

## 🔧 Technical

**SDK**: Google GenAI SDK (`google-genai>=1.0.0`)  
**API**: Gemini 2.5 Flash Image for actual image generation  
**Output**: High-quality PNG files, not text descriptions

---

**This actually generates images.** Uses Google's Gemini 2.5 Flash Image API with the latest Google GenAI SDK for real image creation.
