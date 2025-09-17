# A Stronger Life - Business Card Generator

> Generate professional business cards using Google Gemini 2.5 Flash Image API

## 🚀 Quick Start

```bash
# Install dependencies
pip install requests python-dotenv Pillow

# Set up API key
echo "GEMINI_API_KEY=your_api_key_here" > .env

# Generate cards
python generate_card.py
```

## 🎨 What it does

Generates professional business card images for A Stronger Life using the existing brand style.

## 🔑 Setup

1. **Get API Key**: Go to [Google AI Studio](https://aistudio.google.com) and create an API key
2. **Install**: `pip install requests python-dotenv Pillow`
3. **Configure**: `echo "GEMINI_API_KEY=your_key_here" > .env`
4. **Run**: `python generate_card.py`

## 💰 Cost

~$0.04 per business card image generated.

## 📝 Usage

Run the script and enter the person's details:
```
python generate_card.py
```

Example:
```
Full Name: John Smith
Job Title: Personal Trainer
Phone: (555) 123-4567
Email: john@strongerlife.com
Website: strongerlife.com
```

Generates: `output/ASL_John_Smith_20250117_143052.png`

## 🚀 Features

- Generates actual PNG images (not just descriptions)
- Uses A Stronger Life brand colors and style
- 300 DPI print-ready quality
- References existing brand assets for consistency
- Simple command-line interface

## 🔧 Files

- `generate_card.py` - Main script
- `assets/brand_assets/` - Logo files
- `assets/client_projects/current_cards/` - Reference designs
- `output/` - Generated business cards

That's it! Simple, focused, and gets results.
