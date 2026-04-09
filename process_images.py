import os
from PIL import Image

def remove_watermark(image_path):
    print(f"Processing watermark removal: {image_path}")
    img = Image.open(image_path).convert("RGBA")
    width, height = img.size
    
    # Define a 60x60 square in the bottom right
    # The sparkle is usually small and in the very corner
    box_size = 60
    box = (width - box_size - 10, height - box_size - 10, width - 10, height - 10)
    
    # Sample a color from just outside the box (to the left)
    sample_pixel = (width - box_size - 20, height - (box_size // 2) - 10)
    fill_color = img.getpixel(sample_pixel)
    
    # Create a patch
    patch = Image.new("RGBA", (box_size, box_size), fill_color)
    img.paste(patch, (width - box_size - 10, height - box_size - 10))
    
    # Save back to original
    img.convert("RGB").save(image_path, quality=95)

def create_variations(image_path, prefix):
    print(f"Creating variations for: {image_path}")
    img = Image.open(image_path).convert("RGBA")
    
    # White (Negative)
    white_img = Image.new("RGBA", img.size)
    pixels = img.load()
    new_pixels = white_img.load()
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            r, g, b, a = pixels[x, y]
            if a > 0:
                new_pixels[x, y] = (255, 255, 255, a)
    white_img.save(f"{prefix}-negativa.png")
    
    # Silver (Monochromatic)
    silver_img = Image.new("RGBA", img.size)
    new_pixels = silver_img.load()
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            r, g, b, a = pixels[x, y]
            if a > 0:
                # Silver color #C0C0C0
                new_pixels[x, y] = (192, 192, 192, a)
    silver_img.save(f"{prefix}-monocromatica.png")

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
        remove_watermark(m)

# Logo variations
if os.path.exists("logosemfundo.png"):
    create_variations("logosemfundo.png", "logo")

if os.path.exists("altimaclinicaintegrada.png"):
    create_variations("altimaclinicaintegrada.png", "logo-texto")

if os.path.exists("iconelogo.png"):
    create_variations("iconelogo.png", "icone")

print("Done!")
