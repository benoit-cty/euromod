"""Draw the app icon: a white 'N' on the blue disc of the UI's logo.

Regenerate every size with:
    python3 src-tauri/icons/source/make_icon.py && npx tauri icon src-tauri/icons/source/icon-1024.png
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

S = 1024
img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
d = ImageDraw.Draw(img)
# Radial-ish gradient disc, #4f72c9 -> #1f3d8f, as in App.svelte's .logo
inner, outer = (0x4F, 0x72, 0xC9), (0x1F, 0x3D, 0x8F)
pad = 24
for i in range(200):
    t = i / 199
    r = int((S / 2 - pad) * (1 - t))
    c = tuple(int(outer[k] + (inner[k] - outer[k]) * t) for k in range(3))
    cx, cy = S * 0.5 - t * S * 0.08, S * 0.5 - t * S * 0.1
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c + (255,))
d.ellipse([pad, pad, S - pad, S - pad], outline=(255, 255, 255, 255), width=28)
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 620)
box = d.textbbox((0, 0), "N", font=font)
w, h = box[2] - box[0], box[3] - box[1]
d.text(((S - w) / 2 - box[0], (S - h) / 2 - box[1]), "N", font=font, fill=(255, 255, 255, 255))
img.save(Path(__file__).with_name("icon-1024.png"))
