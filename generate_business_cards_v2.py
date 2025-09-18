#!/usr/bin/env python3
"""
Alex Shafiro PT - Business Card Generator v2.0
Enhanced Hybrid Workflow with Dual Model Support

Features:
- OpenAI GPT Image 1: Production quality ($0.02-$0.19)
- Google Gemini 2.5 Flash Image: Rapid drafts ($0.005)
- Intelligent model selection based on quality requirements
- Cost optimization and monitoring
- Comprehensive error handling and fallback systems

Usage:
    python generate_business_cards_v2.py
"""

import sys
from pathlib import Path
from typing import Dict, List

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

try:
    from hybrid.modern_workflow import ModernHybridWorkflow, ModelType, GenerationResult
    from dotenv import load_dotenv
except ImportError as e:
    print(f"❌ Missing dependency: {e}")
    print("Setup required:")
    print("1. pip install openai>=1.51.0 google-genai>=1.0.0 python-dotenv Pillow")
    print("2. Create .env file with API keys")
    sys.exit(1)

# Load environment variables
load_dotenv()

class BusinessCardGeneratorV2:
    """Enhanced Business Card Generator with Modern Hybrid Workflow"""
    
    def __init__(self):
        """Initialize v2.0 generator"""
        self.workflow = ModernHybridWorkflow()
        self.session_costs = []
        
    def print_banner(self):
        """Print application banner"""
        print("🏥 Alex Shafiro PT - Business Card Generator v2.0")
        print("=" * 60)
        print("🎨 Dual Model Support: OpenAI GPT Image 1 + Google Gemini")
        print("✨ Intelligent quality-based model selection")
        print("💰 Cost optimization and monitoring")
        print("🔥 Production-ready hybrid workflow")
        print()
        
    def show_brand_info(self):
        """Display brand information"""
        brand = self.workflow.BRAND_INFO
        print("📋 Brand Information:")
        print(f"• Name: {brand['name']}")
        print(f"• Company: {brand['company']}")
        print(f"• Tagline: {brand['tagline']}")
        print(f"• Website: {brand['website']}")
        print(f"• Location: {brand['location']}")
        print()
        
    def show_cost_information(self):
        """Display cost information for informed decision making"""
        print("💰 Cost Information:")
        print("┌─────────────────┬─────────────┬──────────────────┐")
        print("│ Quality Level   │ Model       │ Cost per Card    │")
        print("├─────────────────┼─────────────┼──────────────────┤")
        print("│ Draft           │ Gemini      │ ~$0.005          │")
        print("│ Review          │ GPT Image 1 │ ~$0.070          │")
        print("│ Production      │ GPT Image 1 │ ~$0.190          │")
        print("└─────────────────┴─────────────┴──────────────────┘")
        print()
        print("💡 Tip: Start with 'draft' quality for concept exploration,")
        print("   then use 'production' for final deliverables.")
        print()
        
    def show_generation_options(self):
        """Display generation menu options"""
        print("🎨 Generation Options:")
        print()
        print("📊 Quality Levels:")
        print("1. Draft Quality    - Fast iteration, low cost (Gemini)")
        print("2. Review Quality   - Medium quality, moderate cost (GPT Image 1)")  
        print("3. Production       - Highest quality, premium cost (GPT Image 1)")
        print()
        print("🎯 Concept Options:")
        print("4. All Concepts     - Generate all three design variants")
        print("5. Clinical Precision - Medical authority focus")
        print("6. Athletic Edge    - Dynamic, performance-focused")
        print("7. Luxury Wellness  - Equinox-level sophistication")
        print()
        print("🔧 Advanced Options:")
        print("8. Custom Generation - Specify model, quality, and concept")
        print("9. API Status Check  - Verify API connections")
        print("0. Exit")
        print()
        
    def handle_quality_generation(self, quality: str):
        """Handle quality-based generation (all concepts)"""
        concepts = ["Clinical-Precision", "Athletic-Edge", "Luxury-Wellness"]
        
        print(f"\n🎯 Generating all concepts - {quality} quality")
        
        estimated_cost = self.estimate_total_cost(concepts, quality)
        print(f"💰 Estimated total cost: ${estimated_cost:.3f}")
        
        proceed = input("Continue? (y/n): ").strip().lower()
        if proceed not in ['y', 'yes']:
            print("❌ Generation cancelled")
            return
            
        all_results = {}
        
        for concept in concepts:
            print(f"\n📐 Processing {concept.replace('-', ' ')}...")
            results = self.workflow.generate_full_concept_set(concept, quality)
            
            if results:
                all_results[concept] = results
                # Track costs
                for result in results.values():
                    if result.success:
                        self.session_costs.append(result.cost_estimate)
                        
        self.print_generation_results(all_results)
        
    def handle_single_concept(self, concept: str, quality: str = "production"):
        """Handle single concept generation"""
        concept_name = concept.replace('-', ' ')
        
        print(f"\n🎯 Generating {concept_name} - {quality} quality")
        
        estimated_cost = self.estimate_concept_cost(quality)
        print(f"💰 Estimated cost: ${estimated_cost:.3f}")
        
        proceed = input("Continue? (y/n): ").strip().lower()
        if proceed not in ['y', 'yes']:
            print("❌ Generation cancelled")
            return
            
        results = self.workflow.generate_full_concept_set(concept, quality)
        
        if results:
            # Track costs
            for result in results.values():
                if result.success:
                    self.session_costs.append(result.cost_estimate)
                    
            self.print_generation_results({concept: results})
        else:
            print(f"❌ {concept_name} generation failed")
            
    def handle_custom_generation(self):
        """Handle custom generation with user-specified parameters"""
        print("\n🔧 Custom Generation")
        print()
        
        # Model selection
        print("Available models:")
        print("1. Auto (Recommended)")
        print("2. OpenAI GPT Image 1")
        print("3. Google Gemini 2.5 Flash")
        
        model_choice = input("Select model (1-3): ").strip()
        model_map = {
            "1": ModelType.AUTO,
            "2": ModelType.GPT_IMAGE_1,
            "3": ModelType.GEMINI_FLASH
        }
        selected_model = model_map.get(model_choice, ModelType.AUTO)
        
        # Quality selection
        print("\nQuality levels:")
        print("1. Draft")
        print("2. Review") 
        print("3. Production")
        
        quality_choice = input("Select quality (1-3): ").strip()
        quality_map = {"1": "draft", "2": "review", "3": "production"}
        selected_quality = quality_map.get(quality_choice, "production")
        
        # Concept selection
        print("\nDesign concepts:")
        print("1. Clinical Precision")
        print("2. Athletic Edge")
        print("3. Luxury Wellness")
        
        concept_choice = input("Select concept (1-3): ").strip()
        concept_map = {
            "1": "Clinical-Precision",
            "2": "Athletic-Edge", 
            "3": "Luxury-Wellness"
        }
        selected_concept = concept_map.get(concept_choice, "Clinical-Precision")
        
        # Side selection
        print("\nCard sides:")
        print("1. Both (front and back)")
        print("2. Front only")
        print("3. Back only")
        
        side_choice = input("Select sides (1-3): ").strip()
        
        print(f"\n📋 Configuration:")
        print(f"Model: {selected_model.value}")
        print(f"Quality: {selected_quality}")
        print(f"Concept: {selected_concept.replace('-', ' ')}")
        print(f"Sides: {side_choice}")
        
        estimated_cost = self.estimate_custom_cost(selected_quality, side_choice)
        print(f"💰 Estimated cost: ${estimated_cost:.3f}")
        
        proceed = input("Generate cards? (y/n): ").strip().lower()
        if proceed not in ['y', 'yes']:
            print("❌ Generation cancelled")
            return
            
        # Execute generation
        results = {}
        
        if side_choice in ["1", "2"]:  # Front card
            front_result = self.workflow.generate_card(
                selected_concept, "front", selected_model, selected_quality
            )
            if front_result.success:
                results['front'] = front_result
                self.session_costs.append(front_result.cost_estimate)
                
        if side_choice in ["1", "3"]:  # Back card
            back_result = self.workflow.generate_card(
                selected_concept, "back", selected_model, selected_quality
            )
            if back_result.success:
                results['back'] = back_result
                self.session_costs.append(back_result.cost_estimate)
        
        if results:
            self.print_generation_results({selected_concept: results})
        else:
            print("❌ Custom generation failed")
            
    def estimate_total_cost(self, concepts: List[str], quality: str) -> float:
        """Estimate total cost for multiple concepts"""
        concept_cost = self.estimate_concept_cost(quality)
        return concept_cost * len(concepts)
        
    def estimate_concept_cost(self, quality: str) -> float:
        """Estimate cost for a single concept (front + back)"""
        cost_map = {
            "draft": self.workflow.COSTS["gemini_flash"] * 2,
            "review": self.workflow.COSTS["gpt_image_1_medium"] * 2,
            "production": self.workflow.COSTS["gpt_image_1_high"] * 2
        }
        return cost_map.get(quality, cost_map["production"])
        
    def estimate_custom_cost(self, quality: str, side_choice: str) -> float:
        """Estimate cost for custom generation"""
        base_cost = self.estimate_concept_cost(quality)
        
        if side_choice == "1":  # Both sides
            return base_cost
        else:  # Single side
            return base_cost / 2
            
    def print_generation_results(self, all_results: Dict[str, Dict[str, GenerationResult]]):
        """Print comprehensive generation results"""
        if not all_results:
            print("❌ No cards were generated successfully")
            self.print_troubleshooting()
            return
            
        print(f"\n🎉 Generation Complete!")
        print(f"📁 Output directories:")
        print(f"  • Production: {self.workflow.production_dir.resolve()}")
        print(f"  • Drafts: {self.workflow.drafts_dir.resolve()}")
        print()
        
        # List generated files by concept
        total_images = 0
        total_cost = sum(self.session_costs)
        
        for concept, files in all_results.items():
            concept_name = concept.replace('-', ' ')
            print(f"🎨 {concept_name}:")
            
            for side, result in files.items():
                if result.success:
                    filename = Path(result.filepath).name
                    print(f"  {side.upper()}: {filename}")
                    print(f"    Model: {result.model_used}")
                    print(f"    Cost: ${result.cost_estimate:.3f}")
                    print(f"    Time: {result.processing_time:.1f}s")
                    total_images += 1
            print()
            
        print("📊 Session Summary:")
        print(f"• Generated images: {total_images}")
        print(f"• Total cost: ${total_cost:.3f}")
        print(f"• Average cost per image: ${total_cost/max(total_images, 1):.3f}")
        print()
        
        print("📋 Next Steps:")
        print("1. 🔍 Review generated images for quality and layout")
        print("2. 🖨️ Test print on standard business card stock (3.5\" x 2\")")
        print("3. 🎯 Upload final versions to VistaPrint or local print shop")
        print("4. 📈 Consider A/B testing different concepts")
        
    def print_troubleshooting(self):
        """Print troubleshooting information"""
        print("\n🔍 Troubleshooting:")
        print("1. Check API status with option 9")
        print("2. Verify .env file contains valid API keys:")
        print("   OPENAI_API_KEY=sk-xxxxx")
        print("   GOOGLE_API_KEY=AIzaxxxxx")
        print("3. Check internet connection")
        print("4. Try starting with draft quality first")
        
    def run(self):
        """Main application loop"""
        self.print_banner()
        self.workflow.check_api_status()
        print()
        self.show_brand_info()
        self.show_cost_information()
        
        while True:
            self.show_generation_options()
            choice = input("Select option (0-9): ").strip()
            
            try:
                if choice == "0":
                    print("👋 Thank you for using Business Card Generator v2.0!")
                    break
                    
                elif choice == "1":
                    self.handle_quality_generation("draft")
                    
                elif choice == "2":
                    self.handle_quality_generation("review")
                    
                elif choice == "3":
                    self.handle_quality_generation("production")
                    
                elif choice == "4":
                    # All concepts at production quality
                    self.handle_quality_generation("production")
                    
                elif choice == "5":
                    self.handle_single_concept("Clinical-Precision")
                    
                elif choice == "6":
                    self.handle_single_concept("Athletic-Edge")
                    
                elif choice == "7":
                    self.handle_single_concept("Luxury-Wellness")
                    
                elif choice == "8":
                    self.handle_custom_generation()
                    
                elif choice == "9":
                    self.workflow.check_api_status()
                    
                else:
                    print("❌ Invalid selection. Please choose 0-9.")
                    
            except KeyboardInterrupt:
                print("\n\n⚠️ Operation cancelled by user")
                break
                
            except Exception as e:
                print(f"\n❌ Error: {e}")
                print("Please try again or check your configuration.")
                
            # Pause before showing menu again
            input("\nPress Enter to continue...")
            print("\n" + "="*60 + "\n")

def main():
    """Main entry point"""
    try:
        generator = BusinessCardGeneratorV2()
        generator.run()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        print("Please check your setup and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()