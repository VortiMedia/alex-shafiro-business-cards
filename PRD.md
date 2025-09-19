Alex Shafiro PT Business Card System
Product Requirements Document & Development PlanExecutive SummaryThis PRD outlines a multi-stage, iterative workflow for generating expert-level business cards using OpenAI's GPT Image 1 API. The system employs progressive refinement with decreasing creative freedom at each stage to achieve precise, print-ready designs with superior text rendering.Core Problem AnalysisCurrent Issues Identified:

Mockup Presentation: Getting 3D cards on backgrounds instead of flat artboards
Shadow/Depth Effects: Despite requesting flat designs, receiving dimensional presentations
Asset Integration: Logos not being properly integrated into designs
Information Accuracy: Generated cards showing placeholder instead of actual contact info
Quality Control: Inconsistent adherence to print specifications
Solution Strategy:
Implement a 3-Stage Progressive Refinement System with decreasing temperature control and increasing precision at each stage.System ArchitectureStage 1: Concept Foundation (Temperature: 0.8-0.9)
Purpose: Generate abstract backgrounds and layout structures
Output: 3 variations per design concept
Freedom Level: High creative explorationStage 2: Asset Integration (Temperature: 0.5-0.6)
Purpose: Add logos and brand elements to selected concepts
Output: 3 refinements per selected concept
Freedom Level: Moderate, brand-focusedStage 3: Text Finalization (Temperature: 0.2-0.3)
Purpose: Precise text placement and typography
Output: 3 final options per design
Freedom Level: Low, precision-focusedDesign SpecificationsVariation A: Centered Symmetry
yamlfront:
  layout: "center-aligned vertical stack"
  hierarchy:
    1: "Logo icon (0.75" height) with subtle emerald glow"
    2: "Company name below logo, tight kerning"
    3: "Contact strip (phone • email • website) horizontal"
    4: "QR code bottom-right with white outline"
  background: "Matte black with vignette edges"
  
back:
  layout: "centered statement"
  primary_text: "REVOLUTIONARY REHABILITATION"
  effect: "Embossed logo watermark at 5% opacity"
  typography: "Bold uppercase, spaced lettering, glowing edge"Variation B: Dynamic Flow
yamlfront:
  layout: "asymmetric with vertical accent"
  left_column: "Dark charcoal vertical strip (20% width)"
  icons: "Stacked vertically in left column"
  logo: "Large centered with emerald glow"
  accent_line: "Thin glowing green line bottom edge"
  
back:
  layout: "minimalist corner accent"
  logo_ghost: "Bottom-right embossed at 10% opacity"
  text: "Clean white, no effects, pure contrast"Variation C: Classic Professional
yamlfront:
  layout: "traditional left-aligned"
  left_side: "Icon column with aligned text"
  center: "Prominent logo with 'Stronger Life' tagline"
  qr_placement: "Bottom-right corner"
  
back:
  layout: "bold centered statement"
  background: "Pure matte black"
  text: "REVOLUTIONARY REHABILITATION centered"Technical Implementation Plan1. Prompt Engineering Frameworkpythonclass PromptEngine:
    """Advanced prompt construction for flat artboard generation"""
    
    NEGATIVE_PROMPTS = [
        "NO 3D mockups",
        "NO shadows or depth",
        "NO perspective views",
        "NO card on table",
        "NO environmental context",
        "NO rounded corners showing thickness",
        "FLAT vector artboard ONLY"
    ]
    
    QUALITY_MODIFIERS = [
        "flat vector design",
        "adobe illustrator artboard",
        "print-ready artwork",
        "2D graphic design",
        "professional vector graphics",
        "commercial print file"
    ]
    
    def construct_stage_prompt(self, stage, variation, previous_result=None):
        """Build stage-specific prompts with proper constraints"""
        pass2. Temperature Control SystempythonSTAGE_CONFIGS = {
    "concept": {
        "temperature": 0.85,
        "top_k": 50,
        "top_p": 0.95,
        "focus": "creative exploration"
    },
    "asset": {
        "temperature": 0.55,
        "top_k": 30,
        "top_p": 0.90,
        "focus": "brand consistency"
    },
    "text": {
        "temperature": 0.25,
        "top_k": 20,
        "top_p": 0.85,
        "focus": "precise execution"
    }
}3. Selection Mechanismpythonclass SelectionInterface:
    """User selection system for iterative refinement"""
    
    def display_grid(self, images, stage_name):
        """Show 3x3 grid of variations"""
        # Display images in organized grid
        # Label as A1, A2, A3, B1, B2, B3, etc.
        pass
    
    def capture_selections(self):
        """Record user's chosen variations"""
        # Return list of selected indices
        pass
    
    def merge_preferences(self, selections):
        """Combine selected elements for next stage"""
        # Create composite prompt from selections
        pass4. Asset Management Strategypythonclass AssetManager:
    """Handle logo and brand asset integration"""
    
    def prepare_logo(self, logo_path):
        """Process logo for optimal integration"""
        # Steps:
        # 1. Convert to high-contrast version
        # 2. Create multiple size variants
        # 3. Generate placement masks
        # 4. Encode as base64 with metadata
        pass
    
    def create_composite_prompt(self, base_design, logo_data):
        """Merge logo into selected design"""
        # Use inpainting-style prompts
        # Specify exact placement coordinates
        passWorkflow ImplementationPhase 1: Initial Setup
