import numpy as np
from PIL import Image, ImageDraw
import os

def generate_stealth_mask(output_path="output/Stealth_Plate_Print_Template_v2.pdf"):
    # Dimensions (12x6 inches at 300 DPI)
    dpi = 300
    width = 12 * dpi
    height = 6 * dpi
    
    # 1. Create Base (Transparent)
    # Mode 'RGBA' for transparency
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    
    # 2. Load Hat Tile Pattern
    hat_pattern_path = r"C:\Users\Media Server\Desktop\GhostPlate_Launch\Stealth_Plate_Print_Template.png"
    if os.path.exists(hat_pattern_path):
        hat_img = Image.open(hat_pattern_path).convert('L')
        hat_img = hat_img.resize((width, height), Image.NEAREST)
        hat_mask = np.array(hat_img) > 128
    else:
        print(f"Warning: Hat pattern not found at {hat_pattern_path}. Using full area.")
        hat_mask = np.ones((height, width), dtype=bool)

    # 3. Generate Noise Pattern
    # To make noise 20% larger, we generate at a lower resolution and scale up.
    noise_width = int(width / 1.2)
    noise_height = int(height / 1.2)
    noise_array_small = np.random.rand(noise_height, noise_width)
    
    # Create mask where noise > 0.8 (20% coverage density)
    mask_small = (noise_array_small > 0.8)
    
    # Upscale mask to full size using NEAREST to maintain "grit" size
    mask_full_img = Image.fromarray(mask_small.astype(np.uint8) * 255, mode='L')
    mask_full_img = mask_full_img.resize((width, height), Image.NEAREST)
    mask = np.array(mask_full_img) > 0
    
    # Apply Hat Pattern Overlay
    mask = mask & hat_mask
    
    # 4. Create the Ink Layer
    # Color: Black (0,0,0)
    # Alpha: 52 (30% increase from 40). 
    ink_layer = np.zeros((height, width, 4), dtype=np.uint8)
    ink_layer[mask] = [0, 0, 0, 52] 
    
    # Convert back to PIL
    noise_img = Image.fromarray(ink_layer, 'RGBA')
    
    # 5. Composite
    img.alpha_composite(noise_img)
    
    # 6. Add Crop Marks (Guides for cutting)
    draw = ImageDraw.Draw(img)
    # Draw a thin black border (1px) for cutting guide
    draw.rectangle([(0,0), (width-1, height-1)], outline=(0,0,0,255), width=5)
    
    # 7. Save as PDF
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
