# Implementation Guide: Business Card Generator v3.0

**Production-ready dual-model AI business card generator**

## Quick Start

```bash
# Install
pip install -r requirements.txt

# Configure
export OPENAI_API_KEY="sk-xxxxx"
export GOOGLE_API_KEY="AIzaxxxxx" 

# Run
python generate_business_cards.py
```

## Architecture

**Core Components:**
- `generate_business_cards.py` - Main CLI application
- `src/hybrid/modern_workflow.py` - Dual-model generation engine
- `src/validation/` - Image validation system
- `src/monitoring/` - API status monitoring
- `tests/` - Comprehensive test suite (93.4% coverage)

**Model Strategy:**
| Use Case | Model | Cost | Resolution |
|----------|-------|------|-----------|
| **Draft/Review** | Gemini | $0.005 | 1024×1024 |
| **Production** | GPT Image 1 | $0.02-$0.19 | 1536×1024 |

---

## Implementation Code

```python
#!/usr/bin/env python3
"""
Dual-Model Business Card Generator
Supports OpenAI GPT Image 1 and Google Gemini
"""

import os
import base64
from pathlib import Path
from datetime import datetime
from PIL import Image
from dotenv import load_dotenv
import io

load_dotenv()

class BusinessCardGenerator:
    """Generate business cards with dual model support"""
    
    # Brand Info
    BRAND = {
        "name": "Alex Shafiro PT / DPT / OCS / CSCS",
        "company": "A Stronger Life",
        "tagline": "Revolutionary Rehabilitation",
        "email": "admin@aslstrong.com",
        "website": "www.aslstrong.com",
        "location": "Stamford, CT"
    }
    
    def __init__(self, model="auto"):
        self.model = model
        self.output_dir = Path("./output")
        self.output_dir.mkdir(exist_ok=True)
        self._init_clients()
    
    def _init_clients(self):
        """Initialize API clients"""
        # OpenAI
        if openai_key := os.getenv('OPENAI_API_KEY'):
            from openai import OpenAI
            self.openai_client = OpenAI(api_key=openai_key)
            print("✅ OpenAI ready")
        else:
            self.openai_client = None
            
        # Google
        if google_key := os.getenv('GOOGLE_API_KEY'):
            from google import genai
            self.google_client = genai.Client(api_key=google_key)
            print("✅ Google ready")
        else:
            self.google_client = None
    
    def generate(self, concept="premium", side="front", model=None):
        """Generate business card"""
        model = model or self._auto_select_model()
        prompt = self._create_prompt(concept, side)
        
        if model == "gpt-image-1":
            return self._generate_openai(prompt)
        elif model == "gemini":
            return self._generate_gemini(prompt)
    
    def _generate_openai(self, prompt):
        """Generate with OpenAI GPT Image 1"""
        if not self.openai_client:
            return None
            
        response = self.openai_client.images.generate(
            model='gpt-image-1',
            prompt=prompt,
            size='1536x1024',
            quality='high',
            n=1
        )
        
        # Save image
        image_b64 = response.data[0].b64_json
        return self._save_image(base64.b64decode(image_b64), "openai")
    
    def _generate_gemini(self, prompt):
        """Generate with Google Gemini"""
        if not self.google_client:
            return None
            
        response = self.google_client.models.generate_content(
            model='gemini-2.5-flash-image-preview',
            contents=[prompt]
        )
        
        # Extract image data
        for part in response.candidates[0].content.parts:
            if hasattr(part, 'inline_data') and part.inline_data:
                return self._save_image(part.inline_data.data, "gemini")
        return None
    
    def _create_prompt(self, concept, side):
        """Universal prompt for both models"""
        base = f"""
        Professional business card design:
        - Flat 2D (NO 3D mockups/shadows)
        - 3.5" × 2.0" proportions
        - Deep black background (#0A0A0A)
        - Emerald accent (#00C9A7)
        
        TEXT:
        {self.BRAND['name']}
        {self.BRAND['company']}
        {self.BRAND['tagline']}
        {self.BRAND['email']}
        {self.BRAND['website']}
        {self.BRAND['location']}
        """
        
        if side == "front":
            base += "\nFRONT: All contact info, logo top-left, QR bottom-right"
        else:
            base += "\nBACK: Centered tagline, minimal design"
            
        concepts = {
            "premium": "Luxury aesthetic",
            "clinical": "Medical authority", 
            "athletic": "Dynamic energy"
        }
        base += f"\nSTYLE: {concepts.get(concept, 'Premium')}"
        
        return base.strip()
    
    def _save_image(self, data, prefix):
        """Save image data to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{prefix}_{timestamp}.png"
        filepath = self.output_dir / filename
        
        with open(filepath, 'wb') as f:
            f.write(data)
        
        print(f"✅ Saved: {filename}")
        return str(filepath)
    
    def _auto_select_model(self):
        """Auto-select best available model"""
        if self.openai_client:
            return "gpt-image-1"
        elif self.google_client:
            return "gemini"
        else:
            raise ValueError("No API clients available")

# Usage
if __name__ == "__main__":
    generator = BusinessCardGenerator()
    
    # Generate with auto-selection
    generator.generate("premium", "front")
    
    # Force specific model
    generator.generate("clinical", "back", model="gemini")
```

---

## API Configuration

### OpenAI GPT Image 1
```python
# From documentation
response = client.images.generate(
    model='gpt-image-1',
    prompt=prompt,
    size='1536x1024',  # Options: 1024x1024, 1024x1536, 1536x1024
    quality='high',     # Options: low, medium, high
    n=1                 # 1-10 images
)
```

### Google Gemini 2.5 Flash Image
```python
# From documentation
response = client.models.generate_content(
    model='gemini-2.5-flash-image-preview',
    contents=[prompt]  # or [image, prompt] for style transfer
)
```

---

## Cost Optimization

| Use Case | Model | Quality | Cost |
|----------|-------|---------|------|
| Drafts | Gemini | Standard | $0.005 |
| Review | GPT Image 1 | Medium | $0.07 |
| Production | GPT Image 1 | High | $0.19 |
| Bulk | Gemini | Standard | $0.005 |

---

## Troubleshooting

### Check API Status
```python
def check_apis():
    status = {
        "OpenAI": bool(os.getenv('OPENAI_API_KEY')),
        "Google": bool(os.getenv('GOOGLE_API_KEY'))
    }
    for api, ready in status.items():
        print(f"{api}: {'✅' if ready else '❌'}")
```

### Common Errors
- **No API key**: Set `OPENAI_API_KEY` or `GOOGLE_API_KEY` in `.env`
- **Import error**: Install with `pip install openai google-genai`
- **Rate limit**: Implement retry with exponential backoff
- **Content policy**: Adjust prompt wording

---

## Best Practices

1. **Always have fallback**: Try primary, then fallback model
2. **Cache results**: Avoid regenerating identical requests
3. **Log performance**: Track which model works best
4. **Batch wisely**: Use Gemini for bulk, GPT-1 for finals

---

## References

- [OpenAI Image Generation](https://platform.openai.com/docs/guides/image-generation)
- [Google Gemini API](https://ai.google.dev/gemini-api/docs/image-generation)
- [Context7 Documentation](https://context7.ai)