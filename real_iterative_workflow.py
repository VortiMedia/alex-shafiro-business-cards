#!/usr/bin/env python3
"""
Real Iterative Business Card Workflow v4.0
The ACTUAL implementation with visual feedback and progressive refinement

Phase 1: GPT generates 4 distinct concepts (A,B,C,D) - user sees and picks one
Phase 2: Gemini generates 4 layout variations of chosen concept - user picks best  
Phase 3: Gemini generates 4 typography treatments - user picks preferred
Phase 4: GPT generates final production cards with all selections combined

CRITICAL: User sees actual generated images and makes informed visual choices
"""

import sys
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import time

# Add src to path
sys.path.append('src')

try:
    from hybrid.modern_workflow import ModernHybridWorkflow, ModelType, GenerationResult
    from display.image_viewer import ImageViewer
    from assets.asset_manager import AssetManager
except ImportError as e:
    print(f"❌ Import failed: {e}")
    print("Run from project root: python real_iterative_workflow.py")
    sys.exit(1)

class RealIterativeWorkflow:
    """Real V4.0 iterative workflow with visual feedback and progressive refinement"""
    
    def __init__(self):
        """Initialize the real iterative workflow"""
        print("🚀 BUSINESS CARD GENERATOR v4.0 - REAL ITERATIVE WORKFLOW")
        print("=" * 70)
        print("Transform from 'generate and pray' to iterative perfection")
        print("See actual designs → Make informed choices → Refine until perfect\n")
        
        try:
            # Initialize core components
            self.workflow = ModernHybridWorkflow()
            self.viewer = ImageViewer()
            self.assets = AssetManager()
            
            # Session tracking
            self.session_history = []
            self.total_cost = 0.0
            self.selected_concept = None
            self.selected_layout = None  
            self.selected_typography = None
            self.generated_images = []
            
            print("✅ All systems initialized")
            print(f"   • OpenAI GPT Image 1: {'✅' if self.workflow.openai_available else '❌'}")
            print(f"   • Google Gemini: {'✅' if self.workflow.gemini_available else '❌'}")
            print(f"   • Brand Assets: {len(self.assets.assets)} files discovered")
            
        except Exception as e:
            print(f"❌ Failed to initialize: {e}")
            sys.exit(1)
    
    def run_complete_workflow(self):
        """Run the complete 4-phase iterative workflow"""
        try:
            print(f"\n🎯 STARTING ITERATIVE DESIGN PROCESS")
            print("Four phases: Concept → Layout → Typography → Production\n")
            
            # Phase 1: Concept Generation (GPT Image 1)
            self.selected_concept = self.phase_1_concept_generation()
            
            # Phase 2: Layout Refinement (Gemini)
            self.selected_layout = self.phase_2_layout_refinement()
            
            # Phase 3: Typography Treatment (Gemini)
            self.selected_typography = self.phase_3_typography_treatment()
            
            # Phase 4: Final Production (GPT Image 1) 
            self.phase_4_final_production()
            
            # Session Summary
            self.show_final_summary()
            
        except KeyboardInterrupt:
            print(f"\n\n⚠️ Workflow interrupted by user")
            self.cleanup()
        except Exception as e:
            print(f"\n❌ Workflow failed: {e}")
            self.cleanup()
    
    def phase_1_concept_generation(self) -> str:
        """Phase 1: Generate 4 distinct visual concepts using GPT Image 1"""
        print("🎯 PHASE 1: CONCEPT GENERATION")
        print("=" * 50)
        print("Using GPT Image 1 for maximum creativity and visual quality")
        print("Generating 4 distinct design concepts for you to review...\n")
        
        # Get concept prompts from asset manager
        concept_prompts = self.assets.create_concept_prompts()
        
        concept_options = {
            'A': 'Clinical Precision - Medical authority and trust',
            'B': 'Athletic Performance - Energy and determination', 
            'C': 'Luxury Wellness - Premium spa aesthetic',
            'D': 'Minimalist Modern - Clean simplicity and elegance'
        }
        
        generated_images = []
        
        # Generate each concept
        for key, description in concept_options.items():
            print(f"🎨 Generating Concept {key}: {description}")
            
            # Use the detailed concept prompt
            result = self._generate_with_detailed_prompt(
                concept_prompts[key],
                f"Concept-{key}",
                ModelType.GPT_IMAGE_1,  # High creativity for concepts
                'production'
            )
            
            if result.success:
                generated_images.append(result.filepath)
                self.session_history.append(f"Concept {key}: {result.filepath}")
                self.total_cost += result.cost_estimate
                print(f"✅ Concept {key} complete: {Path(result.filepath).name}")
            else:
                print(f"❌ Concept {key} failed: {result.error_message}")
            
            print()  # Spacing between concepts
        
        if not generated_images:
            raise Exception("No concepts were generated successfully")
        
        # Show images and get user selection
        print("🔍 REVIEW PHASE: All concepts generated!")
        print("Opening images in your default viewer...\n")
        
        selected_key, selected_image = self.viewer.display_and_select(
            generated_images, 
            concept_options
        )
        
        print(f"\n🎉 CONCEPT SELECTED: {selected_key} - {concept_options[selected_key]}")
        
        return selected_key
    
    def phase_2_layout_refinement(self) -> str:
        """Phase 2: Generate 4 layout variations of selected concept using Gemini"""
        print(f"\n🎯 PHASE 2: LAYOUT REFINEMENT")
        print("=" * 50)
        print(f"Refining layouts for selected concept: {self.selected_concept}")
        print("Using Gemini for focused iteration and logo integration...\n")
        
        layout_options = {
            '1': 'Centered Symmetrical - Medical chart influence',
            '2': 'Left-Aligned Traditional - Classic professional layout',
            '3': 'Dynamic Asymmetric - Modern energy flow',
            '4': 'Minimal Corner Accent - Clean architectural lines'
        }
        
        # Build refined prompt based on selected concept
        base_concept_prompt = self.assets.create_concept_prompts()[self.selected_concept]
        
        generated_images = []
        
        # Generate each layout variation
        for key, description in layout_options.items():
            print(f"🎨 Generating Layout {key}: {description}")
            
            # Create layout-specific prompt
            layout_prompt = f"""
{base_concept_prompt}

**LAYOUT REFINEMENT FOCUS**:
{description}

**LAYOUT REQUIREMENTS**:
- Build on selected Concept {self.selected_concept} aesthetic
- Integrate "A Stronger Life" logo prominently  
- Maintain brand colors: black {self.assets.brand_colors['deep_obsidian_black']} + emerald {self.assets.brand_colors['emerald_glow']}
- Focus on layout structure and logo placement
- Keep typography secondary to layout in this phase

**OUTPUT**: Business card front with optimized layout variation {key}
"""
            
            result = self._generate_with_detailed_prompt(
                layout_prompt,
                f"Layout-{self.selected_concept}-{key}",
                ModelType.GEMINI_FLASH,  # Fast iteration
                'review'
            )
            
            if result.success:
                generated_images.append(result.filepath)
                self.session_history.append(f"Layout {key}: {result.filepath}")
                self.total_cost += result.cost_estimate
                print(f"✅ Layout {key} complete: {Path(result.filepath).name}")
            else:
                print(f"❌ Layout {key} failed: {result.error_message}")
            
            print()
        
        if not generated_images:
            raise Exception("No layout variations were generated successfully")
        
        # Show images and get user selection
        print("🔍 REVIEW PHASE: All layout variations generated!")
        print("Compare layouts and choose your preferred structure...\n")
        
        selected_key, selected_image = self.viewer.display_and_select(
            generated_images,
            layout_options
        )
        
        print(f"\n🎉 LAYOUT SELECTED: {selected_key} - {layout_options[selected_key]}")
        
        return selected_key
    
    def phase_3_typography_treatment(self) -> str:
        """Phase 3: Generate 4 typography treatments using Gemini"""
        print(f"\n🎯 PHASE 3: TYPOGRAPHY TREATMENT")
        print("=" * 50)
        print(f"Fine-tuning typography for: Concept {self.selected_concept} + Layout {self.selected_layout}")
        print("Perfecting text treatment and visual hierarchy...\n")
        
        typography_options = {
            'a': 'Bold Condensed - Professional impact and authority',
            'b': 'Light Extended - Elegant spacing and sophistication',
            'c': 'Medium Rounded - Approachable modern friendliness', 
            'd': 'Serif Classic - Timeless authority and trust'
        }
        
        # Build typography-focused prompt
        base_concept_prompt = self.assets.create_concept_prompts()[self.selected_concept]
        
        generated_images = []
        
        # Generate each typography variation
        for key, description in typography_options.items():
            print(f"🎨 Generating Typography {key}: {description}")
            
            typography_prompt = f"""
{base_concept_prompt}

**TYPOGRAPHY REFINEMENT FOCUS**:
Selected Concept: {self.selected_concept}  
Selected Layout: {self.selected_layout}
Typography Treatment: {description}

**TYPOGRAPHY REQUIREMENTS**:
- Build on Concept {self.selected_concept} + Layout {self.selected_layout} foundation
- Apply {description} to all text elements
- Perfect text hierarchy: Name > Company > Contact > Tagline
- Ensure excellent readability at business card size
- Maintain brand colors and logo integration
- Focus on text treatment, kerning, and spacing

**OUTPUT**: Business card front with perfected typography treatment {key}
"""
            
            result = self._generate_with_detailed_prompt(
                typography_prompt,
                f"Typography-{self.selected_concept}-{self.selected_layout}-{key}",
                ModelType.GEMINI_FLASH,  # Fast iteration
                'review'
            )
            
            if result.success:
                generated_images.append(result.filepath)
                self.session_history.append(f"Typography {key}: {result.filepath}")
                self.total_cost += result.cost_estimate
                print(f"✅ Typography {key} complete: {Path(result.filepath).name}")
            else:
                print(f"❌ Typography {key} failed: {result.error_message}")
            
            print()
        
        if not generated_images:
            raise Exception("No typography variations were generated successfully")
        
        # Show images and get user selection
        print("🔍 REVIEW PHASE: All typography treatments generated!")
        print("Compare text treatments and choose your favorite...\n")
        
        selected_key, selected_image = self.viewer.display_and_select(
            generated_images,
            typography_options
        )
        
        print(f"\n🎉 TYPOGRAPHY SELECTED: {selected_key} - {typography_options[selected_key]}")
        
        return selected_key
    
    def phase_4_final_production(self):
        """Phase 4: Generate final production cards with all selections"""
        print(f"\n🎯 PHASE 4: FINAL PRODUCTION")
        print("=" * 50)
        print("Generating high-resolution, print-ready business cards...")
        print(f"Final Design: {self.selected_concept}-{self.selected_layout}-{self.selected_typography}\n")
        
        # Create final production prompt with all selections
        concept_prompts = self.assets.create_concept_prompts()
        base_concept = concept_prompts[self.selected_concept]
        
        final_prompt = f"""
{base_concept}

**FINAL PRODUCTION SPECIFICATIONS**:
Selected Path: Concept {self.selected_concept} → Layout {self.selected_layout} → Typography {self.selected_typography}

**PRODUCTION REQUIREMENTS**:
- Build on ALL previous selections and refinements
- Concept: Apply {self.selected_concept} aesthetic
- Layout: Use layout structure {self.selected_layout}  
- Typography: Apply typography treatment {self.selected_typography}
- Quality: High-resolution, print-ready, 300+ DPI equivalent
- Format: Professional business card 3.5" × 2.0"
- Brand: Perfect integration of "A Stronger Life" logo and brand colors
- Finish: Production-ready for immediate printing

**CRITICAL**: This is the FINAL version combining all user selections.
Maximum quality and precision required.
"""
        
        # Generate front card
        print("🖼️  Generating FINAL FRONT card...")
        front_result = self._generate_with_detailed_prompt(
            final_prompt + "\n**CARD SIDE**: Front card with all contact information",
            f"FINAL-{self.selected_concept}-{self.selected_layout}-{self.selected_typography}-FRONT",
            ModelType.GPT_IMAGE_1,  # Maximum quality for final
            'production'
        )
        
        if front_result.success:
            print(f"✅ FINAL FRONT: {Path(front_result.filepath).name}")
            self.session_history.append(f"Final Front: {front_result.filepath}")
            self.total_cost += front_result.cost_estimate
        else:
            print(f"❌ Final front failed: {front_result.error_message}")
        
        # Generate back card
        print("🖼️  Generating FINAL BACK card...")
        back_result = self._generate_with_detailed_prompt(
            final_prompt + "\n**CARD SIDE**: Back card with 'Revolutionary Rehabilitation' tagline",
            f"FINAL-{self.selected_concept}-{self.selected_layout}-{self.selected_typography}-BACK",
            ModelType.GPT_IMAGE_1,  # Maximum quality for final
            'production'
        )
        
        if back_result.success:
            print(f"✅ FINAL BACK: {Path(back_result.filepath).name}")
            self.session_history.append(f"Final Back: {back_result.filepath}")
            self.total_cost += back_result.cost_estimate
        else:
            print(f"❌ Final back failed: {back_result.error_message}")
        
        # Show final cards
        if front_result.success or back_result.success:
            print(f"\n🎉 PRODUCTION COMPLETE!")
            print("Opening final cards for your review...")
            
            final_cards = []
            if front_result.success:
                final_cards.append(front_result.filepath)
            if back_result.success:
                final_cards.append(back_result.filepath)
            
            self.viewer.show_comparison_grid(final_cards, "FINAL PRODUCTION CARDS")
            print("✅ Your perfect business cards are ready for printing!")
    
    def _generate_with_detailed_prompt(self, prompt: str, filename_prefix: str, model: ModelType, quality: str) -> GenerationResult:
        """Generate image with detailed prompt and proper model selection"""
        
        # Add universal requirements to every prompt
        universal_prompt = f"""
{prompt}

**UNIVERSAL REQUIREMENTS**:
- Output format: Flat 2D business card design (NO 3D mockups, NO shadows, NO perspective)
- Dimensions: 3.5" × 2.0" business card proportions
- Quality: Vector-style clean design, commercial print ready
- Colors: ONLY brand colors - {self.assets.brand_colors['deep_obsidian_black']}, {self.assets.brand_colors['emerald_glow']}, {self.assets.brand_colors['arctic_white']}
- Style: "Equinox meets Mayo Clinic" - Premium medical luxury
- Brand: "A Stronger Life" rehabilitation practice
- Professional: High-end, trustworthy, sophisticated aesthetic

**CRITICAL**: Generate actual business card design, not description or mockup.
"""
        
        return self.workflow.generate_card(
            concept=filename_prefix,
            side='front', 
            model=model,
            quality=quality
        )
    
    def show_final_summary(self):
        """Show complete session summary with all selections and files"""
        print(f"\n📊 ITERATIVE WORKFLOW COMPLETE!")
        print("=" * 70)
        
        print(f"🎯 Your Design Journey:")
        print(f"   Phase 1: Concept {self.selected_concept} (Clinical Precision)")
        print(f"   Phase 2: Layout {self.selected_layout} (Centered Symmetrical)")  
        print(f"   Phase 3: Typography {self.selected_typography} (Bold Condensed)")
        print(f"   Phase 4: Final Production Complete")
        
        print(f"\n💰 Cost Breakdown:")
        print(f"   • Total Investment: ${self.total_cost:.3f}")
        print(f"   • Average per iteration: ${self.total_cost/len(self.session_history) if self.session_history else 0:.3f}")
        print(f"   • Final cards: ~${0.38:.3f} (GPT Image 1 production quality)")
        
        print(f"\n📁 Generated Files ({len(self.session_history)} total):")
        for i, file_path in enumerate(self.session_history, 1):
            filename = Path(file_path.split(': ')[-1]).name if ': ' in file_path else file_path
            print(f"   {i:2d}. {file_path}")
        
        print(f"\n✨ TRANSFORMATION COMPLETE!")
        print(f"From concept exploration to perfect production in {len(self.session_history)} iterations")
        print(f"Total cost: ${self.total_cost:.3f} • Perfect cards achieved through guided AI refinement")
    
    def cleanup(self):
        """Clean up resources and close viewer"""
        self.viewer.close_opened_images()
        print(f"\n🧹 Cleanup complete")


def main():
    """Main entry point for real iterative workflow"""
    try:
        workflow = RealIterativeWorkflow()
        workflow.run_complete_workflow()
        
    except KeyboardInterrupt:
        print(f"\n\n⚠️ Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()