pythondef initialize_project():
    """Setup project with brand assets"""
    # 1. Load brand colors, fonts, logos
    # 2. Validate asset quality
    # 3. Create project directory structure
    # 4. Initialize API connectionsPhase 2: Concept Generation
pythondef generate_concepts():
    """Stage 1: Create base concepts"""
    for variation in ["centered", "dynamic", "classic"]:
        for i in range(3):
            prompt = create_concept_prompt(variation, i)
            image = generate_with_gpt_image_1(prompt, quality='high')
            save_to_grid(image, f"{variation}_{i}")
pythondef refine_selected(selections):
    """Stage 2 & 3: Add assets and text"""
    for selected in selections:
        # Stage 2: Add logo
        logo_variants = integrate_logo(selected, temp=0.55)
        
        # User selects best logo integration
        logo_choice = user_select(logo_variants)
        
        # Stage 3: Finalize text
        text_variants = add_precise_text(logo_choice, temp=0.25)
        
        # Final selection
        final = user_select(text_variants)Quality Validation MetricsAutomated Checks

Dimensions: Verify 3.5" x 2.0" at 300 DPI
Color Space: Ensure CMYK compatibility
Contrast Ratio: WCAG AAA compliance (7:1 minimum)
Bleed Area: 0.125" on all sides
Safe Zone: 0.25" margins maintained
Manual Review Checklist

 No 3D effects or shadows present
 Text is crisp and legible at print size
 Logo appears properly integrated
 Brand colors are accurate
 Overall design feels premium
Advanced Prompt TemplatesForce Flat Artboard Output
pythonFLAT_ARTBOARD_PROMPT = """
Create a FLAT 2D business card design as a vector graphic artboard.
This is a TECHNICAL ILLUSTRATION, not a photograph.
Generate as if creating in Adobe Illustrator - pure flat artwork.

CRITICAL REQUIREMENTS:
- Output must be a flat 2D design file
- NO 3D rendering, NO mockups, NO perspective
- NO shadows, NO depth, NO environmental context
- Treat as vector artwork on digital canvas
- Pure geometric shapes and text only
- Export-ready for print production

THINK: Technical drawing, NOT product photography
THINK: Illustrator artboard, NOT mockup presentation
THINK: Print file, NOT marketing image
"""Progressive Enhancement PromptsStage 1 - Concept:
"Abstract geometric composition in black with single emerald accent.
Focus on negative space and visual rhythm. No text or logos yet."Stage 2 - Assets:
"Previous design + integrate provided logo at coordinates (0.5", 0.5").
Maintain all existing geometry. Logo should feel native to design."Stage 3 - Text:
"Previous design + add text exactly as specified:
'Alex Shafiro PT / DPT / OCS / CSCS' at (1.75", 1.0") in Helvetica Neue Bold 11pt.
Ensure perfect kerning and baseline alignment."Error Handling & Recoverypythonclass QualityControl:
    def detect_mockup(self, image):
        """Detect if output is mockup vs flat design"""
        # Check for perspective distortion
        # Analyze shadow presence
        # Verify edge characteristics
        
    def auto_correct(self, image):
        """Attempt automatic correction"""
        # If mockup detected:
        # 1. Re-prompt with stronger constraints
        # 2. Apply perspective correction
        # 3. Remove shadow layersSuccess Metrics
Flat Design Achievement: >95% of outputs are true flat artboards
Brand Consistency: Logo and colors match exactly across variations
Print Readiness: 100% pass VistaPrint upload requirements
Generation Efficiency: <5 iterations to final design
User Satisfaction: Design selected without post-processing needs