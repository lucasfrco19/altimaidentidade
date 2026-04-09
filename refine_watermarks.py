import os
from PIL import Image, ImageFilter

def remove_watermark_refined(image_path):
    print(f"Refining watermark removal: {image_path}")
    img = Image.open(image_path).convert("RGBA")
    width, height = img.size
    
    # Search for the brightest spot in the bottom-right corner (last 100x100 pixels)
    corner_size = 100
    search_area = img.crop((width - corner_size, height - corner_size, width, height))
    search_pixels = search_area.load()
    
    max_bright = -1
    brightest_pos = (0, 0)
    
    for y in range(corner_size):
        for x in range(corner_size):
            r, g, b, a = search_pixels[x, y]
            brightness = r + g + b
            if brightness > max_bright:
                max_bright = brightness
                brightest_pos = (x, y)
    
    # Coordinates in original image
    target_x = width - corner_size + brightest_pos[0]
    target_y = height - corner_size + brightest_pos[1]
    
    # If the brightest spot is actually quite bright (like a sparkle)
    # The sparkle is roughly 20-30 pixels
    patch_size = 30
    box = (target_x - patch_size // 2, target_y - patch_size // 2, 
           target_x + patch_size // 2, target_y + patch_size // 2)
    
    # Sample color from a few pixels away to the left
    sample_pixel = (max(0, target_x - patch_size), target_y)
    fill_color = img.getpixel(sample_pixel)
    
    # Create a small patch and blur it to blend
    patch = Image.new("RGBA", (patch_size, patch_size), fill_color)
    img.paste(patch, (target_x - patch_size // 2, target_y - patch_size // 2))
    
    # Apply a light blur only to that area to blend the edges
    # (Optional, but helps)
    
    # Save back to original
    img.convert("RGB").save(image_path, quality=98)

# Paths
base_dir = r"c:\Users\lucas\Downloads\Identidade Visual - Médico"
os.chdir(base_dir)

mockups = [
    "mockup-balcão.png", "mockup-cadeira.png", "mockup-copo.png",
    "mockup-janela.png", "mockup-placa-fosca.png", "mockup-placa-vidro.png",
    "mockup-tablet.png", "mockup-tv.png", "mockup-variacao.png",
    "fachada.png", "papelaria.png"
]

for m in mockups:
    if os.path.exists(m):
        remove_watermark_refined(m)

print("Refinement done!")
