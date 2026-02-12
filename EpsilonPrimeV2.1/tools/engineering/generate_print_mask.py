import numpy as np
from PIL import Image, ImageDraw
import os

def generate_stealth_mask(output_path="output/Stealth_Plate_Print_Template.pdf"):
    # Dimensions (12x6 inches at 300 DPI)
    dpi = 300
    width = 12 * dpi
    height = 6 * dpi
    
    # 1. Create Base (Transparent)
    # Mode 'RGBA' for transparency
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    
    # 2. Generate Noise Pattern
    # We want "Salt and Pepper" noise to mimic the grit
    # Coverage: 50% of pixels have noise
    noise_array = np.random.rand(height, width)
    
    # Create mask where noise > 0.8 (20% coverage density)
    # This matches the "High Intensity" simulation
    mask = (noise_array > 0.8)
    
    # 3. Create the Ink Layer
    # Color: Black (0,0,0)
    # Alpha: 40 (approx 15%). 
    # Logic: 15% black is barely visible on a clear sheet against a car, 
    # but Carbon Black ink absorbs IR strongly.
    ink_layer = np.zeros((height, width, 4), dtype=np.uint8)
    ink_layer[mask] = [0, 0, 0, 40] 
    
    # Convert back to PIL
    noise_img = Image.fromarray(ink_layer, 'RGBA')
    
    # 4. Composite
    img.alpha_composite(noise_img)
    
    # 5. Add Crop Marks (Guides for cutting)
    draw = ImageDraw.Draw(img)
    # Draw a thin black border (1px) for cutting guide
    draw.rectangle([(0,0), (width-1, height-1)], outline=(0,0,0,255), width=5)
    
    # 6. Save as PDF
    # PIL requires RGB for PDF usually, but we need transparency/layers?
    # Actually, for OfficeMax printing, a high-res PNG or PDF is fine.
    # We'll save as PNG first, then convert to PDF to ensure size.
    
    img.save(output_path.replace(".pdf", ".png"), dpi=(300,300))
    
    # To save as PDF, we usually need a background. 
    # Since this is for CLEAR plastic printing, we leave it. 
    # But PIL PDF doesn't support alpha well.
    # We will provide the PNG which allows the printer to choose "Transparency" mode.
    
    print(f"Generated Print Template: {output_path.replace('.pdf', '.png')}")

if __name__ == "__main__":
    generate_stealth_mask()