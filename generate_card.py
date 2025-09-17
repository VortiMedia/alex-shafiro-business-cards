#!/usr/bin/env python3
"""
A Stronger Life Business Card Generator
Generates actual business card images using Google Gemini 2.5 Flash Image API
"""

import os
import requests
import base64
from datetime import datetime
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()

class StrongerLifeCardGenerator:
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key or self.api_key == 'your_gemini_api_key_here':
            print("❌ Set your GEMINI_API_KEY in .env file")
            print("Get API key: https://aistudio.google.com")
            exit(1)
        
        self.api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image-preview:generateContent"
        self.output_dir = "./output"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def load_reference_image(self, image_path):
        """Load and encode reference image as base64"""
        try:
            with open(image_path, 'rb') as f:
                return base64.b64encode(f.read()).decode('utf-8')
        except Exception as e:
            print(f"⚠️ Could not load reference image: {e}")
            return None
    
    def generate_card_image(self, name, title, phone, email, website=""):
        """Generate actual business card image using Gemini"""
        
        # Try to use existing card as reference
        ref_image = self.load_reference_image("assets/client_projects/current_cards/A STORONGER LIFE_BUSINESS CARD-01.jpg")
        
        prompt = f"""Create a professional business card for A Stronger Life with this person's information:
        
NAME: {name}
TITLE: {title}
PHONE: {phone}
EMAIL: {email}
{f"WEBSITE: {website}" if website else ""}

DESIGN SPECS:
- Exact size: 3.5 inches × 2 inches (standard business card)
- Resolution: 300 DPI print quality
- Brand: A Stronger Life (fitness/wellness company)
- Colors: Emerald green (#10B981), black, white
- Logo: Dynamic human figure (strength/movement theme)
- Style: Modern, clean, professional healthcare/wellness design
- Layout: Logo top-left, company name prominent, contact info with icons
- Typography: Bold, readable sans-serif fonts
- Background: Clean with subtle fitness/wellness elements

Create a photorealistic, print-ready business card mockup with sharp text and professional studio lighting."""

        payload = {
            "contents": [{
                "parts": [
                    {"text": prompt}
                ]
            }]
        }
        
        # Add reference image if available
        if ref_image:
            payload["contents"][0]["parts"].insert(0, {
                "inline_data": {
                    "mime_type": "image/jpeg",
                    "data": ref_image
                }
            })
            payload["contents"][0]["parts"][1]["text"] = f"""Using the reference image as a style guide, create a business card for A Stronger Life with the same design aesthetic but new contact information:

{payload["contents"][0]["parts"][1]["text"]}

Maintain the same color scheme, logo placement, and overall layout style as the reference image."""

        headers = {
            'Content-Type': 'application/json',
            'x-goog-api-key': self.api_key
        }
        
        print(f"🎨 Generating business card image for {name}...")
        
        try:
            response = requests.post(self.api_url, headers=headers, json=payload)
            response.raise_for_status()
            
            result = response.json()
            
            if 'candidates' in result and result['candidates']:
                for part in result['candidates'][0]['content']['parts']:
                    if 'inlineData' in part:
                        # Decode and save the image
                        image_data = base64.b64decode(part['inlineData']['data'])
                        image = Image.open(BytesIO(image_data))
                        
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"ASL_{name.replace(' ', '_')}_{timestamp}.png"
                        filepath = f"{self.output_dir}/{filename}"
                        
                        image.save(filepath)
                        print(f"✅ Business card saved: {filepath}")
                        return filepath
                    elif 'text' in part:
                        print(f"📝 Description: {part['text'][:100]}...")
                
                print("❌ No image generated")
                return None
            else:
                print("❌ No response from API")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"❌ API Error: {e}")
            if hasattr(e.response, 'text'):
                print(f"Response: {e.response.text[:200]}...")
            return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None

def main():
    print("💪 A Stronger Life - Business Card Generator")
    print("=" * 50)
    
    generator = StrongerLifeCardGenerator()
    
    print("\nEnter details for the business card:")
    name = input("Full Name: ").strip()
    title = input("Job Title: ").strip()
    phone = input("Phone: ").strip()
    email = input("Email: ").strip()
    website = input("Website (optional): ").strip()
    
    if not all([name, title, phone, email]):
        print("❌ Name, title, phone, and email are required")
        return
    
    # Generate the card
    result = generator.generate_card_image(name, title, phone, email, website)
    
    if result:
        print(f"\n🎉 Success! Business card generated: {result}")
        print("\n📋 Next steps:")
        print("• Review the generated image")
        print("• Send to printer (already 300 DPI)")
        print("• Or request edits if needed")
        
        another = input("\nGenerate another card? (y/n): ").strip().lower()
        if another == 'y':
            print()
            main()
    else:
        print("❌ Generation failed. Check your API key and try again.")

if __name__ == "__main__":
    main()
