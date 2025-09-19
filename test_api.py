#!/usr/bin/env python3
"""
Quick API connectivity test for Business Card Generator
"""
import sys
import os
sys.path.append('src')

from hybrid.modern_workflow import ModernHybridWorkflow, ModelType

def test_api():
    print("🔍 Testing API connectivity...")
    
    try:
        # Initialize workflow
        workflow = ModernHybridWorkflow()
        print("✅ Workflow initialized")
        
        # Test single card generation with fallback to Gemini
        print("🎨 Testing generation with AUTO model selection...")
        result = workflow.generate_card(
            concept='Clinical-Precision',
            side='front', 
            model=ModelType.AUTO,
            quality='draft'  # Use draft for faster/cheaper testing
        )
        
        print(f"✅ Generation Result: {result.success}")
        if result.success:
            print(f"📁 File: {result.filepath}")
            print(f"🤖 Model: {result.model_used}")
            print(f"💰 Cost: ${result.cost_estimate:.3f}")
            print(f"⏱️  Processing time: {result.processing_time:.2f}s")
        else:
            print(f"❌ Error: {result.error_message}")
            
        return result.success
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_api()
    if success:
        print("\n🎉 MVP is working! Ready for full deployment.")
        exit(0)
    else:
        print("\n⚠️  API issues detected. Check configuration.")
        exit(1)