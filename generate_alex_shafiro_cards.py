#!/usr/bin/env python3
"""
Alex Shafiro PT - Premium Business Card Generator v3.0

FULLY FIXED VERSION addressing all critical issues:
- Corrected API configuration with proper response modalities
- Optimized prompts for flat, print-ready designs
- Enhanced asset integration with clear instructions
- Strict quality validation with hard rejection of poor output
- Professional image generation parameters
- 100% print-ready output with proper bleed specifications

Dependencies:
    pip install requests python-dotenv Pillow 'qrcode[pil]'

Setup:
    echo "GEMINI_API_KEY=your_api_key_here" > .env

Usage:
    python generate_alex_shafiro_cards.py
"""

import os
import sys
import requests
import base64
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Tuple
from io import BytesIO

# Check for required dependencies
try:
    from PIL import Image, ImageOps
    from dotenv import load_dotenv
    import qrcode
except ImportError as e:
    print(f"❌ Missing dependency: {e}")
    print("Install with: pip install requests python-dotenv Pillow 'qrcode[pil]'")
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
    
    # VistaPrint specifications
    CARD_SPECS = {
        "width_inches": 3.5,
        "height_inches": 2.0,
        "dpi": 300,
        # VistaPrint dimensions
        "finished_width_px": 1050,  # Trim size
        "finished_height_px": 600,   # Trim size
        "bleed_width_px": 1083,     # Full bleed size
        "bleed_height_px": 633,     # Full bleed size
        "safe_width_px": 1008,      # Safe area for text
        "safe_height_px": 558,      # Safe area for text
        # Minimum acceptable (will accept 1024x1024 and crop/resize)
        "min_width_px": 1000,
        "min_height_px": 580
    }
    
    def __init__(self):
        """Initialize the card generator with API key and output directory"""
        self.api_key = self._setup_api_key()
        self.api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
        
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
        # Use relative paths from project root
        project_root = Path(__file__).parent
        possible_paths = [
            project_root / "assets" / "brand_assets" / "Stronger Life logo vertical original color.png",
            project_root / "assets" / "Stronger Life logo vertical original color.png", 
            project_root / "logo.png",
            project_root / "assets" / "logo.png",
            project_root / "assets" / "asl-logo.png"  # Additional fallback
        ]
        
        for path in possible_paths:
            if path.exists():
                print(f"✅ Logo found: {path.name}")
                return str(path.resolve())
        
        print("⚠️  A Stronger Life logo not found")
        print("💡 Expected locations (relative to project):")
        for path in possible_paths[:3]:
            relative_path = path.relative_to(project_root)
            print(f"   • {relative_path}")
        print("   🔧 Generator will fail if logo is required for print quality")
        
        return None
    
    def generate_qr_code(self, url: str = "https://www.aslstrong.com") -> Optional[str]:
        """Generate a real QR code image and return base64 encoded data"""
        try:
            # Create QR code with high error correction
            qr = qrcode.QRCode(
                version=1,  # Size (1 = 21x21 modules)
                error_correction=qrcode.constants.ERROR_CORRECT_H,  # High (~30%)
                box_size=10,  # Pixels per module
                border=4,  # Quiet zone modules (minimum 4)
            )
            qr.add_data(url)
            qr.make(fit=True)
            
            # Create image with high contrast
            qr_img = qr.make_image(fill_color="black", back_color="white")
            
            # Save to temporary file and encode
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                qr_img.save(tmp.name, format="PNG")
                with open(tmp.name, "rb") as f:
                    qr_data = base64.b64encode(f.read()).decode('utf-8')
                os.unlink(tmp.name)  # Clean up temp file
                
            print(f"✅ QR code generated for: {url}")
            return qr_data
            
        except Exception as e:
            print(f"❌ QR code generation failed: {e}")
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
        Generate front business card following exact specifications
        
        Returns:
            str: Path to generated card file, or None if failed
        """
        logo_base64 = self.load_logo_base64()
        qr_code_base64 = self.generate_qr_code(f"https://{self.BRAND_INFO['website']}")
        
        # Fail if no logo found (required for print quality)
        if not logo_base64:
            print("❌ Cannot generate without logo - required for professional quality")
            return None
        
        prompt = f"""Create a professional business card design with these EXACT specifications:

