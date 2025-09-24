#!/usr/bin/env python3
"""
Image Display System for Iterative Workflow
Shows generated business cards to user for selection
"""

import subprocess
import sys
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import time

class ImageViewer:
    """Handle image display and user selection for iterative workflow"""
    
    def __init__(self):
        self.opened_images = []
        
    def display_images(self, image_paths: List[str], labels: Dict[str, str]) -> None:
        """
        Display images using system default viewer (Preview on macOS)
        
        Args:
            image_paths: List of file paths to display
            labels: Dict mapping option keys to descriptions
        """
        print(f"\n📸 Opening {len(image_paths)} images for your review...")
        
        for i, path in enumerate(image_paths):
            if Path(path).exists():
                try:
                    # Open image in default viewer
                    if sys.platform == "darwin":  # macOS
                        subprocess.run(['open', path], check=True)
                    elif sys.platform == "linux":
                        subprocess.run(['xdg-open', path], check=True)
                    elif sys.platform == "win32":
                        subprocess.run(['start', path], shell=True, check=True)
                    
                    self.opened_images.append(path)
                    time.sleep(0.5)  # Small delay between opens
                    
                except subprocess.CalledProcessError:
                    print(f"⚠️ Could not open {path}")
            else:
                print(f"❌ File not found: {path}")
        
        print(f"✅ Images opened in your default viewer")
        
    def show_options_and_get_choice(self, options: Dict[str, str]) -> str:
        """
        Display options and get user selection
        
        Args:
            options: Dict mapping option keys to descriptions
            
        Returns:
            Selected option key
        """
        print(f"\n🎨 SELECT YOUR PREFERRED OPTION:")
        print("=" * 40)
        
        for key, desc in options.items():
            print(f"  {key}. {desc}")
        
        valid_choices = list(options.keys())
        
        while True:
            choice = input(f"\nEnter your choice ({'/'.join(valid_choices)}): ").strip()
            
            if choice.upper() in [k.upper() for k in valid_choices]:
                # Find the matching key (case-insensitive)
                selected = next(k for k in valid_choices if k.upper() == choice.upper())
                print(f"\n✅ Selected: {selected} - {options[selected]}")
                return selected
                
            print(f"Please enter one of: {', '.join(valid_choices)}")
    
    def display_and_select(self, image_paths: List[str], options: Dict[str, str]) -> Tuple[str, str]:
        """
        Display images and get user selection in one step
        
        Args:
            image_paths: List of file paths to display
            options: Dict mapping option keys to descriptions
            
        Returns:
            Tuple of (selected_key, selected_image_path)
        """
        # Ensure we have matching images and options
        if len(image_paths) != len(options):
            print(f"⚠️ Warning: {len(image_paths)} images but {len(options)} options")
        
        self.display_images(image_paths, options)
        selected_key = self.show_options_and_get_choice(options)
        
        # Find corresponding image path
        option_keys = list(options.keys())
        if selected_key in option_keys:
            selected_index = option_keys.index(selected_key)
            if selected_index < len(image_paths):
                selected_path = image_paths[selected_index]
                return selected_key, selected_path
        
        # Fallback - return first image
        return selected_key, image_paths[0] if image_paths else ""
    
    def close_opened_images(self):
        """Close any images that were opened (if possible)"""
        # On macOS, we can't easily close specific Preview windows
        # But we can inform the user
        if self.opened_images:
            print(f"\n💡 Tip: You can close the Preview windows manually")
            print(f"   ({len(self.opened_images)} images were opened)")
        self.opened_images.clear()
    
    def show_comparison_grid(self, image_paths: List[str], title: str = "Compare Options"):
        """
        Show a comparison view with all images
        
        Args:
            image_paths: List of file paths to display
            title: Title for the comparison
        """
        print(f"\n🔍 {title.upper()}")
        print("=" * len(title) + "==")
        
        for i, path in enumerate(image_paths, 1):
            filename = Path(path).name
            print(f"  {i}. {filename}")
        
        self.display_images(image_paths, {})
        
        input(f"\nPress Enter when you've reviewed all {len(image_paths)} images...")