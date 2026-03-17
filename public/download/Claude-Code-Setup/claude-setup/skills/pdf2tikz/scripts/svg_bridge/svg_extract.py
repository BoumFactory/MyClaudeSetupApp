"""Extract SVG elements from a PyMuPDF page via get_svg_image()."""

import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from typing import List, Optional

from .svg_transforms import parse_transform
from .svg_style import extract_style, SVGStyle


SVG_NS = '{http://www.w3.org/2000/svg}'


@dataclass
class SVGElement:
    """A single SVG graphic element with accumulated transforms."""
    tag: str                           # 'path', 'line', 'rect', 'circle', 'ellipse'
    d: Optional[str] = None            # path d-attribute (for <path> only)
    style: SVGStyle = field(default_factory=SVGStyle)
    transform_stack: List[tuple] = field(default_factory=list)
    # For primitive elements (line, rect, circle, ellipse)
    attrs: dict = field(default_factory=dict)


def _walk_svg(elem, transform_stack, elements):
    """Recursively walk SVG DOM, collecting graphic elements."""
    tag = elem.tag.replace(SVG_NS, '')

    # Accumulate transform from this element
    tr = elem.get('transform')
    current_stack = transform_stack + ([parse_transform(tr)] if tr else [])

    if tag == 'path':
        d = elem.get('d')
        if d:
            elements.append(SVGElement(
                tag='path',
                d=d,
                style=extract_style(elem),
                transform_stack=list(current_stack),
            ))

    elif tag == 'line':
        elements.append(SVGElement(
            tag='line',
            style=extract_style(elem),
            transform_stack=list(current_stack),
            attrs={k: float(elem.get(k, 0)) for k in ('x1', 'y1', 'x2', 'y2')},
        ))

    elif tag == 'rect':
        elements.append(SVGElement(
            tag='rect',
            style=extract_style(elem),
            transform_stack=list(current_stack),
            attrs={k: float(elem.get(k, 0))
                   for k in ('x', 'y', 'width', 'height')},
        ))

    elif tag == 'circle':
        elements.append(SVGElement(
            tag='circle',
            style=extract_style(elem),
            transform_stack=list(current_stack),
            attrs={k: float(elem.get(k, 0)) for k in ('cx', 'cy', 'r')},
        ))

    elif tag == 'ellipse':
        elements.append(SVGElement(
            tag='ellipse',
            style=extract_style(elem),
            transform_stack=list(current_stack),
            attrs={k: float(elem.get(k, 0)) for k in ('cx', 'cy', 'rx', 'ry')},
        ))

    # Recurse into children (g, svg, defs, etc.)
    for child in elem:
        _walk_svg(child, current_stack, elements)


def extract_svg_elements(page):
    """Extract all graphic elements from a page's SVG representation.

    Returns (elements, viewbox_width, viewbox_height).
    """
    svg_str = page.get_svg_image()
    root = ET.fromstring(svg_str)

    # Parse viewBox for coordinate system
    viewbox = root.get('viewBox', '')
    parts = re.findall(r'[+-]?[\d.]+', viewbox)
    if len(parts) >= 4:
        vb_w, vb_h = float(parts[2]), float(parts[3])
    else:
        vb_w = float(root.get('width', page.rect.width))
        vb_h = float(root.get('height', page.rect.height))

    elements = []
    _walk_svg(root, [], elements)

    return elements, vb_w, vb_h
