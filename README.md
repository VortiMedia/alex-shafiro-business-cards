# Alex Shafiro PT - Premium Business Card Generator

> Generate premium, minimalist business cards following exact Nano Banana specifications using Google Gemini 2.5 Flash Image API

## ✨ Key Features

- **🎯 Nano Banana Specifications**: Follows exact original prompt requirements
- **🖤 Premium Aesthetic**: Matte black with subtle glow/edge highlights
- **🏥 Medical Positioning**: Professional rehabilitation expert branding
- **📐 Print-Ready**: True 300 DPI output with proper dimensions (3.5" × 2.0")
- **🎨 Logo Integration**: Uses actual A Stronger Life logo when available
- **⚡ Single Command**: Generate both front and back cards instantly

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install requests python-dotenv Pillow

# 2. Set up API key
echo "GEMINI_API_KEY=your_api_key_here" > .env

# 3. Generate cards
python generate_alex_shafiro_cards.py
```

## 📋 Design Specifications

### 🎨 **Visual Style**
- **Aesthetic**: Minimalist, high-end, premium, trustworthy
- **Background**: Matte black with subtle glow or edge highlight
- **Typography**: Clean, sans-serif, elegant fonts (no decorative fonts)
- **Color Scheme**: High contrast white text on matte black
- **Industry**: Medical rehabilitation / Elite athletics

### 📐 **Layout Structure**

#### **Front Card:**
- **Top Section**: A Stronger Life logo + company name
- **Center Section**: "Alex Shafiro PT / DPT / OCS / CSCS" + "Rehabilitation Specialist"
- **Left Column**: Contact info with icons (phone, email, address, website)
- **Bottom-Right**: QR code linking to www.aslstrong.com

#### **Back Card:**
- **Background**: Matching matte black finish
- **Center Text**: "Revolutionary Rehabilitation" in large white typography
- **Elements**: Optional subtle logo watermark + centered QR code

### 🔧 **Technical Specs**
- **Dimensions**: 3.5" × 2.0" (standard business card)
- **Resolution**: 300 DPI minimum (print-ready)
- **Format**: PNG output files
- **Color Profile**: CMYK ready
- **Finish**: Matte black recommended

## 🔑 Setup & Configuration

### 1. **API Key Setup**

Get your Google Gemini API key:
1. Visit [Google AI Studio](https://aistudio.google.com)
2. Create/sign in to your account
3. Generate an API key
4. Set up environment variable:

```bash
# Option 1: Create .env file
echo "GEMINI_API_KEY=your_actual_api_key_here" > .env

# Option 2: Export environment variable
export GEMINI_API_KEY=your_actual_api_key_here
```

### 2. **Dependencies Installation**

```bash
# Install required packages
pip install -r requirements.txt