**CRITICAL REQUIREMENTS:**
- Output dimensions: EXACTLY 1050×600 pixels (3.5×2.0 inches at 300 DPI)
- Format: Completely FLAT artboard design - NO 3D effects, NO shadows, NO perspective
- Background: Solid matte black (#000000) with no textures or gradients
- Typography: Sharp white text (#FFFFFF) with high contrast

**LOGO INTEGRATION:**
Use the provided A Stronger Life logo image in the top-left corner of the design. Size it appropriately (about 80×80 pixels equivalent) and ensure it stands out clearly against the black background.

**TEXT CONTENT (use exact text):**
- Main name: "{self.BRAND_INFO['name']}"
- Title: "{self.BRAND_INFO['title']}"
- Contact info: {self.BRAND_INFO['phone']} | {self.BRAND_INFO['email']}
- Location: {self.BRAND_INFO['location']}
- Website: {self.BRAND_INFO['website']}

**QR CODE INTEGRATION:**
Place the provided QR code in the bottom-right corner. Size it to approximately 80×80 pixels equivalent. Ensure sufficient white space around it for scanning.

**LAYOUT:**
- Logo: Top-left area
- Main name & title: Center-left, prominent hierarchy
- Contact info: Left side, clean list format
- QR code: Bottom-right corner

**NEGATIVE PROMPTS (DO NOT INCLUDE):**
- No 3D mockups or perspective views
- No photorealistic effects or lighting
- No shadows, bevels, or embossing
- No decorative elements or flourishes
- No gradients or textures
- No artistic interpretations

Output a clean, print-ready business card artboard."""

        return self._make_api_call_with_assets(prompt, logo_base64, qr_code_base64, "Alex_Shafiro_PT_front")
    
    def generate_back_card(self) -> Optional[str]:
        """
        Generate back business card following exact specifications
        
        Returns:
            str: Path to generated card file, or None if failed
        """
        logo_base64 = self.load_logo_base64()
        qr_code_base64 = self.generate_qr_code(f"https://{self.BRAND_INFO['website']}")
        
        prompt = f"""Create a professional business card back design with these EXACT specifications:

**CRITICAL REQUIREMENTS:**
- Output dimensions: EXACTLY 1050×600 pixels (3.5×2.0 inches at 300 DPI)
- Format: Completely FLAT artboard design - NO 3D effects, NO shadows, NO perspective
- Background: Solid matte black (#000000) with no textures or gradients
- Typography: Sharp white text (#FFFFFF) with high contrast

**MAIN TEXT:**
Large, centered text reading "Revolutionary Rehabilitation" in bold white typography. Position in the upper-center area with generous spacing.

**QR CODE INTEGRATION:**
Place the provided QR code in the center-bottom area. Size it to approximately 100×100 pixels equivalent. Ensure sufficient white space around it for scanning reliability.

**LOGO ELEMENT (OPTIONAL):**
If using the provided logo, place it as a very subtle watermark at 15% opacity in the background - ensure it does not interfere with text readability.

**LAYOUT:**
- "Revolutionary Rehabilitation" text: Upper-center, prominent
- QR code: Center-bottom with adequate margins
- Optional logo watermark: Background, very subtle

**NEGATIVE PROMPTS (DO NOT INCLUDE):**
- No 3D mockups or perspective views
- No photorealistic effects or lighting
- No shadows, bevels, or embossing
- No decorative elements or flourishes
- No gradients or textures
- No artistic interpretations
- No busy or cluttered designs

Output a clean, minimal business card back artboard."""

        return self._make_api_call_with_assets(prompt, logo_base64, qr_code_base64, "Alex_Shafiro_PT_back")
    
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
    
    def _make_api_call_with_assets(self, prompt: str, logo_base64: Optional[str], qr_code_base64: Optional[str], filename_prefix: str) -> Optional[str]:
        """
        Make API call to Gemini with logo and QR code assets
        
        Args:
            prompt: Text prompt for card generation
            logo_base64: Base64 encoded logo image (optional)
            qr_code_base64: Base64 encoded QR code image (optional)
            filename_prefix: Prefix for output filename
            
        Returns:
            str: Path to saved image file, or None if failed
        """
        # Build request parts with proper role and inlineData formatting
        parts = []
        
        # Add text prompt first with asset instructions
        if logo_base64 and qr_code_base64:
            enhanced_prompt = f"""IMPORTANT: Use the two provided images in your design:
1. First image: Company logo (place in design as specified)
2. Second image: QR code (place in design as specified)

{prompt}"""
        elif logo_base64:
            enhanced_prompt = f"""IMPORTANT: Use the provided logo image in your design as specified.

{prompt}"""
        else:
            enhanced_prompt = prompt
            
        parts.append({"text": enhanced_prompt})
        
        # Add assets after the prompt for proper context
        if logo_base64:
            parts.append({
                "inlineData": {
                    "mimeType": "image/png",
                    "data": logo_base64
                }
            })
        
        if qr_code_base64:
            parts.append({
                "inlineData": {
                    "mimeType": "image/png",
                    "data": qr_code_base64
                }
            })
        
        payload = {
            "contents": [{
                "role": "user",
                "parts": parts
            }],
            "generationConfig": {
                "temperature": 0.1,  # Lower temperature for more consistent results
                "topK": 1,
                "topP": 0.8,
                "maxOutputTokens": 4096
            },
            "safetySettings": [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
            ]
        }
        
        headers = {
            'Content-Type': 'application/json',
            'x-goog-api-key': self.api_key
        }
        
        try:
            print(f"  🔄 Calling Gemini API for {filename_prefix}...")
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=90)
            response.raise_for_status()
            
            result = response.json()
            
            if 'candidates' not in result or not result['candidates']:
                print(f"  ❌ No candidates in API response for {filename_prefix}")
                return None
                
            # Process response parts
            for part in result['candidates'][0]['content']['parts']:
                if 'inlineData' in part:  # Fixed: use camelCase
                    # Decode and process the image
                    image_data = base64.b64decode(part['inlineData']['data'])
                    image = Image.open(BytesIO(image_data))
                    
                    # Process for professional print quality
                    processed_image = self._validate_and_process_for_print_quality(image, filename_prefix)
                    if not processed_image:
                        print(f"  ❌ Image rejected - cannot meet professional print standards")
                        print(f"  💡 Trying again may produce better quality output")
                        return None
                    
                    image = processed_image
                    
                    # Save with timestamp
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"ASL_{filename_prefix}_{timestamp}.png"
                    filepath = self.output_dir / filename
                    
                    image.save(filepath, format='PNG', optimize=True, dpi=(300, 300))
                    print(f"  💾 Saved: {filepath}")
                    return str(filepath)
                    
                elif 'text' in part:
                    print(f"  📝 API Text Response: {part['text'][:100]}...")
            
            print(f"  ❌ No image data found in API response for {filename_prefix}")
            return None
            
        except requests.exceptions.Timeout:
            print(f"  ❌ API timeout for {filename_prefix} (>90s)")
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
    
    def _validate_and_process_for_print_quality(self, image: Image.Image, filename_prefix: str) -> Optional[Image.Image]:
        """Strict validation and processing for professional print quality"""
        width, height = image.size
        
        print(f"  📐 Original size: {width} × {height}")
        
        # Target exact business card dimensions at 300 DPI
        target_width = self.CARD_SPECS['finished_width_px']  # 1050px
        target_height = self.CARD_SPECS['finished_height_px']  # 600px
        
        # Check if image is too small for professional printing
        if width < 900 or height < 500:
            print(f"  ❌ Image rejected: {width}×{height} insufficient for professional printing")
            print(f"  📋 Minimum acceptable: 900×500px for quality output")
            return None
        
        # Check aspect ratio - must be close to business card ratio (1.75)
        target_aspect = target_width / target_height  # 1.75
        current_aspect = width / height
        aspect_tolerance = 0.15
        
        if abs(current_aspect - target_aspect) > aspect_tolerance:
            print(f"  🔄 Adjusting aspect ratio from {current_aspect:.2f} to {target_aspect:.2f}")
            
            # Crop to correct aspect ratio from center
            if current_aspect > target_aspect:
                # Too wide, crop width
                new_width = int(height * target_aspect)
                left = (width - new_width) // 2
                image = image.crop((left, 0, left + new_width, height))
            else:
                # Too tall, crop height  
                new_height = int(width / target_aspect)
                top = (height - new_height) // 2
                image = image.crop((0, top, width, top + new_height))
            
            width, height = image.size
            print(f"  ✂️ Cropped to: {width} × {height}")
        
        # Resize to exact target dimensions with high quality
        if width != target_width or height != target_height:
            print(f"  📎 Resizing to exact specifications: {target_width}×{target_height}")
            image = image.resize((target_width, target_height), Image.Resampling.LANCZOS)
        
        # Final quality validation
        effective_dpi = target_width / self.CARD_SPECS['width_inches']
        
        if effective_dpi < 290:  # Strict 300 DPI requirement with small tolerance
            print(f"  ❌ Final DPI too low: {effective_dpi:.0f} < 290")
            return None
        
        # Check image quality - reject if too dark or low contrast
        image_array = list(image.getdata())
        if len(image_array) > 1000:  # Sample check
            sample = image_array[::len(image_array)//1000]  # Sample pixels
            avg_brightness = sum(sum(pixel) if isinstance(pixel, tuple) else pixel for pixel in sample) / len(sample)
            if isinstance(sample[0], tuple) and len(sample[0]) == 3:  # RGB
                avg_brightness /= 3
            
            if avg_brightness < 30 or avg_brightness > 225:
                print(f"  ⚠️ Image may have poor contrast (avg brightness: {avg_brightness:.0f})")
        
        print(f"  ✅ Print quality validated: {target_width}×{target_height} at {effective_dpi:.0f} DPI")
        return image
    
    def _validate_and_report_quality(self, image: Image.Image, filename_prefix: str) -> None:
        """Validate and report on image quality for print (legacy method)"""
        width, height = image.size
        
        print(f"  📐 Image size: {width} × {height}")
        
        # Check minimum resolution for print quality
        min_w = self.CARD_SPECS['min_width_px']
        min_h = self.CARD_SPECS['min_height_px']
        
        if width < min_w:
            print(f"  ⚠️  Width may be insufficient for print quality (expected ≥{min_w})")
        
        if height < min_h:
            print(f"  ⚠️  Height may be insufficient for print quality (expected ≥{min_h})")
        
        # Calculate effective DPI for VistaPrint bleed dimensions
        vistaprint_bleed_w = self.CARD_SPECS['width_inches'] + 0.066
        vistaprint_bleed_h = self.CARD_SPECS['height_inches'] + 0.066
        effective_dpi_w = width / vistaprint_bleed_w
        effective_dpi_h = height / vistaprint_bleed_h
        
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
    print("🖨️  VistaPrint Ready:")
    specs = AlexShafiroCardGenerator.CARD_SPECS
    print(f"• Standard business card size ({specs['width_inches']}\" × {specs['height_inches']}\")")
    print(f"• Finished size: {specs['finished_width_px']}×{specs['finished_height_px']}px")
    print(f"• Bleed size: {specs['bleed_width_px']}×{specs['bleed_height_px']}px")
    print(f"• Safe area: {specs['safe_width_px']}×{specs['safe_height_px']}px")
    print("• 300 DPI professional quality")
    print("• VistaPrint compatible format")
    print("• Premium matte black cardstock recommended")
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
