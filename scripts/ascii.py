"""Convert a photo to ASCII art lines (used for the README card).

The background is dropped with a simple colour mask (dark pixels + skin tones
count as the subject), so only the person is drawn.
"""
import sys
from PIL import Image, ImageDraw, ImageOps, ImageFilter

RAMP = " .'`^\",:;Il!i~+_-?][}{1)(|/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"


def _subject_mask(rgb, region=None):
    w, h = rgb.size
    src = rgb.load()
    mask = Image.new("L", (w, h))
    m = mask.load()
    for y in range(h):
        for x in range(w):
            r, g, b = src[x, y]
            lum = 0.299 * r + 0.587 * g + 0.114 * b
            skin = r > g > b and r - b > 30
            m[x, y] = 255 if (lum < 95 or skin) else 0
    mask = mask.filter(ImageFilter.MedianFilter(9))
    if region:  # rough outline of the person, ignores rocks/grass
        keep = Image.new("L", (w, h))
        d = ImageDraw.Draw(keep)
        d.ellipse(region["head"], fill=255)
        d.polygon(region["body"], fill=255)
        mask = Image.composite(mask, keep, keep)
    return mask


# Outline of the subject in the source photo's pixel coordinates.
REGION = {"head": (250, 150, 590, 560), "body": [(300, 500), (560, 500), (760, 677), (180, 677)]}


def to_ascii(path, cols=44, rows=26, box=None, region=REGION):
    rgb = Image.open(path).convert("RGB")
    mask = _subject_mask(rgb, region)
    if box:
        rgb, mask = rgb.crop(box), mask.crop(box)
    small_mask = mask.resize((cols, rows), Image.BILINEAR)
    gray = ImageOps.equalize(rgb.convert("L"), mask).resize((cols, rows), Image.LANCZOS)
    g, mk = gray.load(), small_mask.load()
    out = []
    for y in range(rows):
        line = ""
        for x in range(cols):
            if mk[x, y] < 128:
                line += " "
                continue
            v = 1 - g[x, y] / 255  # darker pixel -> denser glyph
            line += RAMP[1 + int(v * (len(RAMP) - 2))]
        out.append(line.rstrip())
    return out


if __name__ == "__main__":
    print("\n".join(to_ascii(sys.argv[1], cols=53, rows=27, box=(225, 150, 640, 640))))
