from PIL import Image, ImageDraw

def crop_to_circle(input_path, output_path):
    print(f"Opening {input_path}")
    img = Image.open(input_path).convert("RGBA")
    w, h = img.size
    
    # We want to crop to the black ring. We scan to find the actual circle.
    pixels = img.load()
    left, top, right, bottom = w, h, 0, 0
    
    # Background in the cropped user image is white, we look for dark pixels (the ring)
    # The ring is completely black, so R<50, G<50, B<50
    for y in range(h):
        for x in range(w):
            r, g, b, a = pixels[x, y]
            if a > 0 and r < 50 and g < 50 and b < 50:
                if x < left: left = x
                if x > right: right = x
                if y < top: top = y
                if y > bottom: bottom = y

    # Failsafe if not found
    if left >= right or top >= bottom:
        left, top, right, bottom = 0, 0, w, h
    else:
        # Add 2 pixels padding to prevent harsh cutoffs on antialiased edges
        left = max(0, left - 2)
        top = max(0, top - 2)
        right = min(w, right + 2)
        bottom = min(h, bottom + 2)

    width = right - left
    height = bottom - top
    
    print(f"Circle bounds detected: {left}, {top}, {right}, {bottom}")
    
    # Crop to the tight bounds
    img_cropped = img.crop((left, top, right, bottom))
    
    # Create the circular alpha mask
    mask = Image.new("L", img_cropped.size, 0)
    draw = ImageDraw.Draw(mask)
    # Draw white ellipse covering the cropped boundaries exactly
    draw.ellipse((0, 0, width, height), fill=255)
    
    # Apply mask
    result = Image.new("RGBA", img_cropped.size, (0, 0, 0, 0))
    result.paste(img_cropped, (0, 0), mask=mask)
    
    # Make square bounding box for a perfect favicon
    size = max(width, height)
    final_result = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    x_offset = (size - width) // 2
    y_offset = (size - height) // 2
    final_result.paste(result, (x_offset, y_offset))
    
    # Standardize to 512x512 max favicon size (high res)
    final_result.thumbnail((512, 512), Image.Resampling.LANCZOS)
    
    final_result.save(output_path, format="PNG")
    print(f"Saved circle favicon to {output_path}")

try:
    crop_to_circle("d:/JSR Pharma/images/new_color_logo.png", "d:/JSR Pharma/images/favicon_circle.png")
except Exception as e:
    print(f"Error: {e}")
