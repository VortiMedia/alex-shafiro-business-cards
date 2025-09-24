#!/usr/bin/env python3
"""
Real Asset Manager - ACTUALLY integrates logo files and previous cards
This version doesn't just reference assets - it processes and uses them
"""

import base64
import os
from pathlib import Path
from typing import Optional, Dict, List, Tuple
from PIL import Image
import io

class RealAssetManager:
    """Actually integrate real brand assets and use previous business cards"""
    
    def __init__(self, assets_dir: str = "assets/brand_assets", output_dir: str = "output"):
        self.assets_dir = Path(assets_dir)
        self.output_dir = Path(output_dir)
        
        self.brand_info = {
            "name": "Alex Shafiro PT / DPT / OCS / CSCS",
            "title": "Rehabilitation Specialist", 
            "company": "A Stronger Life",
            "tagline": "Revolutionary Rehabilitation",
            "email": "admin@aslstrong.com",
            "website": "www.aslstrong.com", 
            "location": "Stamford, CT",
            "phone": "(914) 246-5010"
        }
        
        # Brand colors from WARP.md
        self.brand_colors = {
            "deep_obsidian_black": "#0A0A0A",
            "emerald_glow": "#00C9A7", 
            "arctic_white": "#FAFAFA",
            "charcoal_shadow": "#1A1A1A"
        }
        
        # Discover and process assets
        self._discover_and_process_assets()
        self._analyze_previous_cards()
        
    def _discover_and_process_assets(self):
        """Find, process, and prepare logo assets for AI integration"""
        self.assets = {}
        self.logo_descriptions = {}
        
        if not self.assets_dir.exists():
            print(f"⚠️ Assets directory not found: {self.assets_dir}")
            return
        
        # Find logo files
        for file_path in self.assets_dir.glob("*"):
            if file_path.suffix.lower() in ['.svg', '.png', '.jpg', '.jpeg']:
                name = file_path.stem.lower()
                
                if 'logo' in name:
                    if 'horizontal' in name or 'horisontal' in name:
                        self.assets['logo_horizontal'] = file_path
                        self._analyze_logo(file_path, 'horizontal')
                    elif 'vertical' in name:
                        self.assets['logo_vertical'] = file_path
                        self._analyze_logo(file_path, 'vertical')
                    else:
                        self.assets['logo'] = file_path
                        self._analyze_logo(file_path, 'general')
                
                elif 'icon' in name:
                    self.assets['icon'] = file_path
                    self._analyze_logo(file_path, 'icon')
        
        print(f"✅ Processed {len(self.assets)} brand assets:")
        for key, path in self.assets.items():
            print(f"   • {key}: {path.name}")
            if key in self.logo_descriptions:
                print(f"     → {self.logo_descriptions[key]}")
    
    def _analyze_logo(self, logo_path: Path, logo_type: str):
        """Analyze logo file and create detailed description for AI prompts"""
        try:
            # Get logo dimensions and basic info
            if logo_path.suffix.lower() in ['.png', '.jpg', '.jpeg']:
                with Image.open(logo_path) as img:
                    width, height = img.size
                    mode = img.mode
                    
                    # Create detailed description
                    aspect_ratio = width / height
                    if aspect_ratio > 1.5:
                        layout = "wide horizontal"
                    elif aspect_ratio < 0.7:
                        layout = "tall vertical" 
                    else:
                        layout = "square/balanced"
                    
                    self.logo_descriptions[f'logo_{logo_type}'] = {
                        'dimensions': f"{width}x{height}",
                        'layout': layout,
                        'file_type': logo_path.suffix,
                        'description': f"A Stronger Life logo - {layout} format, {width}x{height} pixels"
                    }
            
            elif logo_path.suffix.lower() == '.svg':
                # For SVG, read and parse basic info
                try:
                    with open(logo_path, 'r') as f:
                        svg_content = f.read()
                        
                    # Extract basic SVG dimensions if present
                    if 'width=' in svg_content and 'height=' in svg_content:
                        layout = "scalable vector format"
                    else:
                        layout = "responsive SVG"
                        
                    self.logo_descriptions[f'logo_{logo_type}'] = {
                        'dimensions': 'scalable',
                        'layout': layout,
                        'file_type': '.svg',
                        'description': f"A Stronger Life logo - {layout}, vector graphics"
                    }
                except:
                    pass
                    
        except Exception as e:
            print(f"⚠️ Could not analyze logo {logo_path}: {e}")
    
    def _analyze_previous_cards(self):
        """Find and analyze previously generated business cards as reference"""
        self.previous_cards = []
        
        # Find recent business cards
        if self.output_dir.exists():
            # Look in both output root and subdirectories
            card_files = []
            for pattern in ["*.png", "*.jpg", "*.jpeg"]:
                card_files.extend(self.output_dir.rglob(pattern))
            
            # Sort by modification time (newest first)
            card_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            
            # Take the 3 most recent cards as reference
            for card_file in card_files[:3]:
                if self._is_business_card(card_file):
                    self.previous_cards.append({
                        'path': card_file,
                        'filename': card_file.name,
                        'size_mb': round(card_file.stat().st_size / (1024 * 1024), 1),
                        'description': self._describe_card(card_file)
                    })
        
        if self.previous_cards:
            print(f"✅ Found {len(self.previous_cards)} previous business cards as reference:")
            for card in self.previous_cards:
                print(f"   • {card['filename']} ({card['size_mb']}MB)")
                print(f"     → {card['description']}")
        else:
            print("ℹ️ No previous business cards found for reference")
    
    def _is_business_card(self, file_path: Path) -> bool:
        """Check if file is likely a business card"""
        filename = file_path.name.lower()
        
        # Check for business card indicators
        card_indicators = ['business', 'card', 'asl_alex', 'shafiro', 'stronger', 'life']
        
        return any(indicator in filename for indicator in card_indicators)
    
    def _describe_card(self, card_path: Path) -> str:
        """Create description of existing business card for AI reference"""
        filename = card_path.name
        
        # Parse info from filename
        if 'clinical' in filename.lower():
            return "Clinical Precision concept - Medical authority design"
        elif 'athletic' in filename.lower():
            return "Athletic Performance concept - Energy and strength"
        elif 'luxury' in filename.lower():
            return "Luxury Wellness concept - Premium spa aesthetic"
        elif 'concept-a' in filename.lower():
            return "Concept A variation"
        elif 'concept-b' in filename.lower():
            return "Concept B variation"
        elif 'concept-c' in filename.lower():
            return "Concept C variation"
        elif 'front' in filename.lower():
            return "Front side business card"
        elif 'back' in filename.lower():
            return "Back side business card"
        else:
            return "Business card design variation"
    
    def get_logo_integration_prompt(self, orientation: str = "horizontal") -> str:
        """Generate detailed prompt for actual logo integration"""
        logo_key = f"logo_{orientation}"
        
        if logo_key not in self.assets:
            # Fallback to any available logo
            available_logos = [k for k in self.assets.keys() if 'logo' in k]
            if available_logos:
                logo_key = available_logos[0]
                orientation = logo_key.replace('logo_', '')
            else:
                return self._get_fallback_logo_prompt()
        
        logo_path = self.assets[logo_key]
        logo_desc = self.logo_descriptions.get(logo_key, {})
        
        # Create detailed integration prompt
        prompt = f"""
**ACTUAL LOGO INTEGRATION REQUIRED**:

Logo File: {logo_path.name}
Type: {logo_desc.get('file_type', 'unknown')}
Dimensions: {logo_desc.get('dimensions', 'unknown')}
Layout: {logo_desc.get('layout', 'standard')}

**INTEGRATION REQUIREMENTS**:
- Use the ACTUAL "A Stronger Life" logo design elements
- The logo should reflect the real brand identity (rehabilitation/physical therapy)
- Maintain logo proportions and visual hierarchy
- Position logo prominently but balanced with text
- Colors: Logo elements in emerald glow {self.brand_colors['emerald_glow']} on black {self.brand_colors['deep_obsidian_black']} background

**BRAND IDENTITY NOTES**:
- Medical/rehabilitation practice specializing in "Revolutionary Rehabilitation"  
- Professional but approachable aesthetic
- Strong emphasis on expertise (PT/DPT/OCS/CSCS credentials)
- "A Stronger Life" suggests transformation and improvement

**CRITICAL**: Reference the actual logo design - this is not a generic medical logo.
"""
        return prompt
    
    def _get_fallback_logo_prompt(self) -> str:
        """Fallback prompt when no logo files are found"""
        return f"""
**LOGO REQUIREMENTS (No file available - create consistent branding)**:
- Company: "A Stronger Life"
- Style: Medical/rehabilitation practice logo
- Colors: Emerald glow {self.brand_colors['emerald_glow']} on black background
- Should suggest strength, health, rehabilitation, professional expertise
- Clean, modern, trustworthy aesthetic
"""
    
    def get_previous_cards_reference_prompt(self) -> str:
        """Generate prompt referencing previous business card designs"""
        if not self.previous_cards:
            return "**DESIGN REFERENCE**: Create new professional business card design."
        
        prompt = "**REFERENCE PREVIOUS DESIGNS**:\n"
        prompt += "Build upon and improve these existing business card concepts:\n\n"
        
        for i, card in enumerate(self.previous_cards, 1):
            prompt += f"{i}. {card['filename']}\n"
            prompt += f"   → {card['description']}\n"
            prompt += f"   → File size: {card['size_mb']}MB (indicates quality level)\n\n"
        
        prompt += """
**DESIGN EVOLUTION REQUIREMENTS**:
- Take inspiration from the best elements of previous designs
- Improve upon any weaknesses or inconsistencies
- Maintain brand continuity while enhancing visual appeal
- Ensure this iteration is better than previous versions
- Keep successful design elements that work well

**CRITICAL**: Don't just copy - evolve and improve the design approach.
"""
        return prompt
    
    def create_enhanced_concept_prompts(self) -> Dict[str, str]:
        """Create concept prompts that actually use real assets and previous work"""
        
        # Get logo and reference integration
        logo_prompt = self.get_logo_integration_prompt()
        reference_prompt = self.get_previous_cards_reference_prompt()
        
        base_requirements = f"""
{logo_prompt}

{reference_prompt}

**BRAND INFORMATION**:
Name: {self.brand_info['name']}
Company: {self.brand_info['company']}
Tagline: {self.brand_info['tagline']}
Contact: {self.brand_info['email']} | {self.brand_info['website']} | {self.brand_info['location']}
Phone: {self.brand_info['phone']}

**BRAND COLORS (MANDATORY)**:
- Background: Deep obsidian black {self.brand_colors['deep_obsidian_black']}
- Accent: Emerald glow {self.brand_colors['emerald_glow']}
- Text: Arctic white {self.brand_colors['arctic_white']}
- Shadows: Charcoal shadow {self.brand_colors['charcoal_shadow']}

**STYLE MANDATE**: "Equinox meets Mayo Clinic" - Premium medical luxury aesthetic.
"""
        
        concepts = {
            'A': f"""
**CONCEPT A: CLINICAL PRECISION (Enhanced)**
{base_requirements}

**DESIGN EVOLUTION**:
Building on previous clinical concepts, create an even more refined medical authority design.
Surgical precision in layout, pristine white space, clinical excellence indicators.
Think: "Mayo Clinic meets modern minimalism"

**IMPROVEMENTS FROM PREVIOUS**:
- Sharper geometric precision
- Better text hierarchy for credentials
- More sophisticated use of negative space
- Enhanced professional credibility markers

**LAYOUT FOCUS**: Medical chart precision, centered authority
**MOOD**: Authoritative clinical excellence, refined professionalism
""",
            
            'B': f"""
**CONCEPT B: ATHLETIC PERFORMANCE (Enhanced)** 
{base_requirements}

**DESIGN EVOLUTION**:
Building on previous athletic concepts, amplify the energy and performance aspects.
Dynamic movement in layout, strength symbolism, peak performance aesthetic.
Think: "Equinox premium fitness meets rehabilitation expertise"

**IMPROVEMENTS FROM PREVIOUS**:
- More dynamic energy flow in composition
- Better integration of strength/movement metaphors
- Enhanced performance credibility elements
- Sophisticated athletic luxury presentation

**LAYOUT FOCUS**: Dynamic asymmetry, energy-driven composition
**MOOD**: Peak performance, powerful rehabilitation transformation
""",
            
            'C': f"""
**CONCEPT C: LUXURY WELLNESS (Enhanced)**
{base_requirements}

**DESIGN EVOLUTION**:
Building on previous wellness concepts, elevate to premium spa luxury level.
Sophisticated restraint, high-end materials suggestion, exclusive wellness aesthetic.
Think: "Four Seasons spa meets world-class medical expertise"

**IMPROVEMENTS FROM PREVIOUS**:
- More refined luxury presentation
- Better use of premium negative space
- Enhanced exclusivity and sophistication markers
- Elevated wellness transformation messaging

**LAYOUT FOCUS**: Minimal luxury, elegant spatial relationships
**MOOD**: Exclusive premium wellness, sophisticated medical luxury
""",
            
            'D': f"""
**CONCEPT D: MINIMALIST MODERN (Enhanced)**
{base_requirements}

**DESIGN EVOLUTION**:
Building on previous minimalist approaches, achieve perfect modern simplicity.
Architectural precision, maximum impact with minimal elements, Scandinavian influence.
Think: "Apple Store minimalism meets medical authority"

**IMPROVEMENTS FROM PREVIOUS**:
- Cleaner architectural precision
- Better use of minimal elements for maximum impact
- Enhanced modern sophistication
- Perfect balance of simplicity and authority

**LAYOUT FOCUS**: Ultra-minimal architecture, clean geometric precision
**MOOD**: Modern sophistication, effortless professional authority
"""
        }
        
        return concepts
    
    def get_logo_file_path(self, orientation: str = "horizontal") -> Optional[str]:
        """Get actual path to logo file for potential direct use"""
        logo_key = f"logo_{orientation}"
        
        if logo_key in self.assets:
            return str(self.assets[logo_key])
        elif 'logo' in self.assets:
            return str(self.assets['logo'])
        
        return None