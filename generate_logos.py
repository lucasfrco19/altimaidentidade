from PIL import Image, ImageOps
import os

def process_logos():
    original_path = 'logo sem fundo.png'
    if not os.path.exists(original_path):
        print(f"Error: {original_path} not found.")
        return

    img = Image.open(original_path).convert("RGBA")
    
    # Generate White Logo (Negative)
    white_img = Image.new("RGBA", img.size)
    pixels = img.load()
    new_pixels = white_img.load()
    
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            r, g, b, a = pixels[x, y]
            if a > 0:
                new_pixels[x, y] = (255, 255, 255, a)
            else:
                new_pixels[x, y] = (0, 0, 0, 0)
    
    white_img.save('logo-branca.png')
    print("Saved logo-branca.png")

    # Generate Monochromatic Logo (Grayscale)
    mono_img = Image.new("RGBA", img.size)
    mono_pixels = mono_img.load()
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            r, g, b, a = pixels[x, y]
            if a > 0:
                # Standard grayscale formula (luminosity)
                v = int(0.299 * r + 0.587 * g + 0.114 * b)
                mono_pixels[x, y] = (v, v, v, a)
            else:
                mono_pixels[x, y] = (0, 0, 0, 0)
    
    mono_img.save('logo-monocromatica.png')
    print("Saved logo-monocromatica.png")

if __name__ == "__main__":
    process_logos()
