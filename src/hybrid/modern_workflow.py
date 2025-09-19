#!/usr/bin/env python3
"""
Modern Hybrid Workflow - Business Card Generator v2.0

Dual Model Implementation:
- OpenAI GPT Image 1: High-quality production cards ($0.02-$0.19)
- Google Gemini 2.5 Flash Image: Rapid iteration and drafts ($0.005)

Architecture:
- Phase 1: Gemini for rapid concept exploration (low cost)
- Phase 2: GPT Image 1 for production quality (higher cost, better results)
- Phase 3: Intelligent model selection based on use case

Based on MASTER_IMPLEMENTATION_GUIDE.md specifications
"""

import os
import base64
import io
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List, Literal
from dataclasses import dataclass
from enum import Enum

try:
    from openai import OpenAI
    from google import genai
    from PIL import Image
    from dotenv import load_dotenv
except ImportError as e:
    print(f"❌ Missing dependency: {e}")
    print("Install with: pip install openai>=1.51.0 google-genai>=1.0.0 python-dotenv Pillow")
    raise

# Load environment variables
load_dotenv()

class ModelType(Enum):
    """Available AI models for generation"""
    GPT_IMAGE_1 = "gpt-image-1"
    GEMINI_FLASH = "gemini-2.5-flash-image-preview"
    AUTO = "auto"

@dataclass
class GenerationResult:
    """Result container for image generation"""
    success: bool
    image_data: Optional[bytes] = None
    filepath: Optional[str] = None
    model_used: Optional[str] = None
    cost_estimate: float = 0.0
    processing_time: float = 0.0
    error_message: Optional[str] = None

