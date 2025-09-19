#!/usr/bin/env python3
"""
Alex Shafiro PT - Business Card Generator v2.0
Using OpenAI's GPT Image 1 for state-of-the-art image generation

Production-ready system that generates print-ready business cards
NOT text descriptions - this actually generates PNG images with superior quality
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict

# Check dependencies
try:
    from openai import OpenAI
    from PIL import Image
    from dotenv import load_dotenv
    import base64
    import io
    import json
except ImportError as e:
    print(f"❌ Missing dependency: {e}")
    print("Install with: pip install openai python-dotenv Pillow")
    sys.exit(1)

# Load environment variables
load_dotenv()

class BusinessCardGenerator:
    """Generate Alex Shafiro PT business cards using OpenAI's GPT Image 1"""
    
    # Brand specifications from PRD
    BRAND_INFO = {
        "name": "Alex Shafiro PT / DPT / OCS / CSCS",
        "title": "Rehabilitation Specialist", 
        "company": "A Stronger Life",
        "tagline": "Revolutionary Rehabilitation",
        "email": "admin@aslstrong.com",
        "website": "www.aslstrong.com",
        "location": "Stamford, CT",
        "phone": "+1 (XXX) XXX-XXXX"
    }
    
    # PRD Color System
    COLORS = {
        "deep_obsidian_black": "#0A0A0A",
        "emerald_glow": "#00C9A7", 
        "arctic_white": "#FAFAFA",
        "charcoal_shadow": "#1A1A1A"
    }
    
    def __init__(self):
        """Initialize the generator"""
        self.setup_api()
        self.setup_directories()
        
    def setup_api(self):
        """Setup OpenAI API client for GPT Image 1"""
        api_key = os.getenv('OPENAI_API_KEY')
        
        if not api_key:
            print("❌ API Key not found!")
            print("Setup instructions:")
            print("1. Get key from: https://platform.openai.com/api-keys")
            print("2. Set environment variable:")
            print("   export OPENAI_API_KEY='your_key_here'")
            print("3. Or create .env file with: OPENAI_API_KEY=your_key_here")
            sys.exit(1)
            
        try:
            # Create the OpenAI client
            self.client = OpenAI(api_key=api_key)
            print("✅ OpenAI client initialized")
            print("✨ Image generation ready (GPT Image 1 - Latest Model)")
        except Exception as e:
            print(f"❌ Failed to initialize OpenAI client: {e}")
            sys.exit(1)
    
    def setup_directories(self):
        """Create output directories"""
        self.output_dir = Path("./output")
        self.output_dir.mkdir(exist_ok=True)
        print(f"📁 Output directory: {self.output_dir.resolve()}")
    
    def generate_front_card(self, concept: str = "Clinical-Precision") -> Optional[str]:
        """
        Generate front business card using Gemini image generation
        
        Args:
            concept: Design concept variant
            
        Returns:
            Path to generated image file or None if failed
        """
        print(f"\n🎨 Generating front card - {concept.replace('-', ' ')}...")
        
        # Craft the prompt using OpenAI GPT Image 1 best practices
        prompt = f"""Ultra-premium business card front design with these EXACT specifications:

**SUBJECT & CONTEXT:**
Professional business card for Alex Shafiro PT, a premium rehabilitation specialist, 
on a deep matte black background (#0A0A0A), embodying Equinox-meets-medical excellence.

**STYLE & MEDIUM:**
Clean, minimalist luxury design, flat artboard presentation (NO 3D mockups, NO shadows, NO perspective), 
studio-quality commercial design, vector-sharp quality.

**LIGHTING & MOOD:**
Subtle emerald glow accent (#00C9A7) at 15% opacity, high contrast arctic white text (#FAFAFA), 
sophisticated premium aesthetic commanding instant respect.

**LAYOUT & FRAMING:**
- Logo area (top-left): "A Stronger Life" company logo placeholder, exactly 0.75" height equivalent
- Identity block (center-left): "{self.BRAND_INFO['name']}" in 14pt bold, tracked +50
- Contact info (left column): Phone, email, location in clean hierarchy
- QR code area (bottom-right): 0.5" x 0.5" placeholder for website QR code
- Typography: Helvetica Neue or clean sans-serif, arctic white text

**QUALITY MODIFIERS:**
Professional design, ultra-detailed, print-ready quality, commercial grade, 
exact business card proportions 3.5" x 2.0", high dynamic range.

**CRITICAL REQUIREMENTS:**
- Aspect ratio 16:9 to approximate business card proportions
- Deep matte black background (not gray or charcoal)
- Single emerald accent color only 
- 40% negative space minimum
- Flat artboard design ready for print
- Text within safe zones

Output a professional business card front design ready for immediate printing."""

        return self._generate_image(prompt, f"{concept}_front")
    
    def generate_back_card(self, concept: str = "Clinical-Precision") -> Optional[str]:
        """
        Generate back business card using Gemini image generation
        
        Args:
            concept: Design concept variant
            
        Returns:
            Path to generated image file or None if failed
        """
        print(f"\n🎨 Generating back card - {concept.replace('-', ' ')}...")
        
        prompt = f"""Ultra-premium business card back design with these EXACT specifications:

**SUBJECT & CONTEXT:**
Professional business card back for premium rehabilitation practice, 
deep matte black background (#0A0A0A), minimal luxury aesthetic.

**STYLE & MEDIUM:**
Clean, minimalist design, flat artboard presentation (NO 3D mockups, NO shadows), 
studio-quality commercial design, vector-sharp quality.

**LIGHTING & MOOD:**
Subtle emerald glow underglow on main text (#00C9A7) at 20% opacity, 
high contrast arctic white text (#FAFAFA), sophisticated restraint.

**LAYOUT & FRAMING:**
- Primary text (center): "Revolutionary Rehabilitation" in bold 16pt, tracked +150, all caps
- Perfect optical centering with generous negative space
- Optional: Subtle company logo watermark at 3% opacity maximum
- QR code area (center-bottom): Small placeholder for website

**QUALITY MODIFIERS:**
Professional design, ultra-detailed, print-ready quality, commercial grade,
exact business card proportions 3.5" x 2.0", high dynamic range.

**CRITICAL REQUIREMENTS:**
- Aspect ratio 16:9 to approximate business card proportions  
- Deep matte black background (not gray)
- Single emerald accent only
- Minimal text - maximum impact
- Flat artboard design ready for print
- Premium restraint over embellishment

Output a sophisticated business card back design ready for immediate printing."""

        return self._generate_image(prompt, f"{concept}_back")
    
    def _generate_image(self, prompt: str, filename_prefix: str) -> Optional[str]:
        """
        Generate actual image using OpenAI's GPT Image 1 and save to file
        
        Args:
            prompt: Text prompt for image generation
            filename_prefix: Prefix for output filename
            
        Returns:
            Path to saved image or None if failed
        """
        try:
            print(f"  🎨 Calling OpenAI GPT Image 1 API...")
            
            # Generate image using OpenAI's latest model
            response = self.client.images.generate(
                model='gpt-image-1',
                prompt=prompt,
                size='1536x1024',  # Wider format better for business cards
                quality='high',     # High quality for professional printing
                n=1                 # Generate 1 image at a time
            )
            
            # Check if we got a valid response
            if not response.data or len(response.data) == 0:
                print(f"  ❌ No image data in response")
                return None
            
            # Get the base64 encoded image data
            image_b64 = response.data[0].b64_json
            
            if not image_b64:
                print(f"  ❌ No base64 image data found")
                return None
            
            # Decode base64 to bytes
            try:
                image_data = base64.b64decode(image_b64)
            except Exception as decode_err:
                print(f"  ❌ Failed to decode base64 image: {decode_err}")
                return None
            
            # Create timestamp for unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ASL_Alex_Shafiro_{filename_prefix}_{timestamp}.png"
            filepath = self.output_dir / filename
            
            # Save the image
            try:
                with open(filepath, 'wb') as f:
                    f.write(image_data)
            except Exception as save_err:
                print(f"  ❌ Failed to save image: {save_err}")
                return None
            
            # Verify the file was created and has content
            if not filepath.exists() or filepath.stat().st_size == 0:
                print(f"  ❌ Failed to save image file")
                return None
            
            print(f"  ✅ Image generated successfully: {filename}")
            print(f"  📏 File size: {filepath.stat().st_size / 1024:.1f} KB")
            
            # Display image info using PIL
            try:
                with Image.open(filepath) as img:
                    print(f"  🖼️ Dimensions: {img.width}x{img.height} pixels")
                    print(f"  🎨 Format: {img.format} ({img.mode})")
                    print(f"  💎 Quality: High (GPT Image 1 Premium)")
            except Exception as img_err:
                print(f"  ⚠️ Could not read image info: {img_err}")
            
            return str(filepath)
                
        except Exception as e:
            print(f"  ❌ Image generation failed: {e}")
            print(f"  📝 Error type: {type(e).__name__}")
            # Try to provide more helpful error messages
            if 'quota' in str(e).lower() or 'limit' in str(e).lower():
                print(f"  💳 This might be a quota/billing issue. Check your OpenAI usage limits.")
            elif 'auth' in str(e).lower() or 'api' in str(e).lower():
                print(f"  🔑 This might be an authentication issue. Check your OPENAI_API_KEY.")
            elif 'content_policy' in str(e).lower():
                print(f"  🚫 Content policy violation. Try adjusting your prompt.")
            elif 'invalid' in str(e).lower():
                print(f"  ⚠️ Invalid request. Check model name and parameters.")
            
            return None
    
    
    def generate_concept_set(self, concept: str = "Clinical-Precision") -> Dict[str, Optional[str]]:
        """
        Generate both front and back cards for a concept
        
        Args:
            concept: Design concept to generate
            
        Returns:
            Dict with front/back file paths
        """
        print(f"\n🏥 Generating {concept.replace('-', ' ')} business card set...")
        
        results = {}
        
        # Generate front card
        front_result = self.generate_front_card(concept)
        if front_result:
            results['front'] = front_result
        
        # Generate back card  
        back_result = self.generate_back_card(concept)
        if back_result:
            results['back'] = back_result
        
        return results
    
    def generate_all_concepts(self) -> Dict[str, Dict[str, Optional[str]]]:
        """
        Generate all three concept variations
        
        Returns:
            Dict of concept results
        """
        print("🎯 Generating Alex Shafiro PT Premium Business Card System")
        print("Based on PRD specifications - Equinox meets Mayo Clinic\n")
        
        concepts = [
            "Clinical-Precision",
            "Athletic-Edge", 
            "Luxury-Wellness"
        ]
        
        all_results = {}
        
        for concept in concepts:
            results = self.generate_concept_set(concept)
            if results:
                all_results[concept] = results
                print(f"✅ {concept.replace('-', ' ')} concept complete")
            else:
                print(f"❌ {concept.replace('-', ' ')} concept failed")
        
        return all_results

