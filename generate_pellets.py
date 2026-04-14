import random
import math
import os

OUTPUT_DIR = r"D:\JSR Pharma\images"

def create_pellet_svg(filename, color_start, color_end, count=200, style="glossy"):
    width = 400
    height = 300
    
    svg_content = f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">'
    
    # Background
    svg_content += f'<rect width="100%" height="100%" fill="#f8f9fa"/>'
    
    # Definitions for gradients
    svg_content += '<defs>'
    for i in range(10):
        # Create slightly different gradients for realism
        ratio = i / 10.0
        c1 = interpolate_color(color_start, color_end, ratio + (random.random() * 0.1 - 0.05))
        c2 = interpolate_color(color_start, "#000000", 0.1) # Shadow color
        
        grad_id = f'grad_{i}'
        
        if style == "glossy":
            svg_content += f'''
            <radialGradient id="{grad_id}" cx="30%" cy="30%" r="70%" fx="30%" fy="30%">
                <stop offset="0%" style="stop-color:#ffffff;stop-opacity:0.9" />
                <stop offset="20%" style="stop-color:{c1};stop-opacity:1" />
                <stop offset="100%" style="stop-color:{c2};stop-opacity:0.6" />
            </radialGradient>
            '''
        else: # Matte/Rough
            svg_content += f'''
            <radialGradient id="{grad_id}" cx="40%" cy="40%" r="80%" fx="30%" fy="30%">
                <stop offset="0%" style="stop-color:{c1};stop-opacity:1" />
                <stop offset="90%" style="stop-color:{c2};stop-opacity:0.4" />
            </radialGradient>
            '''
    svg_content += '</defs>'
    
    # Draw pellets
    pellets = []
    
    # Generate random positions
    for _ in range(count):
        r = random.uniform(15, 35) # Radius
        x = random.uniform(r, width - r)
        y = random.uniform(r, height - r)
        z = random.uniform(0, 1) # Depth for sorting
        pellets.append({'x': x, 'y': y, 'r': r, 'z': z})
        
    # Sort by Z to draw back-to-front
    pellets.sort(key=lambda p: p['y'] + p['z']*10)
    
    for p in pellets:
        grad_idx = random.randint(0, 9)
        # Drop shadow
        svg_content += f'<circle cx="{p["x"]+2}" cy="{p["y"]+2}" r="{p["r"]}" fill="rgba(0,0,0,0.1)" />'
        # Sphere
        svg_content += f'<circle cx="{p["x"]}" cy="{p["y"]}" r="{p["r"]}" fill="url(#grad_{grad_idx})" stroke="rgba(0,0,0,0.05)" stroke-width="1"/>'

    svg_content += '</svg>'
    
    with open(os.path.join(OUTPUT_DIR, filename), "w") as f:
        f.write(svg_content)

def interpolate_color(c1, c2, factor):
    # Very basic hex interpolation
    h1 = c1.lstrip('#')
    h2 = c2.lstrip('#')
    rgb1 = tuple(int(h1[i:i+2], 16) for i in (0, 2, 4))
    rgb2 = tuple(int(h2[i:i+2], 16) for i in (0, 2, 4))
    
    new_rgb = [
        max(0, min(255, int(rgb1[i] + (rgb2[i] - rgb1[i]) * factor))) 
        for i in range(3)
    ]
        
    return '#{:02x}{:02x}{:02x}'.format(*new_rgb)

# Generate Images
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# 1. Sugar Pellets (Bright White, Glossy)
create_pellet_svg("sugar_pellets.svg", "#ffffff", "#e0e0e0", count=250, style="glossy")

# 2. MCC Pellets (Off-white, Matte/Rough)
create_pellet_svg("mcc_pellets.svg", "#fcfcfc", "#dcdcdc", count=300, style="matte")

# 3. Lactose Pellets (Creamy, Matte)
create_pellet_svg("lactose_pellets.svg", "#fffdd0", "#e6e0b0", count=220, style="matte")

# 4. Starch Pellets (Pure White, Matte)
create_pellet_svg("starch_pellets.svg", "#ffffff", "#eeeeee", count=280, style="matte")

# 5. NPS (Tiny, Glossy)
create_pellet_svg("nps.svg", "#f0f8ff", "#cbd5e1", count=400, style="glossy")

print("Images generated successfully!")