class ModernHybridWorkflow:
    """
    Modern Dual-Model Business Card Generator
    
    Implements intelligent model selection:
    - Gemini: Rapid iteration, concept exploration, bulk generation
    - GPT Image 1: Production quality, final outputs, critical deliverables
    """
    
    # Brand specifications from v1.0
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
    
    # Color system 
    COLORS = {
        "deep_obsidian_black": "#0A0A0A",
        "emerald_glow": "#00C9A7", 
        "arctic_white": "#FAFAFA",
        "charcoal_shadow": "#1A1A1A"
    }
    
    # Cost estimates (USD) from MASTER_IMPLEMENTATION_GUIDE
    COSTS = {
        "gpt_image_1_low": 0.02,
        "gpt_image_1_medium": 0.07,
        "gpt_image_1_high": 0.19,
        "gemini_flash": 0.005,
    }
    
    def __init__(self):
        """Initialize modern hybrid workflow with both clients"""
        self.setup_clients()
        self.setup_directories()
        
    def setup_clients(self):
        """Initialize OpenAI and Gemini clients"""
        # OpenAI GPT Image 1 client
        openai_key = os.getenv('OPENAI_API_KEY')
        if openai_key:
            self.openai_client = OpenAI(api_key=openai_key)
            self.openai_available = True
            print("✅ OpenAI GPT Image 1 ready")
        else:
            self.openai_client = None
            self.openai_available = False
            print("⚠️ OpenAI API key not found")
            
        # Gemini 2.5 Flash Image client  
        gemini_key = os.getenv('GOOGLE_API_KEY') or os.getenv('GEMINI_API_KEY')
        if gemini_key:
            self.gemini_client = genai.Client(api_key=gemini_key)
            self.gemini_available = True
            print("✅ Google Gemini 2.5 Flash Image ready")
        else:
            self.gemini_client = None
            self.gemini_available = False
            print("⚠️ Google API key not found")
        
        if not (self.openai_available or self.gemini_available):
            raise ValueError("No API keys available. Please set OPENAI_API_KEY and/or GOOGLE_API_KEY")
            
    def setup_directories(self):
        """Create output directories"""
        self.output_dir = Path("./output")
        self.drafts_dir = Path("./output/drafts") 
        self.production_dir = Path("./output/production")
        
        for directory in [self.output_dir, self.drafts_dir, self.production_dir]:
            directory.mkdir(exist_ok=True)
        
        print(f"📁 Output: {self.output_dir.resolve()}")

    def generate_card(
        self, 
        concept: str = "Clinical-Precision", 
        side: str = "front",
        model: ModelType = ModelType.AUTO,
        quality: Literal["draft", "review", "production"] = "production"
    ) -> GenerationResult:
        """
        Generate business card with intelligent model selection
        
        Args:
            concept: Design concept variant
            side: 'front' or 'back'
            model: Specific model to use or AUTO for intelligent selection
            quality: Quality level affecting model and cost selection
            
        Returns:
            GenerationResult with image data and metadata
        """
        print(f"\n🎨 Generating {concept} {side} - {quality} quality")
        start_time = datetime.now()
        
        # Auto-select model based on quality and availability
        selected_model = self._select_model(model, quality)
        if not selected_model:
            return GenerationResult(
                success=False,
                error_message="No suitable model available for request"
            )
        
        # Build prompt optimized for selected model
        prompt = self._build_universal_prompt(concept, side)
        
        try:
            if selected_model == ModelType.GPT_IMAGE_1:
                result = self._generate_with_gpt_image(prompt, quality)
            elif selected_model == ModelType.GEMINI_FLASH:
                result = self._generate_with_gemini(prompt)
            else:
                return GenerationResult(
                    success=False,
                    error_message=f"Unknown model: {selected_model}"
                )
            
            if result.success:
                # Save to appropriate directory
                directory = self.production_dir if quality == "production" else self.drafts_dir
                filepath = self._save_image(
                    result.image_data, 
                    concept, 
                    side, 
                    selected_model.value,
                    directory
                )
                result.filepath = filepath
                
                processing_time = (datetime.now() - start_time).total_seconds()
                result.processing_time = processing_time
                
                print(f"✅ Generated with {selected_model.value} ({processing_time:.1f}s)")
                print(f"💰 Estimated cost: ${result.cost_estimate:.3f}")
                print(f"📄 Saved: {Path(filepath).name}")
            
            return result
            
        except Exception as e:
            return GenerationResult(
                success=False,
                error_message=f"Generation failed: {e}",
                model_used=selected_model.value if selected_model else None
            )

    def _select_model(self, requested: ModelType, quality: str) -> Optional[ModelType]:
        """Intelligent model selection based on requirements and availability"""
        
        if requested != ModelType.AUTO:
            # User specified a model - validate availability
            if requested == ModelType.GPT_IMAGE_1 and self.openai_available:
                return ModelType.GPT_IMAGE_1
            elif requested == ModelType.GEMINI_FLASH and self.gemini_available:
                return ModelType.GEMINI_FLASH
            else:
                print(f"⚠️ Requested model {requested.value} not available, falling back to AUTO")
        
        # Auto selection logic
        if quality == "production" and self.openai_available:
            return ModelType.GPT_IMAGE_1  # Best quality for finals
        elif quality in ["draft", "review"] and self.gemini_available:
            return ModelType.GEMINI_FLASH  # Fast and cost-effective
        elif self.openai_available:
            return ModelType.GPT_IMAGE_1  # Fallback to GPT if available
        elif self.gemini_available:
            return ModelType.GEMINI_FLASH  # Fallback to Gemini
        else:
            return None  # No models available

    def _generate_with_gpt_image(self, prompt: str, quality: str) -> GenerationResult:
        """Generate with OpenAI GPT Image 1"""
        
        # Map quality to OpenAI parameters
        quality_settings = {
            "draft": {"quality": "low", "size": "1024x1024", "cost": self.COSTS["gpt_image_1_low"]},
            "review": {"quality": "medium", "size": "1536x1024", "cost": self.COSTS["gpt_image_1_medium"]},
            "production": {"quality": "high", "size": "1536x1024", "cost": self.COSTS["gpt_image_1_high"]}
        }
        
        settings = quality_settings.get(quality, quality_settings["production"])
        
        try:
            response = self.openai_client.images.generate(
                model='gpt-image-1',
                prompt=prompt,
                size=settings["size"],
                quality=settings["quality"],
                n=1
            )
            
            # Extract image data
            image_data = base64.b64decode(response.data[0].b64_json)
            
            # Validate image
            self._validate_image(image_data)
            
            return GenerationResult(
                success=True,
                image_data=image_data,
                model_used="gpt-image-1",
                cost_estimate=settings["cost"]
            )
            
        except Exception as e:
            return GenerationResult(
                success=False,
                error_message=f"OpenAI generation failed: {e}",
                model_used="gpt-image-1"
            )

    def _generate_with_gemini(self, prompt: str) -> GenerationResult:
        """Generate with Google Gemini 2.5 Flash Image"""
        
        try:
            response = self.gemini_client.models.generate_content(
                model='gemini-2.5-flash-image-preview',
                contents=[prompt]
            )
            
            # Extract image data from response
            image_data = None
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'inline_data') and part.inline_data:
                    image_data = part.inline_data.data
                    break
                    
            if not image_data:
                return GenerationResult(
                    success=False,
                    error_message="No image data in Gemini response",
                    model_used="gemini-2.5-flash-image-preview"
                )
            
            # Validate image
            self._validate_image(image_data)
            
            return GenerationResult(
                success=True,
                image_data=image_data,
                model_used="gemini-2.5-flash-image-preview",
                cost_estimate=self.COSTS["gemini_flash"]
            )
            
        except Exception as e:
            return GenerationResult(
                success=False,
                error_message=f"Gemini generation failed: {e}",
                model_used="gemini-2.5-flash-image-preview"
            )

    def _build_universal_prompt(self, concept: str, side: str) -> str:
        """Build universal prompt optimized for both models"""
        
        base_prompt = f"""Professional business card design for premium rehabilitation practice:

CRITICAL SPECIFICATIONS:
- Completely flat 2D design (NO 3D mockups, NO shadows, NO perspective)
- Business card proportions: 3.5" × 2.0" 
- Deep matte black background ({self.COLORS['deep_obsidian_black']})
- Single emerald accent color ({self.COLORS['emerald_glow']}) for highlights only
- Arctic white text ({self.COLORS['arctic_white']}) for maximum contrast
- "Equinox meets Mayo Clinic" aesthetic - sophisticated restraint

BRAND INFORMATION:
Name: {self.BRAND_INFO['name']}
Company: {self.BRAND_INFO['company']}
Tagline: {self.BRAND_INFO['tagline']}
Email: {self.BRAND_INFO['email']}
Website: {self.BRAND_INFO['website']}
Location: {self.BRAND_INFO['location']}"""

        if side == "front":
            layout_spec = """
FRONT CARD LAYOUT:
- Logo area (top-left): "A Stronger Life" logo placeholder
- Name/title block (center-left): Primary prominence for name
- Contact information (left column): Phone, email, website, location
- QR code area (bottom-right): Small QR code placeholder
- Professional hierarchy with generous negative space"""

        else:  # back
            layout_spec = """
BACK CARD LAYOUT:
- Centered tagline: "Revolutionary Rehabilitation" 
- Bold uppercase lettering with increased letter spacing
- Optional: Subtle company logo watermark at 3% opacity maximum
- Maximum negative space for sophisticated impact"""

        # Add concept-specific styling
        concept_styles = {
            "Clinical-Precision": "Medical authority focus, symmetric layout, clinical trust",
            "Athletic-Edge": "Dynamic energy, performance-focused design elements",
            "Luxury-Wellness": "Equinox-level luxury, spa-like sophistication"
        }
        
        style_spec = f"\nDESIGN CONCEPT: {concept_styles.get(concept, 'Premium professional')}"
        
        return base_prompt + layout_spec + style_spec + "\n\nOUTPUT: Flat artboard design ready for professional printing."

    def _validate_image(self, image_data: bytes):
        """Validate generated image data"""
        try:
            img = Image.open(io.BytesIO(image_data))
            if img.width < 512 or img.height < 512:
                raise ValueError("Generated image resolution too low")
            if img.mode not in ['RGB', 'RGBA']:
                raise ValueError("Invalid image color mode")
        except Exception as e:
            raise ValueError(f"Image validation failed: {e}")

    def _save_image(
        self, 
        image_data: bytes, 
        concept: str, 
        side: str, 
        model: str,
        directory: Path
    ) -> str:
        """Save image data to file with proper naming convention"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        model_short = "GPT1" if "gpt" in model else "GEMINI"
        
        filename = f"ASL_Alex_Shafiro_{concept}_{side}_{model_short}_{timestamp}.png"
        filepath = directory / filename
        
        # Ensure parent directory exists before writing
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(filepath, 'wb') as f:
                f.write(image_data)
            
            # Verify file was created successfully
            if not filepath.exists() or filepath.stat().st_size == 0:
                raise ValueError("Failed to create image file")
                
            return str(filepath)
            
        except Exception as e:
            raise ValueError(f"Image save failed: {e}")

    def generate_full_concept_set(
        self, 
        concept: str = "Clinical-Precision",
        quality: str = "production"
    ) -> Dict[str, GenerationResult]:
        """Generate both front and back cards for a complete concept"""
        
        print(f"\n🏥 Generating complete {concept} set - {quality} quality")
        
        results = {}
        
        # Generate front card
        front_result = self.generate_card(concept, "front", ModelType.AUTO, quality)
        if front_result.success:
            results['front'] = front_result
        
        # Generate back card
        back_result = self.generate_card(concept, "back", ModelType.AUTO, quality)
        if back_result.success:
            results['back'] = back_result
        
        return results

    def check_api_status(self):
        """Check status of both API connections"""
        print("\n🔍 API Status Check:")
        print(f"OpenAI GPT Image 1: {'✅' if self.openai_available else '❌'}")
        print(f"Google Gemini 2.5: {'✅' if self.gemini_available else '❌'}")
        
        if not (self.openai_available or self.gemini_available):
            print("\n⚠️ No APIs available. Please set up API keys:")
            print("OPENAI_API_KEY=sk-xxxxx")
            print("GOOGLE_API_KEY=AIzaxxxxx")

# Usage example
if __name__ == "__main__":
    workflow = ModernHybridWorkflow()
    workflow.check_api_status()
    
    # Generate production quality card
    result = workflow.generate_card("Clinical-Precision", "front", ModelType.AUTO, "production")
    
    if result.success:
        print(f"Success! Generated with {result.model_used}")
    else:
        print(f"Failed: {result.error_message}")