def print_banner():
    """Print application banner"""
    print("🏥 Alex Shafiro PT - Premium Business Card Generator")
    print("=" * 55)
    print("🎨 Powered by Gemini 2.5 Flash Image (Nano Banana)")
    print("✨ ACTUAL image generation - Ready for print")
    print("🔥 Equinox meets Mayo Clinic aesthetic")
    print()

def print_results(all_results: Dict[str, Dict[str, Optional[str]]], generator):
    """Print generation results"""
    if not all_results:
        print("❌ No cards were generated successfully")
        print("\n🔍 Troubleshooting:")
        print("1. Check your GEMINI_API_KEY is valid")
        print("2. Verify internet connection")
        print("3. Try running individual concepts")
        return
    
    print(f"\n🎉 Image Generation Complete!")
    print(f"📁 Output directory: {generator.output_dir.resolve()}\n")
    
    # List generated image files
    total_images = 0
    for concept, files in all_results.items():
        concept_name = concept.replace('-', ' ')
        print(f"🎨 {concept_name}:")
        if 'front' in files:
            print(f"  🇫 Front Card: {Path(files['front']).name}")
            total_images += 1
        if 'back' in files:
            print(f"  🇫 Back Card: {Path(files['back']).name}")
            total_images += 1
        print()
    
    print("📋 Next Steps:")
    print("1. 🔍 Open images to review quality and layout")
    print("2. 🖨️ Print test cards on standard business card stock (3.5\" x 2\")")
    print("3. 🎯 Upload final versions to VistaPrint or local print shop")
    print("4. 💼 Consider creating variations for team members")
    
    print(f"\n📊 Generated {total_images} high-quality images")
    print(f"💰 Estimated Gemini API cost: ~${total_images * 0.005:.3f}")

