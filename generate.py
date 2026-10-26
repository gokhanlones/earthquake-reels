import os
import sys
from PIL import Image, ImageDraw, ImageFont
import numpy as np

def wrap_text(text, font, max_width, draw):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        test = (current + " " + word).strip()
        bbox = draw.textbbox((0,0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines

def generate(magnitude, region, country, depth, time_str, output_path="output.jpg"):
    img = Image.open("template.png").convert("RGBA")
    W, H = img.size
    draw = ImageDraw.Draw(img)

    f_region    = ImageFont.truetype("Poppins-Bold.ttf", 80)
    f_country   = ImageFont.truetype("Poppins-Bold.ttf", 54)
    f_magnitude = ImageFont.truetype("Jersey M54.ttf", 380)
    f_details   = ImageFont.truetype("LiberationSans-Regular.ttf", 52)

    def center(text, font, y, color=(255,255,255,255)):
        bbox = draw.textbbox((0,0), text, font=font)
        tw = bbox[2] - bbox[0]
        draw.text(((W - tw) / 2, y), text, font=font, fill=color)

    # Üst - Region
    region_lines = wrap_text(region.upper(), f_region, W - 80, draw)
    y = 60
    for line in region_lines:
        center(line, f_region, y, (255,255,255,230))
        y += 95

    # Country
    country_lines = wrap_text(country.upper(), f_country, W - 80, draw)
    for line in country_lines:
        center(line, f_country, y, (200,200,200,180))
        y += 68

    # Orta - Büyüklük
    center(magnitude, f_magnitude, 580, (255,255,255,255))

    # Alt - Detaylar
    center(depth,    f_details, 1480, (220,220,220,210))
    center(time_str, f_details, 1550, (220,220,220,210))

    img.convert("RGB").save(output_path, "JPEG", quality=95)
    print(f"Kaydedildi: {output_path}")

if __name__ == "__main__":
    generate(
        magnitude = sys.argv[1] if len(sys.argv) > 1 else "4.2",
        region    = sys.argv[2] if len(sys.argv) > 2 else "California",
        country   = sys.argv[3] if len(sys.argv) > 3 else "United States",
        depth     = sys.argv[4] if len(sys.argv) > 4 else "Depth: 10 km",
        time_str  = sys.argv[5] if len(sys.argv) > 5 else "2026-10-26 · 19:32 UTC"
    )
