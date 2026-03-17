"""Extract and parse SVG style attributes into stroke/fill/width/dashes."""

import re

# Minimal SVG named colors (most common)
_SVG_NAMED = {
    'black': (0, 0, 0), 'white': (255, 255, 255), 'red': (255, 0, 0),
    'green': (0, 128, 0), 'blue': (0, 0, 255), 'yellow': (255, 255, 0),
    'cyan': (0, 255, 255), 'magenta': (255, 0, 255), 'orange': (255, 165, 0),
    'gray': (128, 128, 128), 'grey': (128, 128, 128),
    'none': None,
}


def parse_color(color_str):
    """Parse SVG color string to (r, g, b) floats 0-1, or None."""
    if not color_str or color_str.strip() == 'none':
        return None

    color_str = color_str.strip().lower()

    if color_str in _SVG_NAMED:
        val = _SVG_NAMED[color_str]
        return (val[0] / 255, val[1] / 255, val[2] / 255) if val else None

    # #rrggbb
    m = re.match(r'^#([0-9a-f]{6})$', color_str)
    if m:
        h = m.group(1)
        return (int(h[0:2], 16) / 255, int(h[2:4], 16) / 255, int(h[4:6], 16) / 255)

    # #rgb
    m = re.match(r'^#([0-9a-f]{3})$', color_str)
    if m:
        h = m.group(1)
        return (int(h[0]*2, 16) / 255, int(h[1]*2, 16) / 255, int(h[2]*2, 16) / 255)

    # rgb(r, g, b) — values 0-255
    m = re.match(r'^rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)$', color_str)
    if m:
        return (int(m.group(1)) / 255, int(m.group(2)) / 255, int(m.group(3)) / 255)

    return None


def parse_dasharray(dash_str):
    """Parse stroke-dasharray to a list of floats, or None if solid."""
    if not dash_str or dash_str.strip() == 'none':
        return None
    nums = re.findall(r'[\d.]+', dash_str)
    return [float(n) for n in nums] if nums else None


class SVGStyle:
    """Parsed SVG style for a single element."""

    __slots__ = ('stroke', 'fill', 'stroke_width', 'dashes', 'opacity')

    def __init__(self, stroke=None, fill=None, stroke_width=1.0,
                 dashes=None, opacity=1.0):
        self.stroke = stroke        # (r,g,b) 0-1 or None
        self.fill = fill            # (r,g,b) 0-1 or None
        self.stroke_width = stroke_width
        self.dashes = dashes        # list of floats or None
        self.opacity = opacity


def extract_style(elem):
    """Extract SVGStyle from an XML element (attributes + inline style)."""
    attrs = {}

    # Direct XML attributes
    for key in ('stroke', 'fill', 'stroke-width', 'stroke-dasharray',
                'opacity', 'stroke-opacity', 'fill-opacity'):
        val = elem.get(key)
        if val:
            attrs[key] = val

    # Inline style="" overrides
    style_str = elem.get('style', '')
    for part in style_str.split(';'):
        part = part.strip()
        if ':' in part:
            k, v = part.split(':', 1)
            attrs[k.strip()] = v.strip()

    return SVGStyle(
        stroke=parse_color(attrs.get('stroke')),
        fill=parse_color(attrs.get('fill')),
        stroke_width=float(attrs.get('stroke-width', 1.0) or 1.0),
        dashes=parse_dasharray(attrs.get('stroke-dasharray')),
        opacity=float(attrs.get('opacity', 1.0) or 1.0),
    )