def main():
    """Main application entry point"""
    print_banner()
    
    # Initialize generator
    try:
        generator = BusinessCardGenerator()
    except SystemExit:
        return
    
    # Show brand info
    brand = generator.BRAND_INFO
    print("📋 Brand Information:")
    print(f"• Name: {brand['name']}")
    print(f"• Company: {brand['company']}")
    print(f"• Tagline: {brand['tagline']}")
    print(f"• Website: {brand['website']}")
    print()
    
    # Generation options
    print("🎨 Generation Options:")
    print("1. Generate all three concepts (Recommended)")
    print("2. Generate single concept (Clinical Precision)")
    print("3. Generate single concept (Athletic Edge)")
    print("4. Generate single concept (Luxury Wellness)")
    print()
    
    choice = input("Select option (1-4): ").strip()
    
    if choice == "1":
        # Generate all concepts
        proceed = input("Generate all three concept variations? (y/n): ").strip().lower()
        if proceed not in ['y', 'yes']:
            print("❌ Generation cancelled")
            return
        
        all_results = generator.generate_all_concepts()
        print_results(all_results, generator)
        
    elif choice in ["2", "3", "4"]:
        # Generate single concept
        concept_map = {
            "2": "Clinical-Precision",
            "3": "Athletic-Edge",
            "4": "Luxury-Wellness" 
        }
        
        concept = concept_map[choice]
        concept_name = concept.replace('-', ' ')
        
        proceed = input(f"Generate {concept_name} concept? (y/n): ").strip().lower()
        if proceed not in ['y', 'yes']:
            print("❌ Generation cancelled")
            return
        
        results = generator.generate_concept_set(concept)
        if results:
            print_results({concept: results}, generator)
        else:
            print(f"❌ {concept_name} generation failed")
    
    else:
        print("❌ Invalid selection")

if __name__ == "__main__":
    main()