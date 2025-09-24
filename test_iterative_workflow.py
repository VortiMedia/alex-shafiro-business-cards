#!/usr/bin/env python3
"""
Business Card Generator - Iterative Workflow Test
Simulates the V4.0 4-phase iterative design process using current V3.0 components

Phase 1: Concept Selection (A, B, C, D)
Phase 2: Layout Refinement (1, 2, 3, 4)  
Phase 3: Typography Treatment (a, b, c, d)
Phase 4: Final Production (high-res generation)
"""

import sys
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List

# Add src to path
sys.path.append('src')

try:
    from hybrid.modern_workflow import ModernHybridWorkflow, ModelType, GenerationResult
except ImportError as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)

class IterativeWorkflowTest:
    """Simulates the V4.0 iterative workflow using V3.0 components"""
    
    def __init__(self):
        """Initialize the workflow engine"""
        print("🚀 Business Card Generator - Iterative Workflow Test")
        print("=" * 60)
        
        try:
            self.workflow = ModernHybridWorkflow()
            self.session_history = []
            self.total_cost = 0.0
            
            print("✅ Dual AI models ready")
            print(f"   • OpenAI GPT Image 1: {'✅' if self.workflow.openai_available else '❌'}")
            print(f"   • Google Gemini: {'✅' if self.workflow.gemini_available else '❌'}")
            
        except Exception as e:
            print(f"❌ Failed to initialize: {e}")
            sys.exit(1)
    
    def run_interactive_session(self):
        """Run the complete 4-phase iterative workflow"""
        print("\n🎨 ITERATIVE DESIGN WORKFLOW")
        print("Transform from 'generate and pray' to iterative perfection")
        print("Users guide AI through refinement rounds until perfect\n")
        
        # Phase 1: Concept Selection
        concept_choice = self.phase_1_concepts()
        
        # Phase 2: Layout Refinement  
        layout_choice = self.phase_2_layouts(concept_choice)
        
        # Phase 3: Typography Treatment
        typography_choice = self.phase_3_typography(concept_choice, layout_choice)
        
        # Phase 4: Final Production
        self.phase_4_production(concept_choice, layout_choice, typography_choice)
        
        # Session Summary
        self.show_session_summary()
    
    def phase_1_concepts(self) -> str:
        """Phase 1: Generate and select initial concept variations"""
        print("🎯 PHASE 1: CONCEPT SELECTION")
        print("=" * 40)
        print("Choose your design foundation from 4 concept variations:\n")
        
        concepts = {
            'A': ('Clinical-Precision', 'Medical authority and professional trust'),
            'B': ('Athletic-Edge', 'Performance, energy, and determination'),  
            'C': ('Luxury-Wellness', 'Premium spa aesthetic and exclusivity'),
            'D': ('Minimalist-Modern', 'Clean simplicity with subtle elegance')
        }
        
        print("CONCEPT OPTIONS:")
        for key, (name, desc) in concepts.items():
            print(f"  {key}. {name}")
            print(f"     → {desc}")
        
        # Generate sample for demonstration (using draft quality)
        print(f"\n🎨 Generating concept previews...")
        sample_concept = concepts['A'][0]  # Clinical-Precision as example
        
        result = self.workflow.generate_card(
            concept=sample_concept,
            side='front',
            model=ModelType.GEMINI_FLASH,  # Fast/cheap for iteration
            quality='draft'
        )
        
        if result.success:
            self.session_history.append(f"Phase 1 Preview: {result.filepath}")
            self.total_cost += result.cost_estimate
            print(f"✅ Sample generated: {Path(result.filepath).name}")
        else:
            print(f"❌ Generation failed: {result.error_message}")
        
        # User selection
        while True:
            choice = input("\nSelect your preferred concept (A/B/C/D): ").upper().strip()
            if choice in concepts:
                selected = concepts[choice]
                print(f"\n✅ Selected: {choice} - {selected[0]}")
                print(f"   {selected[1]}")
                return selected[0]
            print("Please enter A, B, C, or D")
    
    def phase_2_layouts(self, concept: str) -> str:
        """Phase 2: Refine layout variations of chosen concept"""
        print(f"\n🎯 PHASE 2: LAYOUT REFINEMENT")
        print("=" * 40)
        print(f"Refining layout options for: {concept}\n")
        
        layouts = {
            '1': 'Centered-Symmetrical',
            '2': 'Left-Aligned-Traditional', 
            '3': 'Dynamic-Asymmetric',
            '4': 'Minimal-Corner-Accent'
        }
        
        print("LAYOUT OPTIONS:")
        for key, layout in layouts.items():
            print(f"  {key}. {layout}")
        
        print(f"\n🎨 Generating layout variations...")
        
        # Generate one layout example
        result = self.workflow.generate_card(
            concept=concept,
            side='front',
            model=ModelType.GEMINI_FLASH,
            quality='draft'
        )
        
        if result.success:
            self.session_history.append(f"Phase 2 Layout: {result.filepath}")
            self.total_cost += result.cost_estimate
            print(f"✅ Layout sample: {Path(result.filepath).name}")
        
        # User selection
        while True:
            choice = input("\nSelect your preferred layout (1/2/3/4): ").strip()
            if choice in layouts:
                print(f"✅ Selected: {choice} - {layouts[choice]}")
                return layouts[choice]
            print("Please enter 1, 2, 3, or 4")
    
    def phase_3_typography(self, concept: str, layout: str) -> str:
        """Phase 3: Typography and text treatment variations"""
        print(f"\n🎯 PHASE 3: TYPOGRAPHY TREATMENT") 
        print("=" * 40)
        print(f"Fine-tuning typography for: {concept} + {layout}\n")
        
        typography = {
            'a': 'Bold-Condensed (Professional Impact)',
            'b': 'Light-Extended (Elegant Spacing)',
            'c': 'Medium-Rounded (Approachable Modern)', 
            'd': 'Serif-Classic (Timeless Authority)'
        }
        
        print("TYPOGRAPHY OPTIONS:")
        for key, typo in typography.items():
            print(f"  {key}. {typo}")
        
        print(f"\n🎨 Generating typography treatments...")
        
        # Generate typography example
        result = self.workflow.generate_card(
            concept=concept,
            side='front', 
            model=ModelType.GEMINI_FLASH,
            quality='review'  # Slightly higher quality for typography
        )
        
        if result.success:
            self.session_history.append(f"Phase 3 Typography: {result.filepath}")
            self.total_cost += result.cost_estimate
            print(f"✅ Typography sample: {Path(result.filepath).name}")
        
        # User selection
        while True:
            choice = input("\nSelect your preferred typography (a/b/c/d): ").lower().strip()
            if choice in typography:
                print(f"✅ Selected: {choice} - {typography[choice]}")
                return typography[choice]
            print("Please enter a, b, c, or d")
    
    def phase_4_production(self, concept: str, layout: str, typography: str):
        """Phase 4: Generate final production-ready cards"""
        print(f"\n🎯 PHASE 4: FINAL PRODUCTION")
        print("=" * 40)
        print("Generating high-resolution production files...\n")
        
        design_code = f"{concept}_{layout}_{typography}"
        
        print(f"🎨 Final Design Specification:")
        print(f"   • Concept: {concept}")
        print(f"   • Layout: {layout}")
        print(f"   • Typography: {typography}")
        print(f"   • Design Code: {design_code}")
        
        # Generate final front card (production quality)
        print(f"\n🖼️  Generating FRONT card...")
        front_result = self.workflow.generate_card(
            concept=concept,
            side='front',
            model=ModelType.GPT_IMAGE_1,  # High quality for final
            quality='production'
        )
        
        if front_result.success:
            print(f"✅ FRONT: {Path(front_result.filepath).name}")
            self.session_history.append(f"Final Front: {front_result.filepath}")
            self.total_cost += front_result.cost_estimate
        else:
            print(f"❌ Front generation failed: {front_result.error_message}")
        
        # Generate final back card
        print(f"🖼️  Generating BACK card...")
        back_result = self.workflow.generate_card(
            concept=concept,
            side='back', 
            model=ModelType.GPT_IMAGE_1,
            quality='production'
        )
        
        if back_result.success:
            print(f"✅ BACK: {Path(back_result.filepath).name}")
            self.session_history.append(f"Final Back: {back_result.filepath}")
            self.total_cost += back_result.cost_estimate
        else:
            print(f"❌ Back generation failed: {back_result.error_message}")
        
        print(f"\n🎉 PRODUCTION COMPLETE!")
        print(f"Your perfect business cards are ready for printing!")
    
    def show_session_summary(self):
        """Display complete session results"""
        print(f"\n📊 SESSION SUMMARY")
        print("=" * 60)
        
        print(f"🎯 Design Journey:")
        for i, step in enumerate(self.session_history, 1):
            print(f"   {i}. {step}")
        
        print(f"\n💰 Cost Breakdown:")
        print(f"   • Total Cost: ${self.total_cost:.3f}")
        print(f"   • Average per iteration: ${self.total_cost/len(self.session_history) if self.session_history else 0:.3f}")
        
        print(f"\n📁 Generated Files:")
        output_dir = Path("./output")
        if output_dir.exists():
            png_files = list(output_dir.rglob("*.png"))
            recent_files = sorted(png_files, key=lambda x: x.stat().st_mtime, reverse=True)[:5]
            
            for file in recent_files:
                size_mb = file.stat().st_size / (1024 * 1024)
                mod_time = datetime.fromtimestamp(file.stat().st_mtime)
                print(f"   📄 {file.name} ({size_mb:.1f}MB) - {mod_time.strftime('%H:%M:%S')}")
        
        print(f"\n✨ ITERATIVE WORKFLOW COMPLETE!")
        print(f"From concept to production in ~$0.25 with guided AI refinement")


def main():
    """Main entry point"""
    try:
        workflow_test = IterativeWorkflowTest()
        workflow_test.run_interactive_session()
        
    except KeyboardInterrupt:
        print(f"\n\n⚠️ Workflow interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Workflow failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()