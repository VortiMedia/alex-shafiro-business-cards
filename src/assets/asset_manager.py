#!/usr/bin/env python3
"""
Asset Manager - Brand Logo Integration System
Manages brand assets for business card generation
"""

import base64
from pathlib import Path
from typing import Optional, Dict, List
from PIL import Image
import io

class AssetManager:
    """Manage brand assets and logo integration for business card generation"""
    
    def __init__(self, assets_dir: str = "assets/brand_assets"):
        self.assets_dir = Path(assets_dir)
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
        
        self._discover_assets()
    
    def _discover_assets(self):
        """Find and catalog available brand assets"""
        self.assets = {}
        
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
                    elif 'vertical' in name:
                        self.assets['logo_vertical'] = file_path
                    else:
                        self.assets['logo'] = file_path
                
                elif 'icon' in name:
                    self.assets['icon'] = file_path
        
        print(f"✅ Discovered {len(self.assets)} brand assets:")
        for key, path in self.assets.items():
            print(f"   • {key}: {path.name}")
    
    def get_logo_path(self, orientation: str = "horizontal") -> Optional[str]:
        """
        Get path to logo file
        
        Args:
            orientation: 'horizontal' or 'vertical'
            
        Returns:
            Path to logo file or None
        """
        key = f"logo_{orientation}"
        if key in self.assets:
            return str(self.assets[key])
        elif 'logo' in self.assets:
            return str(self.assets['logo'])
        return None
    
    def get_brand_color_prompts(self) -> str:
        """Generate prompt text for brand colors"""
        return f"""
**BRAND COLORS (MANDATORY)**:
- Primary Background: Deep obsidian black {self.brand_colors['deep_obsidian_black']}
- Accent Color: Emerald glow {self.brand_colors['emerald_glow']} 
- Text Color: Arctic white {self.brand_colors['arctic_white']}
- Shadow/Border: Charcoal shadow {self.brand_colors['charcoal_shadow']}

CRITICAL: Use ONLY these exact hex colors. No substitutions.
"""
    
    def get_logo_description(self, orientation: str = "horizontal") -> str:
        """Generate prompt description for logo placement"""
        logo_path = self.get_logo_path(orientation)
        
        if not logo_path:
            return "**LOGO**: 'A Stronger Life' text logo placeholder (emerald glow color)"
        
        return f"""**LOGO INTEGRATION**:
- Company logo: "A Stronger Life" 
- Style: Clean, professional medical aesthetic
- Color: Use emerald glow {self.brand_colors['emerald_glow']} for logo elements
- Placement: Integrate naturally into design hierarchy
- Size: Prominent but balanced with other elements
"""
    
    def get_brand_info_prompts(self) -> str:
        """Generate prompt text with all brand information"""
        return f"""
**BRAND INFORMATION**:
Name: {self.brand_info['name']}
Company: {self.brand_info['company']} 
Tagline: {self.brand_info['tagline']}
Email: {self.brand_info['email']}
Website: {self.brand_info['website']}
Location: {self.brand_info['location']}
Phone: {self.brand_info['phone']}
"""
    
    def get_complete_brand_prompt(self, orientation: str = "horizontal") -> str:
        """Get complete brand prompt with colors, logo, and info"""
        return f"""
{self.get_brand_color_prompts()}

{self.get_logo_description(orientation)}

{self.get_brand_info_prompts()}

**STYLE MANDATE**: "Equinox meets Mayo Clinic" - Premium medical luxury aesthetic.
Clean, sophisticated, trustworthy, high-end rehabilitation practice.
"""
    
    def encode_logo_base64(self, orientation: str = "horizontal") -> Optional[str]:
        """
        Encode logo as base64 for direct prompt inclusion
        
        Args:
            orientation: 'horizontal' or 'vertical'
            
        Returns:
            Base64 encoded logo or None
        """
        logo_path = self.get_logo_path(orientation)
        
        if not logo_path or not Path(logo_path).exists():
            return None
        
        try:
            with open(logo_path, 'rb') as f:
                encoded = base64.b64encode(f.read()).decode('utf-8')
            return encoded
        except Exception as e:
            print(f"❌ Failed to encode logo: {e}")
            return None
    
    def get_logo_dimensions(self, orientation: str = "horizontal") -> Optional[tuple]:
        """Get logo dimensions for prompt specifications"""
        logo_path = self.get_logo_path(orientation)
        
        if not logo_path or not Path(logo_path).exists():
            return None
            
        try:
            with Image.open(logo_path) as img:
                return img.size
        except Exception as e:
            print(f"❌ Failed to get logo dimensions: {e}")
            return None
    
    def create_concept_prompts(self) -> Dict[str, str]:
        """Create 4 distinct concept prompts for Phase 1"""
        base_prompt = self.get_complete_brand_prompt()
        
        concepts = {
            'A': f"""
**CONCEPT A: CLINICAL PRECISION**
{base_prompt}

**DESIGN DIRECTION**: 
Medical authority, clinical precision, professional trust.
Clean geometric layouts, surgical precision in typography,
subtle medical cross elements, pristine white space usage.
Think: "Mayo Clinic meets modern design"

**LAYOUT BIAS**: Centered symmetry, medical chart influence
**MOOD**: Authoritative, trustworthy, clinical excellence
""",
            
            'B': f"""
**CONCEPT B: ATHLETIC PERFORMANCE** 
{base_prompt}

**DESIGN DIRECTION**:
Performance, energy, determination, peak physical condition.
Dynamic angles, movement-inspired layouts, strength symbolism,
athletic performance metaphors in design.
Think: "Equinox meets rehabilitation"

**LAYOUT BIAS**: Dynamic asymmetric, energy flow
**MOOD**: Powerful, energetic, peak performance
""",
            
            'C': f"""
**CONCEPT C: LUXURY WELLNESS**
{base_prompt}

**DESIGN DIRECTION**: 
Premium spa aesthetic, luxury wellness, exclusivity.
Minimalist luxury, premium materials suggestion,
sophisticated restraint, high-end wellness retreat vibe.
Think: "Four Seasons spa meets medical expertise"

**LAYOUT BIAS**: Minimal luxury, elegant white space
**MOOD**: Exclusive, sophisticated, premium wellness
""",
            
            'D': f"""
**CONCEPT D: MINIMALIST MODERN**
{base_prompt}

**DESIGN DIRECTION**:
Clean simplicity, modern minimalism, subtle elegance.
Maximum white space, minimal elements, clean typography,
modern architectural influence, Scandinavian simplicity.
Think: "Apple Store meets rehabilitation"

**LAYOUT BIAS**: Ultra-minimal, architectural clean lines
**MOOD**: Clean, modern, effortlessly sophisticated
"""
        }
        
        return concepts