"""Draws img/hero-lines.svg, the backdrop of the home hero.

A hot water loop in the logo's tan: supply main along the top of the hero, return main along the
bottom, joined by a riser on the right. The mains sit in the hero's top and bottom padding, so they
stay visible at every window width without running behind the headline or the card.
Pipes are hollow: a tan stroke with a black stroke on top.
Run: python3 src/herolines.py
"""
import os

TAN, INK = "#c8a880", "#101113"
W, H = 2600, 800
TOP, BOT = 46, 754          # centre lines of the two mains
RISER = W - 150             # main riser
R = 34                      # elbow radius


def pipe(d):
    return (f'<path d="{d}" fill="none" stroke="{TAN}" stroke-width="18" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="12" stroke-linejoin="round"/>')


def flange(x, y, vertical=False):
    if vertical:
        return f'<rect x="{x - 17}" y="{y - 4}" width="34" height="8" fill="{TAN}"/>'
    return f'<rect x="{x - 4}" y="{y - 17}" width="8" height="34" fill="{TAN}"/>'


def valve(x, y, up=True, vertical=False):
    if vertical:
        body = f'<path d="M{x - 17},{y - 26} L{x + 17},{y + 26} L{x - 17},{y + 26} L{x + 17},{y - 26} Z" fill="{INK}" stroke="{TAN}" stroke-width="3" stroke-linejoin="round"/>'
        stem = f'<path d="M{x},{y} H{x + 36} M{x + 36},{y - 18} V{y + 18}" fill="none" stroke="{TAN}" stroke-width="3"/>'
        return body + stem
    s = -1 if up else 1
    body = f'<path d="M{x - 26},{y - 17} L{x + 26},{y + 17} L{x + 26},{y - 17} L{x - 26},{y + 17} Z" fill="{INK}" stroke="{TAN}" stroke-width="3" stroke-linejoin="round"/>'
    stem = f'<path d="M{x},{y} V{y + s * 34} M{x - 18},{y + s * 34} H{x + 18}" fill="none" stroke="{TAN}" stroke-width="3"/>'
    return body + stem


def arrow(x, y, d):
    pts = {"l": f"{x + 9},{y - 7} {x - 9},{y} {x + 9},{y + 7}", "r": f"{x - 9},{y - 7} {x + 9},{y} {x - 9},{y + 7}",
           "d": f"{x - 7},{y - 9} {x},{y + 9} {x + 7},{y - 9}", "u": f"{x - 7},{y + 9} {x},{y - 9} {x + 7},{y + 9}"}[d]
    return f'<polygon points="{pts}" fill="{TAN}"/>'


def label(x, y, t):
    return f'<text x="{x}" y="{y}" font-family="Arial Narrow, Arial, sans-serif" font-size="17" font-weight="700" letter-spacing="3" fill="{TAN}">{t}</text>'


def build():
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">']
    # the loop: supply runs right along the top, turns down the riser, returns left along the bottom
    o.append(pipe(f"M0,{TOP} H{RISER - R} a{R},{R} 0 0 1 {R},{R} V{BOT - R} a{R},{R} 0 0 1 -{R},{R} H0"))
    # a second riser past the loop, top to bottom, for wide windows
    o.append(pipe(f"M{W - 60},0 V{H}"))
    for x in range(W - 330, 0, -260):
        o.append(flange(x, TOP))
        o.append(flange(x - 130, BOT))
    for y in (220, 400, 580):
        o.append(flange(RISER, y, True))
    for y in (130, 330, 520, 690):
        o.append(flange(W - 60, y, True))
    o.append(valve(W - 700, TOP, up=False))
    o.append(valve(W - 1500, TOP, up=False))
    o.append(valve(W - 1000, BOT, up=True))
    o.append(valve(W - 1850, BOT, up=True))
    o.append(valve(RISER, 300, vertical=True))
    for x in (W - 420, W - 900, W - 1300, W - 1900, W - 2300):
        o.append(arrow(x, TOP, "r"))
        o.append(arrow(x - 60, BOT, "l"))
    o.append(arrow(RISER, 470, "d"))
    o.append(arrow(W - 60, 240, "d"))
    # labels only near the right, where nothing else sits in the hero's padding
    o.append(label(W - 400, TOP + 40, "HWS"))
    o.append(label(W - 400, BOT - 26, "HWR"))
    o.append("</svg>")
    return "".join(o)


if __name__ == "__main__":
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(os.path.join(root, "img", "hero-lines.svg"), "w", encoding="utf-8") as f:
        f.write(build())
    print("wrote img/hero-lines.svg")
