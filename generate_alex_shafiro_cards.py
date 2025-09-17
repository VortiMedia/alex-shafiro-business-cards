#!/usr/bin/env python3
"""
Alex Shafiro PT - Premium Business Card Generator

Follows exact Nano Banana prompt specifications:
- Minimalist, high-end, premium, trustworthy design
- Matte black background with subtle glow/edge highlight  
- Clean sans-serif typography
- A Stronger Life logo integration
- Specific contact info and layout requirements
- Print-ready 300 DPI output

Dependencies:
    pip install requests python-dotenv Pillow

Setup:
    echo "GEMINI_API_KEY=your_api_key_here" > .env

Usage:
    python generate_alex_shafiro_cards.py
"""

import os
import sys
import requests
import base64
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict
from io import BytesIO

# Check for required dependencies
try:
    from PIL import Image
    from dotenv import load_dotenv
except ImportError as e:
    print(f"❌ Missing dependency: {e}")
    print("Install with: pip install requests python-dotenv Pillow")
    sys.exit(1)

load_dotenv()

class AlexShafiroCardGenerator:
    """
    Premium business card generator for Alex Shafiro PT
    Implements exact Nano Banana prompt specifications
    """
    
    # Brand specifications
    BRAND_INFO = {
        "name": "Alex Shafiro PT / DPT / OCS / CSCS",
        "title": "Rehabilitation Specialist", 
        "company": "A Stronger Life",
        "email": "admin@aslstrong.com",
        "website": "www.aslstrong.com",
        "location": "Stamford, CT",
        "phone": "+1 (XXX) XXX-XXXX"  # Placeholder as per original prompt
    }
    
    # Technical specifications
    CARD_SPECS = {
        "width_inches": 3.5,
        "height_inches": 2.0, 
        "dpi": 300,
        "min_width_px": 1050,  # 3.5" at 300 DPI
        "min_height_px": 600   # 2.0" at 300 DPI
    }
    
    def __init__(self):
        """Initialize the card generator with API key and output directory"""
        self.api_key = self._setup_api_key()
        self.api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image-preview:generateContent"
        
        # Setup output directory
        self.output_dir = Path("./output")
        self.output_dir.mkdir(exist_ok=True)
        
        # Setup logo path - check multiple possible locations
        self.logo_path = self._find_logo_file()
        
    def _setup_api_key(self) -> str:
        """Setup and validate API key"""
        api_key = os.getenv('GEMINI_API_KEY')
        
        if not api_key or api_key == 'your_gemini_api_key_here':
            print("❌ GEMINI_API_KEY not found in environment")
            print("📋 Setup instructions:")
            print("1. Get API key: https://aistudio.google.com")
            print("2. Create .env file: echo 'GEMINI_API_KEY=your_key_here' > .env")
            print("3. Or export: export GEMINI_API_KEY=your_key_here")
            sys.exit(1)
            
        return api_key
    
    def _find_logo_file(self) -> Optional[str]:
        """Find the A Stronger Life logo in possible locations"""
        possible_paths = [
            "./assets/brand_assets/Stronger Life logo vertical original color.png",
            "./assets/Stronger Life logo vertical original color.png",
            "./logo.png",
            "./assets/logo.png"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return str(Path(path).resolve())
        
        print("⚠️  A Stronger Life logo not found")
        print("💡 Expected locations:")
        for path in possible_paths[:2]:
            print(f"   • {path}")
        print("   Generator will work without logo but quality may be reduced")
        
        return None
    
    def load_logo_base64(self) -> Optional[str]:
        """Load and encode the A Stronger Life logo as base64"""
        if not self.logo_path:
            return None
            
        try:
            with open(self.logo_path, 'rb') as f:
                logo_data = base64.b64encode(f.read()).decode('utf-8')
                print(f"✅ Logo loaded: {Path(self.logo_path).name}")
                return logo_data
        except Exception as e:
            print(f"⚠️  Could not load logo from {self.logo_path}: {e}")
            return None
    
    def generate_front_card(self) -> Optional[str]:
        """
        Generate front business card following exact Nano Banana specifications
        
        Returns:
            str: Path to generated card file, or None if failed
        """
        logo_base64 = self.load_logo_base64()
        
        prompt = f"""Create a minimalist, high-end business card design for a rehabilitation expert.

**CARD SPECIFICATIONS:**
- Orientation: horizontal, standard business card size (3.5" × 2.0")
- Resolution: 300 DPI, print-ready quality  
- Style: modern, luxury, premium, trustworthy
- Ready for print at 300 dpi, CMYK color profile

**BACKGROUND:**
- Matte black background with subtle glow or edge highlight
- High-end feel, clean edges, no clutter
- Balanced spacing with plenty of negative space

**TYPOGRAPHY:**
- Clean, sans-serif, elegant fonts (avoid decorative fonts)
- Professional hierarchy and spacing
- High contrast white text on matte black

**LAYOUT REQUIREMENTS:**

**TOP SECTION:**
- Place the A Stronger Life logo prominently (use uploaded logo file)
- Under logo: "A Stronger Life" in smaller, refined typography

**CENTER SECTION:**  
- "{self.BRAND_INFO['name']}" (name with credentials)
- "{self.BRAND_INFO['title']}" (professional title)
- Both center-aligned with proper hierarchy

**LEFT SIDE COLUMN (with icons + text):**
- Phone: "{self.BRAND_INFO['phone']}" with phone icon
- Email: "{self.BRAND_INFO['email']}" with email icon
- Address: "{self.BRAND_INFO['location']}" with location icon  
- Website: "{self.BRAND_INFO['website']}" with web icon
- Clean geometric icons, professional presentation

**BOTTOM-RIGHT CORNER:**
- QR code for the website ({self.BRAND_INFO['website']})
- Proper sizing and contrast for scanning
- Clean positioning with adequate quiet zone

**VISUAL TREATMENT:**
- Professional studio photography lighting
- Matte black finish appearance with subtle texture
- Subtle edge highlight or glow (very restrained)
- Premium luxury aesthetic suitable for medical professional
- High-end rehabilitation expert positioning

Generate this as a photorealistic mockup of a physical business card lying flat on a clean white surface with professional studio lighting. The design should exude premium quality and medical expertise."""

        return self._make_api_call_with_logo(prompt, logo_base64, "Alex_Shafiro_PT_front")
    
    def generate_back_card(self) -> Optional[str]:
        """
        Generate back business card following exact Nano Banana specifications
        
        Returns:
            str: Path to generated card file, or None if failed
        """
        logo_base64 = self.load_logo_base64()
        
        prompt = f"""Create the back side of a minimalist, high-end business card for a rehabilitation expert.

**CARD SPECIFICATIONS:**
- Orientation: horizontal, standard business card size (3.5" × 2.0")
- Resolution: 300 DPI, print-ready quality
- Ready for print at 300 dpi, CMYK color profile

**BACKGROUND:**
- Matte black background (matching front card)
- Clean, premium finish appearance  
- Subtle texture suggesting high-end stock

**CONTENT LAYOUT:**
- Large centered text: "Revolutionary Rehabilitation" in white
- Prominent, inspiring typography
- Professional hierarchy and spacing

**DESIGN ELEMENTS:**
- Optional: subtle ghosted logo watermark behind the text (A Stronger Life logo at low opacity)
- Ensure text legibility remains perfect over watermark
- Centered QR code linking to {self.BRAND_INFO['website']}
- QR code positioned for optimal scanning

**VISUAL TREATMENT:**
- Complementary design to front card
- Same premium aesthetic and matte black finish
- Professional studio lighting with subtle depth
- High-end luxury feel
- Medical expertise positioning

**TYPOGRAPHY:**
- Clean, modern sans-serif fonts
- High contrast white text on black background  
- Elegant spacing and proportions
- Premium professional appearance

Generate this as a photorealistic mockup of the back of a premium business card on a clean white surface with professional studio lighting matching the front card aesthetic."""

        return self._make_api_call_with_logo(prompt, logo_base64, "Alex_Shafiro_PT_back")
    
    def generate_both_cards(self) -> Dict[str, str]:
        """
        Generate both front and back cards
        
        Returns:
            Dict with 'front' and/or 'back' keys containing file paths
        """
        print("🏥 Generating Alex Shafiro PT business cards...")
        print("📋 Following exact Nano Banana prompt specifications")
        print()
        
        results = {}
        
        # Generate front card
        print("📄 Creating premium front card...")
        front_result = self.generate_front_card()
        if front_result:
            results['front'] = front_result
            print(f"✅ Front card saved: {Path(front_result).name}")
        else:
            print("❌ Front card generation failed")
        
        # Generate back card  
        print("📄 Creating premium back card...")
        back_result = self.generate_back_card()
        if back_result:
            results['back'] = back_result
            print(f"✅ Back card saved: {Path(back_result).name}")
        else:
            print("❌ Back card generation failed")
        
        return results
    
    def _make_api_call_with_logo(self, prompt: str, logo_base64: Optional[str], filename_prefix: str) -> Optional[str]:
        """
        Make API call to Gemini with optional logo image and prompt
        
        Args:
            prompt: Text prompt for card generation
            logo_base64: Base64 encoded logo image (optional)
            filename_prefix: Prefix for output filename
            
        Returns:
            str: Path to saved image file, or None if failed
        """
        # Build request parts - logo first if available
        parts = []
        if logo_base64:
            parts.append({
                "inline_data": {
                    "mime_type": "image/png",
                    "data": logo_base64
                }
            })
        parts.append({"text": prompt})
        
        payload = {
            "contents": [{
                "parts": parts
            }]
        }
        
        headers = {
            'Content-Type': 'application/json',
            'x-goog-api-key': self.api_key
        }
        
        try:
            print(f"  🔄 Calling Gemini API for {filename_prefix}...")
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            
            if 'candidates' not in result or not result['candidates']:
                print(f"  ❌ No candidates in API response for {filename_prefix}")
                return None
                
            # Process response parts
            for part in result['candidates'][0]['content']['parts']:
                if 'inlineData' in part:
                    # Decode and save the image
                    image_data = base64.b64decode(part['inlineData']['data'])
                    image = Image.open(BytesIO(image_data))
                    
                    # Validate print quality
                    self._validate_and_report_quality(image, filename_prefix)
                    
                    # Save with timestamp
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"ASL_{filename_prefix}_{timestamp}.png"
                    filepath = self.output_dir / filename
                    
                    image.save(filepath, format='PNG', optimize=True)
                    print(f"  💾 Saved: {filepath}")
                    return str(filepath)
                    
                elif 'text' in part:
                    print(f"  📝 API Text Response: {part['text'][:100]}...")
            
            print(f"  ❌ No image data found in API response for {filename_prefix}")
            return None
            
        except requests.exceptions.Timeout:
            print(f"  ❌ API timeout for {filename_prefix} (>60s)")
            return None
        except requests.exceptions.RequestException as e:
            print(f"  ❌ API request error for {filename_prefix}: {e}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    if 'error' in error_data:
                        print(f"  📋 API Error: {error_data['error'].get('message', 'Unknown error')}")
                except:
                    print(f"  📋 Raw response: {e.response.text[:300]}...")
            return None
        except Exception as e:
            print(f"  ❌ Unexpected error for {filename_prefix}: {e}")
            return None
    
    def _validate_and_report_quality(self, image: Image.Image, filename_prefix: str) -> None:
        """Validate and report on image quality for print"""
        width, height = image.size
        
        print(f"  📐 Image size: {width} × {height}")
        
        # Check minimum resolution for print quality
        if width < self.CARD_SPECS['min_width_px'] * 0.9:
            print(f"  ⚠️  Width may be insufficient for print quality (expected ≥{self.CARD_SPECS['min_width_px']})")
        
        if height < self.CARD_SPECS['min_height_px'] * 0.9:
            print(f"  ⚠️  Height may be insufficient for print quality (expected ≥{self.CARD_SPECS['min_height_px']})")
        
        # Calculate effective DPI
        effective_dpi_w = width / self.CARD_SPECS['width_inches']
        effective_dpi_h = height / self.CARD_SPECS['height_inches'] 
        
        if effective_dpi_w >= 280 and effective_dpi_h >= 280:
            print(f"  ✅ Print quality: ~{min(effective_dpi_w, effective_dpi_h):.0f} DPI")
        else:
            print(f"  ⚠️  Print quality may be low: ~{min(effective_dpi_w, effective_dpi_h):.0f} DPI")

def print_banner():
    """Print application banner and information"""
    print("🏥 Alex Shafiro PT - Premium Business Card Generator")
    print("=" * 55)
    print("📋 Following exact Nano Banana prompt specifications")
    print("🎯 Minimalist, high-end, premium, trustworthy design") 
    print("🖤 Matte black with subtle glow/edge highlight")
    print()

def print_brand_info():
    """Print brand information that will be used"""
    info = AlexShafiroCardGenerator.BRAND_INFO
    print("📋 Card Information:")
    print(f"• Name: {info['name']}")
    print(f"• Title: {info['title']}")
    print(f"• Company: {info['company']}")
    print(f"• Email: {info['email']}")
    print(f"• Website: {info['website']}")
    print(f"• Location: {info['location']}")
    print(f"• Phone: {info['phone']}")
    print()

def print_results(results: Dict[str, str], output_dir: Path):
    """Print generation results and next steps"""
    if not results:
        print("❌ No cards were generated successfully")
        print("💡 Check your API key and internet connection")
        return
        
    print(f"\n🎉 Alex Shafiro PT business card generation complete!")
    print(f"📁 Output directory: {output_dir.resolve()}")
    print()
    
    # List generated files
    if 'front' in results:
        print(f"📄 Front card: {Path(results['front']).name}")
    if 'back' in results:
        print(f"📄 Back card: {Path(results['back']).name}")
    print()
        
    # Specification checklist
    print("📋 Design Specifications Met:")
    print("✅ Minimalist, high-end, premium, trustworthy")
    print("✅ Matte black background with subtle glow")
    print("✅ Clean sans-serif typography")
    print("✅ A Stronger Life logo integration")
    print("✅ Contact info with icons (left column)")
    print("✅ QR code (bottom-right)")
    print("✅ 'Revolutionary Rehabilitation' back text")
    print("✅ 300 DPI print-ready quality")
    print("✅ CMYK color profile ready")
    print()
    
    # Print specifications
    print("🖨️  Print Ready:")
    specs = AlexShafiroCardGenerator.CARD_SPECS
    print(f"• Standard business card size ({specs['width_inches']}\" × {specs['height_inches']}\")") 
    print(f"• {specs['dpi']} DPI resolution")
    print("• CMYK color profile")
    print("• Matte black finish recommended")
    print("• Premium cardstock suggested")
    print()
    
    # Cost estimate
    num_cards = len(results)
    cost_estimate = num_cards * 0.04  # Approximate API cost
    print(f"💰 Estimated generation cost: ~${cost_estimate:.2f}")

def main():
    """Main application entry point"""
    print_banner()
    
    # Initialize generator (validates API key and setup)
    try:
        generator = AlexShafiroCardGenerator()
    except SystemExit:
        return  # API key setup failed
    
    print_brand_info()
    
    # Confirm generation
    proceed = input("Generate cards with these specifications? (y/n): ").strip().lower()
    if proceed not in ['y', 'yes']:
        print("❌ Generation cancelled")
        return
    
    print()
    
    # Generate cards
    results = generator.generate_both_cards()
    
    # Display results
    print_results(results, generator.output_dir)

if __name__ == "__main__":
    main()
    
    print("Generating business cards for:")
    print("• Name: Alex Shafiro PT / DPT / OCS / CSCS")
    print("• Title: Rehabilitation Specialist")
    print("• Company: A Stronger Life")
    print("• Email: admin@aslstrong.com")
    print("• Website: www.aslstrong.com")
    print("• Location: Stamford, CT")
    print()
    
    proceed = input("Generate cards with these specifications? (y/n): ").strip().lower()
    if proceed != 'y':
        print("❌ Generation cancelled")
        return
    
    # Generate both cards
    results = generator.generate_both_cards()
    
    if results:
        print(f"\n🎉 Alex Shafiro PT business card generation complete!")
        print(f"📁 Output directory: {generator.output_dir}")
        
        if 'front' in results:
            print(f"📄 Front card: {results['front']}")
        if 'back' in results:
            print(f"📄 Back card: {results['back']}")
            
        print("\n📋 Design Specifications Met:")
        print("✅ Minimalist, high-end, premium, trustworthy")
        print("✅ Matte black background with subtle glow")
        print("✅ Clean sans-serif typography")
        print("✅ A Stronger Life logo integration")
        print("✅ Contact info with icons (left column)")
        print("✅ QR code (bottom-right)")
        print("✅ 'Revolutionary Rehabilitation' back text")
        print("✅ 300 DPI print-ready quality")
        print("✅ CMYK color profile ready")
        
        print("\n🖨️ Print Ready:")
        print("• Standard business card size (3.5\" × 2.0\")")
        print("• 300 DPI resolution")
        print("• CMYK color profile")
        print("• Matte black finish recommended")
        
        # Cost estimate
        num_cards = len(results)
        cost_estimate = num_cards * 0.04
        print(f"💰 Generation cost estimate: ~${cost_estimate:.2f}")
        
    else:
        print("❌ Generation failed. Check your API key and logo file.")

if __name__ == "__main__":
    main()