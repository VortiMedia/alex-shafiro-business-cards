# Professional Business Card Designer with Google Gemini AI

> Create stunning, brand-consistent business cards using Google's Gemini 2.5 Flash Image API with advanced prompt engineering and iterative design workflows.

## 🚀 Quick Start

```bash
# Clone and setup
git clone <repository-url>
cd business-card-designer-2025

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Run example
python examples/quick_start.py
```

## ✨ Features

### 🎨 Advanced Design Capabilities
- **Brand Consistency Engine**: Maintains exact color codes, typography, and logo placement
- **Multi-variant Generation**: Creates 4+ design variations simultaneously  
- **Iterative Refinement**: Client feedback integration with conversation history
- **Professional Enhancements**: Spot UV effects, embossing simulation, premium finishes

### 🔧 Technical Excellence
- **Print-Ready Output**: 300 DPI, CMYK color space, proper bleeds and crop marks
- **Service Area Validation**: Geographic targeting for local businesses
- **Performance Optimized**: Parallel processing, cost management, caching
- **Quality Assurance**: Automated validation for typography, contrast, dimensions

### 📊 Business Intelligence
- **Conversion Tracking**: GTM integration for design performance metrics
- **A/B Testing Ready**: Built-in variant testing capabilities
- **Cost Management**: API usage optimization and budget controls
- **Analytics Dashboard**: Design performance and client feedback tracking

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- Google Cloud Account with billing enabled
- Google AI Studio API key
- Basic knowledge of design principles

### 1. Google Cloud Setup

```bash
# Install Google Cloud CLI
curl https://sdk.cloud.google.com | bash
exec -l $SHELL

# Initialize and authenticate
gcloud init
gcloud auth application-default login

# Create project
gcloud projects create business-card-designer-2025
gcloud config set project business-card-designer-2025

# Enable required APIs
gcloud services enable generativelanguage.googleapis.com
gcloud services enable aiplatform.googleapis.com
```

### 2. API Key Configuration

