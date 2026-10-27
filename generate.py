import os
import sys
from PIL import Image, ImageDraw, ImageFont

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
    # Şablonu aç (1080x1920 veya benzeri dik dikey şablon)
    img = Image.open("template.png").convert("RGBA")
    W, H = img.size
    draw = ImageDraw.Draw(img)

    # Font tanımlamaları
    f_region    = ImageFont.truetype("Poppins-Bold.ttf", 75)
    f_country   = ImageFont.truetype("Poppins-Bold.ttf", 50)
    f_magnitude = ImageFont.truetype("Jersey M54.ttf", 420) # Ortada devasa büyüklük
    f_depth     = ImageFont.truetype("LiberationSans-Regular.ttf", 55)
    f_time      = ImageFont.truetype("LiberationSans-Regular.ttf", 48)

    def center(text, font, y, color=(255,255,255,255)):
        bbox = draw.textbbox((0,0), text, font=font)
        tw = bbox[2] - bbox[0]
        draw.text(((W - tw) / 2, y), text, font=font, fill=color)

    # 1. ÜST: Lokasyon Adı (Region ve Country ardışık)
    y = 120
    region_lines = wrap_text(region.upper(), f_region, W - 80, draw)
    for line in region_lines:
        center(line, f_region, y, (255,255,255,255))
        y += 90

    country_lines = wrap_text(country.upper(), f_country, W - 80, draw)
    for line in country_lines:
        center(line, f_country, y, (200,200,200,200))
        y += 65

    # 2. ORTA: Büyük Jersey Fontunda Büyüklük (Dikeyde ortalanmış alan)
    center(magnitude, f_magnitude, 750, (255,255,255,255))

    # 3. ALT: Derinlik ve Altında Zaman (İkonlar tamamen kaldırıldı)
    center(depth.upper(), f_depth, 1450, (230,220,220,230))
    center(time_str.upper(), f_time, 1530, (180,180,180,200))

    img.convert("RGB").save(output_path, "JPEG", quality=95)
    print(f"Yeni tasarımlı görsel kaydedildi: {output_path}")

if __name__ == "__main__":
    generate(
        magnitude = sys.argv[1] if len(sys.argv) > 1 else "4.2",
        region    = sys.argv[2] if len(sys.argv) > 2 else "California",
        country   = sys.argv[3] if len(sys.argv) > 3 else "United States",
        depth     = sys.argv[4] if len(sys.argv) > 4 else "Depth: 10 km",
        time_str  = sys.argv[5] if len(sys.argv) > 5 else "2026-10-26 · 19:32 UTC"
    )
