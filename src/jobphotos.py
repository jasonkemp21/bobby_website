#!/usr/bin/env python3
"""Turns the owners' phone photos into the job photos in img/.

    python3 src/jobphotos.py <folder holding the original .heic or .jpg files>

Needs Pillow and pillow-heif:  pip install pillow pillow-heif

Every photo gets a fixed crop, the same light grade and two sizes (1200 and 600 wide).
Camera data is dropped on the way out. Most of these were taken inside customers' homes
and the originals carry GPS coordinates, which must never reach the website.

To add a photo: add a row to PHOTOS, run this, then give it an entry in JOBS in content.py.
"""
import os
import sys

from PIL import Image, ImageChops, ImageEnhance, ImageOps

try:
    import pillow_heif
    pillow_heif.register_heif_opener()
except ImportError:  # .jpg originals still work without it
    pillow_heif = None

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "img")

# original file (without extension), output name, shape, crop as fractions of the
# upright photo (left, top, right, bottom), extra options
TALL = (1200, 1500)   # 4:5, used in page headers and the job grids
WIDE = (1200, 900)    # 4:3, used beside text
PHOTOS = [
    ("IMG_3580", "boiler", TALL, (0.000, 0.030, 1.000, 0.9675), {}),
    ("IMG_3589", "furnace", TALL, (0.285, 0.293, 0.890, 0.860), {}),
    ("IMG_3587", "condensers", TALL, (0.000, 0.0575, 1.000, 0.995), {}),
    ("67216582904__9384F24C-EE32-4503-8343-B511C6F04018", "ductless", TALL, (0.121, 0.173, 0.897, 0.9005), {}),
    ("IMG_3920", "water-heaters", TALL, (0.048, 0.091, 0.921, 0.909), {}),
    ("IMG_4077", "water-heater", TALL, (0.060, 0.090, 1.000, 0.9713), {}),
    # the pink foam board behind this one shouts; "calm_pink" greys it down
    ("IMG_0695", "filtration", TALL, (0.303, 0.164, 1.000, 0.817), {"calm_pink": True}),
    ("IMG_6449", "ac-pair", WIDE, (0.130, 0.150, 0.960, 0.980), {}),
]


def find(folder, stem):
    for name in os.listdir(folder):
        base, ext = os.path.splitext(name)
        if base == stem and ext.lower() in (".heic", ".jpg", ".jpeg", ".png"):
            return os.path.join(folder, name)
    return None


def calm_pink(im):
    """Pull the saturation out of pinks and magentas only (hue roughly 285 to 350 degrees)."""
    h, s, v = im.convert("HSV").split()
    lo, hi, feather = 285 * 255 // 360, 350 * 255 // 360, 8

    def keep(hue):  # 255 keeps the colour, small values grey it
        if lo <= hue <= hi:
            return 30
        d = min(abs(hue - lo), abs(hue - hi))
        return 255 if d >= feather else 30 + (225 * d) // feather
    s = ImageChops.multiply(s, h.point([keep(i) for i in range(256)]))
    return Image.merge("HSV", (h, s, v)).convert("RGB")


def grade(im, opts):
    """One grade for every photo: even out the exposure, take the colour down so mixed
    basement lighting sits with the site's black, white and tan, and warm it a touch."""
    im = ImageOps.autocontrast(im, cutoff=(0.4, 0.4), preserve_tone=True)
    if opts.get("calm_pink"):
        im = calm_pink(im)
    im = ImageEnhance.Color(im).enhance(0.62)
    r, g, b = im.split()
    r = r.point(lambda x: min(255, round(x * 1.025)))
    b = b.point(lambda x: round(x * 0.955))
    im = Image.merge("RGB", (r, g, b))
    return ImageEnhance.Contrast(im).enhance(1.04)


def main(folder):
    for stem, name, (w, h), box, opts in PHOTOS:
        src = find(folder, stem)
        if not src:
            print("skip (not found):", stem)
            continue
        im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
        x0, y0, x1, y1 = box
        im = im.crop((round(x0 * im.width), round(y0 * im.height), round(x1 * im.width), round(y1 * im.height)))
        im = grade(ImageOps.fit(im, (w, h), Image.LANCZOS), opts)
        # a fresh image object carries no EXIF, so nothing about the camera or the place is written
        im.save(os.path.join(OUT, f"job-{name}.webp"), "WEBP", quality=70, method=6)
        im.resize((w // 2, h // 2), Image.LANCZOS).save(os.path.join(OUT, f"job-{name}-600.webp"), "WEBP", quality=76, method=6)
        print("wrote", f"job-{name}.webp", f"{w}x{h}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