1. Visit [Google AI Studio](https://aistudio.google.com)
2. Click "Get API Key" → "Create API key in new project"  
3. Enable billing (required for image generation - $0.039 per image)
4. Copy API key to `.env` file

### 3. Environment Setup

```bash
# Clone repository
git clone <your-repo-url>
cd business-card-designer-2025

# Create virtual environment  
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your credentials
```

## 📁 Project Structure

```
business-card-designer-2025/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── .env.example                # Environment template
├── .gitignore                  # Git ignore rules
├── 
├── src/
│   ├── __init__.py
│   ├── main.py                 # Main application entry
│   ├── processors/
│   │   ├── __init__.py
│   │   ├── card_processor.py   # Business card analysis
│   │   └── image_processor.py  # Image manipulation
│   ├── engines/
│   │   ├── __init__.py
│   │   ├── brand_engine.py     # Brand consistency
│   │   ├── design_engine.py    # Iterative design
│   │   └── export_engine.py    # Production export
│   └── utils/
│       ├── __init__.py
│       ├── validation.py       # Quality checks
│       ├── tracking.py         # Analytics
│       └── helpers.py          # Utility functions
├── 
├── examples/
│   ├── quick_start.py          # Simple usage example
│   ├── advanced_workflow.py    # Full workflow demo  
│   └── batch_processing.py     # Multiple cards
├── 
├── assets/
│   ├── templates/              # Design templates
│   └── brand_assets/           # Sample brand materials
├── 
├── docs/
│   ├── setup/
│   │   ├── google_cloud.md     # GCP setup guide
│   │   └── api_configuration.md # API setup
│   ├── workflows/
│   │   ├── basic_workflow.md   # Simple card creation
│   │   └── advanced_features.md # Pro techniques
│   └── troubleshooting.md      # Common issues
├── 
├── tests/
│   ├── test_processors.py      # Unit tests
│   ├── test_engines.py         # Engine tests
│   └── test_integration.py     # Full workflow tests
└── 
└── scripts/
    ├── setup.py               # Installation helper
    └── validate_setup.py      # Environment validation
```

## 🎯 Usage Examples

### Basic Card Creation

```python
from src.main import ProfessionalCardDesigner

# Initialize designer
designer = ProfessionalCardDesigner()

# Define brand assets
brand_assets = {
    'logo': 'assets/brand_assets/logo.svg',
    'colors': {
        'primary': '#1E3A8A',
        'secondary': '#64748B', 
        'accent': '#F59E0B'
    },
    'fonts': ['Inter', 'Roboto']
}

# Create requirements
requirements = {
    'style': 'Modern minimalist with tech influence',
    'logo_position': 'top-left',
    'include_qr': True,
    'double_sided': False
}

# Generate business card
result = designer.design_card(
    existing_card_path='assets/templates/current_card.png',
    brand_assets=brand_assets,
    requirements=requirements
)

print("✅ Business card design complete!")
print(f"Generated: {result.output_path}")
```

### Advanced Workflow with Feedback

```python
# Initialize with conversation history
designer = ProfessionalCardDesigner(enable_history=True)

# Generate initial variations
designs = designer.generate_variations(
    brand_prompt=base_prompt,
    variations=4
)

# Client selects design #2 and provides feedback
feedback = "Make the logo 20% larger and add more white space around text"

# Refine based on feedback
final_design = designer.refine_design(
    selected_design=designs[1],
    feedback=feedback
)

# Prepare for print production
print_files = designer.prepare_for_print(final_design)
```

### Batch Processing Multiple Cards

```python
# Process team business cards
team_members = [
    {'name': 'John Smith', 'title': 'CEO', 'email': 'john@company.com'},
    {'name': 'Jane Doe', 'title': 'CTO', 'email': 'jane@company.com'},
]

for member in team_members:
    card = designer.create_team_card(
        member_info=member,
        template='executive',
        brand_assets=brand_assets
    )
    print(f"✅ Created card for {member['name']}")
```

## 🔧 Configuration

### Environment Variables

```bash
# Required
GOOGLE_API_KEY=your_api_key_here
GOOGLE_CLOUD_PROJECT=business-card-designer-2025

# Optional  
GOOGLE_CLOUD_LOCATION=us-central1
OUTPUT_DIRECTORY=./output
ENABLE_CACHING=true
MAX_GENERATIONS_PER_DAY=50

# Analytics (Optional)
GTM_CONTAINER_ID=GTM-XXXXXXX
ENABLE_TRACKING=true
```

### API Cost Management

```python
# Built-in cost controls
designer = ProfessionalCardDesigner(
    daily_budget=25.00,          # $25 daily limit
    cost_per_generation=0.039,   # Gemini pricing
    enable_caching=True,         # Cache successful results
    batch_size=4                 # Generate 4 variations per call
)
```

## 🎨 Design Best Practices

### Brand Consistency
- Always use exact hex color codes
- Specify logo dimensions as percentages
- Maintain consistent typography hierarchy
- Include clear space requirements

### Print Specifications
- **Resolution**: 300 DPI minimum
- **Color Mode**: CMYK for print
- **Dimensions**: 3.5" × 2" (standard US)
- **Bleed**: 0.125" on all sides
- **Safe Zone**: 0.25" margin from edges

### Prompt Engineering Tips
```python
# Ultra-specific prompts yield better results
excellent_prompt = """
Create a business card for John Smith, Senior Developer:
- Exact hex colors: #1E3A8A (navy), #F59E0B (amber accent)
- Font: Inter for headers, Roboto for body text
- Logo: Top-left corner, exactly 0.5" width, 0.125" clear space
- Layout: Left-aligned text, asymmetric modern design
- Quality: Print-ready 300 DPI, photorealistic mockup
"""
```

## 📊 Performance & Analytics

### Speed Optimization
- **Parallel Processing**: Generate multiple variants simultaneously
- **Smart Caching**: Reuse successful generations
- **Progressive Enhancement**: Start with low-res previews
- **Batch Operations**: Process multiple cards efficiently

### Cost Management
```python
# Track and control costs
cost_tracker = CostTracker(
    budget_limit=50.00,
    alert_threshold=0.80,
    auto_pause=True
)

# Monitor usage
print(f"Today's usage: ${cost_tracker.daily_spend:.2f}")
print(f"Remaining budget: ${cost_tracker.remaining:.2f}")
```

## 🧪 Testing & Validation

### Run Tests
```bash
# Unit tests
python -m pytest tests/test_processors.py -v

# Integration tests  
python -m pytest tests/test_integration.py -v

# Validate environment
python scripts/validate_setup.py
```

### Quality Checks
- ✅ **Resolution**: 300 DPI verified
- ✅ **Color Accuracy**: Brand colors match exactly  
- ✅ **Typography**: All text legible at print size
- ✅ **Alignment**: Perfect grid alignment
- ✅ **Print Ready**: Bleeds and crop marks included

## 🚀 Deployment Options

### Local Development
```bash
# Start local server
python src/main.py --mode=server --port=8000
```

### Cloud Deployment
```bash
# Deploy to Google Cloud Run
gcloud run deploy business-card-designer \
    --source . \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated
```

### Docker Container
```bash
# Build and run container
docker build -t business-card-designer .
docker run -p 8000:8000 -e GOOGLE_API_KEY=$GOOGLE_API_KEY business-card-designer
```

## 🔍 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| API quota exceeded | Check daily limits in Google Cloud Console |
| Poor image quality | Verify 300 DPI requirement in prompts |
| Brand colors incorrect | Use exact hex codes, mention "color accuracy critical" |
| Logo distorted | Upload logo as separate reference, specify dimensions |
| Slow generation | Enable caching, use batch processing |

### Debug Mode
```bash
# Enable verbose logging
export DEBUG_MODE=true
python examples/quick_start.py
```

### Support Resources
- 📖 [Full Documentation](docs/)
- 🐛 [Issue Tracker](../../issues)
- 💬 [Discussions](../../discussions)
- 📧 [Email Support](mailto:support@yourproject.com)

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup
```bash
# Fork and clone repository
git clone https://github.com/yourusername/business-card-designer-2025.git

# Install development dependencies
pip install -r requirements-dev.txt

# Run pre-commit hooks
pre-commit install

# Run tests before submitting
pytest tests/ -v
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Related Projects

- [Google Generative AI](https://developers.generativeai.google/) - Core API
- [PIL/Pillow](https://pillow.readthedocs.io/) - Image processing
- [OpenCV](https://opencv.org/) - Computer vision utilities

---

**Created with ❤️ for professional business card design**

*Leverage the power of Google's Gemini AI to create stunning business cards that maintain perfect brand consistency while allowing for rapid iteration and client feedback integration.*