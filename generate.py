import os
import sys
from PIL import Image, ImageDraw, ImageFont
import numpy as np

def generate(magnitude, region, country, depth, time_str, output_path="output.jpg"):
    img = Image.open("template.png").convert("RGBA")
    W, H = img.size

    # Radyal gradient overlay
    arr = np.array(img, dtype=np.float32)
    cx, cy = W / 2, H / 2
    Y, X = np.ogrid[:H, :W]
    dist = np.sqrt((X - cx)**2 + (Y - cy)**2)
    max_dist = np.sqrt(cx**2 + cy**2)
    t = np.clip(dist / max_dist, 0, 1)
    darken = t ** 1.4 * 0.75
    arr[:,:,0] = np.clip(arr[:,:,0] * (1 - darken), 0, 255)
    arr[:,:,1] = np.clip(arr[:,:,1] * (1 - darken), 0, 255)
    arr[:,:,2] = np.clip(arr[:,:,2] * (1 - darken), 0, 255)
    glow = (1 - t) ** 2 * 35
    arr[:,:,0] = np.clip(arr[:,:,0] + glow, 0, 255)
    img = Image.fromarray(arr.astype(np.uint8))
    draw = ImageDraw.Draw(img)

    # Fontlar
    f_region    = ImageFont.truetype("/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf", 88)
    f_country   = ImageFont.truetype("/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf", 58)
    f_magnitude = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 420)
    f_details   = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 52)

    def center(text, font, y, color=(255,255,255,255)):
        bbox = draw.textbbox((0,0), text, font=font)
        tw = bbox[2] - bbox[0]
        draw.text(((W - tw) / 2, y), text, font=font, fill=color)

    center(region.upper(),  f_region,    100, (255,255,255,230))
    center(country.upper(), f_country,   205, (200,200,200,180))
    center(magnitude,       f_magnitude, 650, (255,255,255,255))
    center(depth,           f_details,  1650, (200,200,200,200))
    center(time_str,        f_details,  1720, (200,200,200,200))

    img.convert("RGB").save(output_path, "JPEG", quality=95)
    print(f"Kaydedildi: {output_path}")

if __name__ == "__main__":
    generate(
        magnitude = sys.argv[1] if len(sys.argv) > 1 else "4.2",
        region    = sys.argv[2] if len(sys.argv) > 2 else "California",
        country   = sys.argv[3] if len(sys.argv) > 3 else "United States",
        depth     = sys.argv[4] if len(sys.argv) > 4 else "Depth: 10 km",
        time_str  = sys.argv[5] if len(sys.argv) > 5 else "2026-10-25 · 14:32 UTC"
    )
