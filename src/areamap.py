"""Draws the service-area map as an inline SVG from county outlines in src/data.

County outlines: OpenStreetMap contributors (ODbL), fetched once through Nominatim.
Town and station positions are approximate and only need to read right at this scale.
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")

# map window
LON0, LON1 = -75.66, -75.03
LAT0, LAT1 = 39.79, 40.165
W = 900
K = math.cos(math.radians((LAT0 + LAT1) / 2))
H = round(W * (LAT1 - LAT0) / ((LON1 - LON0) * K))


def xy(lat, lon):
    x = (lon - LON0) / (LON1 - LON0) * W
    y = (LAT1 - lat) / (LAT1 - LAT0) * H
    return round(x, 1), round(y, 1)


COUNTIES = [
    # file, css class
    ("Burlington_County__New_Jersey", "out"),
    ("Camden_County__New_Jersey", "out"),
    ("Gloucester_County__New_Jersey", "out"),
    ("Salem_County__New_Jersey", "out"),
    ("New_Castle_County__Delaware", "out"),
    ("Bucks_County__Pennsylvania", "out"),
    ("Montgomery_County__Pennsylvania", "out"),
    ("Chester_County__Pennsylvania", "out"),
    ("Philadelphia_County__Pennsylvania", "out"),
    ("Delaware_County__Pennsylvania", "core"),
]

# Paoli/Thorndale rail line, the "Main Line" itself: 30th Street out to Malvern.
# Only the stretch from Overbrook west is drawn; the city end is outside the service area.
RAIL = [
    (39.9557, -75.1820), (39.9735, -75.2190), (39.9895, -75.2496), (39.9990, -75.2513), (40.0048, -75.2613),
    (40.0027, -75.2727), (40.0083, -75.2903), (40.0140, -75.2997), (40.0219, -75.3165), (40.0278, -75.3266),
    (40.0384, -75.3415), (40.0448, -75.3590), (40.0437, -75.3728), (40.0459, -75.3868), (40.0494, -75.4031),
    (40.0472, -75.4229), (40.0481, -75.4424), (40.0431, -75.4609), (40.0429, -75.4838), (40.0364, -75.5157),
]
CORRIDOR = RAIL[2:]  # Overbrook west

# Home base, drawn larger than the other towns
HOME = ("Havertown", 39.9810, -75.3080)

# name, lat, lon, label side (r, l, t, b). Only towns inside the service area get a dot.
TOWNS = [
    ("Ardmore", 40.0083, -75.2903, "tr"),
    ("Bryn Mawr", 40.0219, -75.3165, "l"),
    ("Wayne", 40.0459, -75.3868, "t"),
    ("Paoli", 40.0429, -75.4838, "t"),
    ("Malvern", 40.0364, -75.5157, "b"),
    ("Upper Darby", 39.9600, -75.2610, "b"),
    ("Springfield", 39.9310, -75.3200, "r"),
    ("Newtown Square", 39.9870, -75.4010, "l"),
    ("Media", 39.9170, -75.3880, "l"),
    ("Swarthmore", 39.9020, -75.3500, "r"),
    ("Glen Mills", 39.8890, -75.4930, "b"),
    ("Ridley Park", 39.8810, -75.3240, "b"),
    ("Broomall", 39.9815, -75.3566, "b"),
]

# big quiet region names; the last value marks ones near the edge, hidden when phones crop the map
REGIONS = [
    ("Delaware County", 39.925, -75.445, 0),
    ("Chester County", 39.985, -75.585, 1),
    ("Montgomery County", 40.125, -75.330, 0),
    ("Philadelphia", 40.035, -75.135, 1),
    ("New Jersey", 39.865, -75.105, 1),
    ("Del.", 39.812, -75.575, 1),
]


def _rings(name):
    with open(os.path.join(DATA, name + ".json"), encoding="utf-8") as f:
        g = json.load(f)["features"][0]["geometry"]
    polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
    for poly in polys:
        for ring in poly:
            yield ring


def _path(name):
    parts = []
    for ring in _rings(name):
        pts = [xy(lat, lon) for lon, lat in ring]
        parts.append("M" + " ".join(f"{x},{y}" for x, y in pts) + "Z")
    return "".join(parts)


def area_map_svg():
    o = []
    o.append(f'<svg viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice" role="img" aria-labelledby="map-t map-d" xmlns="http://www.w3.org/2000/svg">')
    o.append('<title id="map-t">Kennedy &amp; Smith Mechanical service area</title>')
    o.append('<desc id="map-d">Map of the service area: Delaware County and the Main Line rail corridor from Overbrook to Malvern, with the home base in Havertown marked.</desc>')
    o.append("<style>"
             ".out{fill:#f1f2ee;stroke:#b9bcb5;stroke-width:1}"
             ".core{fill:#ead9bf;stroke:#101113;stroke-width:2.2}"
             ".corr{fill:none;stroke:#c8a880;stroke-width:34;stroke-linecap:round;stroke-linejoin:round;opacity:.62}"
             ".rail{fill:none;stroke:#101113;stroke-width:3}"
             ".tie{fill:none;stroke:#101113;stroke-width:9;stroke-dasharray:1.6 9}"
             ".dot{fill:#101113}"
             ".home{fill:#101113;stroke:#c8a880;stroke-width:4}"
             ".hn{font:800 21px 'Barlow Condensed','Arial Narrow',Arial,sans-serif;letter-spacing:.05em;text-transform:uppercase;fill:#101113;paint-order:stroke;stroke:#ead9bf;stroke-width:4px;stroke-linejoin:round}"
             ".tn{font:600 17px 'Barlow Condensed','Arial Narrow',Arial,sans-serif;letter-spacing:.04em;text-transform:uppercase;fill:#101113;paint-order:stroke;stroke:#fff;stroke-width:3.5px;stroke-linejoin:round}"
             ".rg{font:700 16px 'Barlow Condensed','Arial Narrow',Arial,sans-serif;letter-spacing:.22em;text-transform:uppercase;fill:#7b7f79}"
             ".ml{font:800 19px 'Barlow Condensed','Arial Narrow',Arial,sans-serif;letter-spacing:.2em;text-transform:uppercase;fill:#101113;paint-order:stroke;stroke:#ead9bf;stroke-width:4px;stroke-linejoin:round}"
             "@media (max-width:600px){.edge{display:none}}"
             "</style>")
    o.append(f'<rect width="{W}" height="{H}" fill="#d5d8d2"/>')
    for name, cls in COUNTIES:
        o.append(f'<path class="{cls}" d="{_path(name)}"/>')
    corr = " ".join(f"{x},{y}" for x, y in (xy(a, b) for a, b in CORRIDOR))
    rail = corr
    o.append(f'<polyline class="corr" points="{corr}"/>')
    o.append(f'<polyline class="tie" points="{rail}"/>')
    o.append(f'<polyline class="rail" points="{rail}"/>')
    for name, lat, lon, edge in REGIONS:
        x, y = xy(lat, lon)
        cls = "rg edge" if edge else "rg"
        o.append(f'<text class="{cls}" x="{x}" y="{y}" text-anchor="middle">{name}</text>')
    for name, lat, lon, side in TOWNS:
        x, y = xy(lat, lon)
        o.append(f'<circle class="dot" cx="{x}" cy="{y}" r="4"/>')
        if side == "r":
            o.append(f'<text class="tn" x="{x + 9}" y="{y + 5}">{name}</text>')
        elif side == "l":
            o.append(f'<text class="tn" x="{x - 9}" y="{y + 5}" text-anchor="end">{name}</text>')
        elif side == "tr":
            o.append(f'<text class="tn" x="{x + 4}" y="{y - 10}">{name}</text>')
        elif side == "t":
            o.append(f'<text class="tn" x="{x}" y="{y - 10}" text-anchor="middle">{name}</text>')
        else:
            o.append(f'<text class="tn" x="{x}" y="{y + 20}" text-anchor="middle">{name}</text>')
    hx, hy = xy(HOME[1], HOME[2])
    o.append(f'<circle class="home" cx="{hx}" cy="{hy}" r="8"/>')
    o.append(f'<text class="hn" x="{hx + 15}" y="{hy + 7}">{HOME[0]}</text>')
    # the corridor's own name, set along the line between Villanova and Devon
    x, y = xy(40.071, -75.372)
    o.append(f'<text class="ml" x="{x}" y="{y}" text-anchor="middle">The Main Line</text>')
    o.append("</svg>")
    return "".join(o)


if __name__ == "__main__":
    print(area_map_svg())