# Or install manually
pip install requests python-dotenv Pillow
```

### 3. **Logo File (Optional)**

For best results, place the A Stronger Life logo at:
- `./assets/brand_assets/Stronger Life logo vertical original color.png`
- `./assets/Stronger Life logo vertical original color.png`
- `./logo.png`

The generator will work without a logo but quality may be reduced.

## 🎯 Usage

### **Basic Usage**

```bash
python generate_alex_shafiro_cards.py
```

**Interactive Process:**
1. Displays brand information to be used
2. Asks for confirmation to proceed
3. Generates front card with logo, contact info, and QR code
4. Generates back card with "Revolutionary Rehabilitation" text
5. Saves files to `./output/` directory
6. Reports on quality and print readiness

### **Brand Information Used**

- **Name**: Alex Shafiro PT / DPT / OCS / CSCS
- **Title**: Rehabilitation Specialist
- **Company**: A Stronger Life
- **Email**: admin@aslstrong.com
- **Website**: www.aslstrong.com
- **Location**: Stamford, CT
- **Phone**: +1 (XXX) XXX-XXXX (placeholder as per original prompt)

### **Output Files**

Generated cards are saved as:
```
./output/ASL_Alex_Shafiro_PT_front_YYYYMMDD_HHMMSS.png
./output/ASL_Alex_Shafiro_PT_back_YYYYMMDD_HHMMSS.png
```

## 🖨️ Print Preparation

### **Print Specifications**
- **Size**: 3.5" × 2.0" (89mm × 51mm)
- **Resolution**: 300 DPI minimum
- **Color Profile**: Convert to CMYK for offset printing
- **Stock**: Premium cardstock recommended
- **Finish**: Matte black finish with optional spot UV on logo
- **Bleed**: Add 0.125" bleed if required by printer

### **Quality Validation**
The generator automatically:
- ✅ Validates minimum resolution (1050×600 pixels)
- ✅ Reports effective DPI
- ✅ Checks print quality standards
- ⚠️ Warns if resolution may be insufficient

## 💰 Cost

- **Generation Cost**: ~$0.04 per card (front or back)
- **Complete Set**: ~$0.08 for both cards
- **API Usage**: Uses Google Gemini 2.5 Flash Image API

## 🛠️ Technical Details

### **Architecture**
- **Single File**: Everything contained in `generate_alex_shafiro_cards.py`
- **Dependencies**: Minimal - only essential packages
- **Error Handling**: Comprehensive API error handling and retry logic
- **Quality Control**: Built-in print quality validation
- **Logo Handling**: Automatic logo detection and base64 encoding

### **API Integration**
- **Service**: Google Gemini 2.5 Flash Image API
- **Endpoint**: `generativelanguage.googleapis.com`
- **Input**: Text prompt + optional logo image
- **Output**: High-quality PNG business card images
- **Timeout**: 60 seconds per generation

## 📊 Quality Standards

### **Design Quality**
- ✅ Follows exact Nano Banana prompt specifications
- ✅ Professional medical/rehabilitation positioning
- ✅ Premium luxury aesthetic appropriate for high-end practice
- ✅ Clean, minimalist design with generous negative space
- ✅ High contrast for excellent readability

### **Technical Quality**
- ✅ 300 DPI minimum resolution
- ✅ Standard business card dimensions
- ✅ Print-ready PNG format
- ✅ Optimized file sizes
- ✅ CMYK color profile compatibility

## 🔄 Development History

### **V2.0 - Complete Redesign**
- Fixed poor output quality from original system
- Implemented Gemini API best practices
- Added descriptive scene prompting
- Professional photography terminology
- Accurate text rendering
- Both front AND back card generation
- Quality validation and error handling

### **Key Improvements**
- **Before**: Copied existing designs with poor quality
- **After**: Original, professional designs from scratch
- **Before**: Blurry, unreadable text
- **After**: Sharp, print-ready typography
- **Before**: Front cards only
- **After**: Complete card sets (front + back)

## 🚨 Troubleshooting

### **Common Issues**

**API Key Error:**
```bash
❌ GEMINI_API_KEY not found in environment
```
**Solution**: Set up your API key in `.env` file or environment variable

**Logo Not Found:**
```bash
⚠️ A Stronger Life logo not found
```
**Solution**: Place logo file in expected location or continue without (reduced quality)

**Low Resolution Warning:**
```bash
⚠️ Print quality may be low: ~200 DPI
```
**Solution**: Try running again - API sometimes returns variable resolutions

**API Timeout:**
```bash
❌ API timeout for front card (>60s)
```
**Solution**: Check internet connection and try again

## 📝 License

This project is for generating Alex Shafiro PT business cards following specific design requirements.

## 🤝 Support

For issues or questions:
1. Check troubleshooting section above
2. Verify API key setup
3. Ensure dependencies are installed
4. Check internet connection

---

## 🎯 Summary

This premium business card generator creates professional, print-ready business cards for Alex Shafiro PT that perfectly match the original Nano Banana prompt specifications. The matte black aesthetic with subtle glow, clean typography, and professional medical positioning make these cards ideal for a high-end rehabilitation practice.

**Generate premium business cards in seconds. Print-ready. Professional quality. Zero compromises.** 🚀
