import ezdxf

def generate_plate_dxf(filename="output/plate_cover_cutline.dxf"):
    # Create a new DXF document (AutoCAD 2010 format)
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()

    # Dimensions (Inches)
    width = 12.0
    height = 6.0
    radius = 0.5
    hole_diameter = 0.25
    hole_radius = hole_diameter / 2.0

    # SAE Hole Spacing
    # Horizontal: 7.0" (Center-to-center)
    # Vertical: 4.75" (Center-to-center)
    h_offset = 7.0 / 2.0
    v_offset = 4.75 / 2.0
    center_x = width / 2.0
    center_y = height / 2.0

    # 1. DRAW OUTER BOUNDARY (Rounded Rectangle)
    # Bottom Line
    msp.add_line((radius, 0), (width - radius, 0))
    # Top Line
    msp.add_line((radius, height), (width - radius, height))
    # Left Line
    msp.add_line((0, radius), (0, height - radius))
    # Right Line
    msp.add_line((width, radius), (width, height - radius))

    # Corners (Arcs)
    msp.add_arc((radius, radius), radius, 180, 270)          # Bottom-Left
    msp.add_arc((width - radius, radius), radius, 270, 0)    # Bottom-Right
    msp.add_arc((width - radius, height - radius), radius, 0, 90) # Top-Right
    msp.add_arc((radius, height - radius), radius, 90, 180)  # Top-Left

    # 2. DRAW MOUNTING HOLES (Circles)
    hole_positions = [
        (center_x - h_offset, center_y - v_offset), # Bottom-Left Hole
        (center_x + h_offset, center_y - v_offset), # Bottom-Right Hole
        (center_x + h_offset, center_y + v_offset), # Top-Right Hole
        (center_x - h_offset, center_y + v_offset)  # Top-Left Hole
    ]

    for pos in hole_positions:
        msp.add_circle(pos, radius=hole_radius)

    # Save
    doc.saveas(filename)
    print(f"DXF file saved to: {filename}")

if __name__ == "__main__":
    generate_plate_dxf()
